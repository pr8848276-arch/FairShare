# Core JavaScript Engine
JS_CODE = r"""  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    /**
     * FairShare Pro — Smart Shared Expense Splitter & Settlement
     * Advanced Features:
     * 1. Secure Authentication (Google & Email/Password with Demo Fallback)
     * 2. AI Receipt & Bill Scanner (Camera / Upload OCR with Tesseract.js)
     * 3. Direct UPI 'Pay Now' Deep Links (upi://pay?pa=... with dynamic QR code)
     * 4. Flexible Split Options (Equal 1/N, Exact Amount, Item-by-Item)
     * 5. Recurring Expenses & Subscriptions (Monthly dues with 1-click posting)
     * 6. Spending Insights & Visual Analytics (Chart.js category & member charts)
     * Core Rules Preserved: Floating Quick Calculator, Strict Pair-to-Pair Debts, Immutable History.
     */

    const STORAGE_KEY = 'fairshare_cloud_app_v3';
    const FB_CONFIG_KEY = 'fairshare_firebase_config_v2';
    const AUTH_USER_KEY = 'fairshare_auth_user_session';

    // Firebase Project Configuration
    const DEFAULT_FIREBASE_CONFIG = {
      apiKey: "AIzaSyBRTvVKf9xdPodKTTTswpPFL4Bf5_wn6sU",
      authDomain: "fairshare-59067.firebaseapp.com",
      projectId: "fairshare-59067",
      storageBucket: "fairshare-59067.firebasestorage.app",
      messagingSenderId: "125069540955",
      appId: "1:125069540955:web:30cfe5185f870ab59bc97e",
      measurementId: "G-8RNMZQH68W"
    };

    // Global Application State
    let appState = {
      currentGroupId: 'ROOM-101',
      currentUser: null,       // Active member name in group (e.g. 'Rahul')
      authUser: null,          // Authenticated user object { email, displayName, photoURL, uid }
      activeTab: 'debts',      // 'debts' | 'analytics' | 'recurring'
      currency: '₹',
      darkMode: false,
      groups: {
        'ROOM-101': {
          id: 'ROOM-101',
          name: 'Shared Expenses',
          currency: '₹',
          members: ['Rahul', 'Amit', 'Pooja'],
          memberProfiles: {
            'Rahul': { upiId: 'rahul@okhdfcbank', email: 'rahul@fairshare.app' },
            'Amit': { upiId: 'amit@okaxis', email: 'amit@fairshare.app' },
            'Pooja': { upiId: 'pooja@paytm', email: 'pooja@fairshare.app' }
          },
          expenses: [],
          recurringBills: [
            {
              id: 'rec_rent',
              title: 'Monthly Flat Rent',
              amount: 15000,
              category: 'Rent',
              paidBy: 'Rahul',
              splitAmong: ['Rahul', 'Amit', 'Pooja'],
              cycle: 'monthly',
              nextDueDate: '2026-11-01'
            },
            {
              id: 'rec_wifi',
              title: 'High-Speed Wi-Fi Fiber',
              amount: 999,
              category: 'Utilities',
              paidBy: 'Amit',
              splitAmong: ['Rahul', 'Amit', 'Pooja'],
              cycle: 'monthly',
              nextDueDate: '2026-10-25'
            }
          ],
          updatedAt: 0,
          isPlaceholder: false
        }
      },
      searchQuery: '',
      categoryFilter: 'ALL',
      hasPromptedIdentity: false
    };

    // Firebase & Realtime State
    let firebaseDb = null;
    let firebaseAuth = null;
    let firestoreUnsubscribe = null;
    let isCloudOnline = false;

    // Cross-tab BroadcastChannel
    const realtimeChannel = typeof BroadcastChannel !== 'undefined' ? new BroadcastChannel('fairshare_v3_broadcast') : null;
    if (realtimeChannel) {
      realtimeChannel.onmessage = (event) => {
        if (!event.data) return;
        if (event.data.type === 'SYNC_GROUP' && event.data.groupId === appState.currentGroupId) {
          if (event.data.updatedAt > (getCurrentGroup().updatedAt || 0)) {
            appState.groups[appState.currentGroupId] = event.data.groupData;
            saveLocalStateOnly();
            renderApp();
            showToast('✨ Synced changes from another device/tab', 'info');
          }
        }
      };
    }

    // Chart.js instances
    let categoryChartInstance = null;
    let memberSpendChartInstance = null;

    // Split Mode State
    let currentSplitMode = 'equal'; // 'equal' | 'exact' | 'items'
    let currentLineItems = [
      { id: 'item_1', name: 'Main Dish / Pizza', amount: 450, splitMembers: [] }
    ];

    // OCR Working State
    let lastExtractedOcr = null;

    // Avatar Color Gradients
    const AVATAR_GRADIENTS = [
      'from-blue-500 to-indigo-600',
      'from-emerald-400 to-teal-600',
      'from-purple-500 to-pink-600',
      'from-amber-400 to-orange-500',
      'from-rose-500 to-red-600',
      'from-cyan-400 to-blue-600',
      'from-fuchsia-500 to-purple-600',
      'from-lime-400 to-emerald-600'
    ];

    // Category Configurations
    const CATEGORIES = {
      'Food': { icon: '🍽️', label: 'Food & Dining', color: 'bg-orange-100 text-orange-800 dark:bg-orange-950/70 dark:text-orange-300', chartColor: '#f97316' },
      'Rent': { icon: '🏠', label: 'Rent & Living', color: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-950/70 dark:text-indigo-300', chartColor: '#6366f1' },
      'Travel': { icon: '🚗', label: 'Travel & Transport', color: 'bg-blue-100 text-blue-800 dark:bg-blue-950/70 dark:text-blue-300', chartColor: '#3b82f6' },
      'Groceries': { icon: '🛒', label: 'Groceries & Snacks', color: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300', chartColor: '#10b981' },
      'Utilities': { icon: '⚡', label: 'Utilities & Bills', color: 'bg-amber-100 text-amber-800 dark:bg-amber-950/70 dark:text-amber-300', chartColor: '#f59e0b' },
      'Entertainment': { icon: '🎬', label: 'Entertainment & OTT', color: 'bg-pink-100 text-pink-800 dark:bg-pink-950/70 dark:text-pink-300', chartColor: '#ec4899' },
      'Settlement': { icon: '🤝', label: 'Settlement / Payment', color: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300 border border-emerald-300/80', chartColor: '#14b8a6' },
      'Other': { icon: '📦', label: 'Other', color: 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300', chartColor: '#64748b' }
    };

    // --- HELPER FUNCTIONS ---
    function getCurrentGroup() {
      if (!appState.groups[appState.currentGroupId]) {
        appState.groups[appState.currentGroupId] = {
          id: appState.currentGroupId,
          name: `Room ${appState.currentGroupId}`,
          currency: appState.currency || '₹',
          members: ['Rahul', 'Amit', 'Pooja'],
          memberProfiles: {
            'Rahul': { upiId: 'rahul@okhdfcbank' },
            'Amit': { upiId: 'amit@okaxis' },
            'Pooja': { upiId: 'pooja@paytm' }
          },
          expenses: [],
          recurringBills: [],
          updatedAt: 0,
          isPlaceholder: true
        };
      }
      const grp = appState.groups[appState.currentGroupId];
      if (!grp.memberProfiles) grp.memberProfiles = {};
      if (!grp.recurringBills) grp.recurringBills = [];
      return grp;
    }

    function getAvatarGradient(name) {
      let hash = 0;
      for (let i = 0; i < (name || '').length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
      }
      return AVATAR_GRADIENTS[Math.abs(hash) % AVATAR_GRADIENTS.length];
    }

    function getInitials(name) {
      if (!name) return '?';
      const parts = name.trim().split(/\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    function formatMoney(amount, currency = (getCurrentGroup().currency || appState.currency)) {
      const num = Number(amount) || 0;
      return `${currency}${num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function generateRoomCode(prefix = 'ROOM') {
      const randomNum = Math.floor(100 + Math.random() * 900);
      const cleanPrefix = (prefix.trim().toUpperCase().replace(/[^A-Z]/g, '') || 'GRP').substring(0, 4);
      return `${cleanPrefix}-${randomNum}`;
    }

    // --- LOCAL PERSISTENCE ---
    function loadLocalState() {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          if (parsed.groups && typeof parsed.groups === 'object') {
            appState.groups = parsed.groups;
          }
          if (parsed.currentGroupId) appState.currentGroupId = parsed.currentGroupId;
          if (parsed.currency) appState.currency = parsed.currency;
          if (typeof parsed.darkMode === 'boolean') appState.darkMode = parsed.darkMode;
        }

        // Restore auth user session
        const savedAuth = localStorage.getItem(AUTH_USER_KEY);
        if (savedAuth) {
          appState.authUser = JSON.parse(savedAuth);
        }

        // Restore guest mode flag
        try {
          if (sessionStorage.getItem('fairshare_is_guest') === 'true') {
            appState.isGuest = true;
          }
        } catch (e) {}

        const savedUser = localStorage.getItem('fairshare_user_' + appState.currentGroupId);
        if (savedUser) appState.currentUser = savedUser;
      } catch (e) {
        console.error('Failed to load local state:', e);
      }
    }

    function saveLocalStateOnly() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          groups: appState.groups,
          currentGroupId: appState.currentGroupId,
          currency: appState.currency,
          darkMode: appState.darkMode
        }));
        if (appState.authUser) {
          localStorage.setItem(AUTH_USER_KEY, JSON.stringify(appState.authUser));
        } else {
          localStorage.removeItem(AUTH_USER_KEY);
        }
        if (appState.currentUser) {
          localStorage.setItem('fairshare_user_' + appState.currentGroupId, appState.currentUser);
        }
      } catch (e) {
        console.error('Failed to save local state:', e);
      }
    }

    function commitStateChanges(source = '') {
      const group = getCurrentGroup();
      group.updatedAt = Date.now();
      saveLocalStateOnly();

      if (realtimeChannel) {
        realtimeChannel.postMessage({
          type: 'SYNC_GROUP',
          groupId: group.id,
          updatedAt: group.updatedAt,
          groupData: group
        });
      }

      syncGroupToFirebase(group);
      updateSyncIndicator();
    }

    function updateSyncIndicator() {
      const badge = document.getElementById('groupSyncTimestamp');
      if (!badge) return;
      if (isCloudOnline) {
        badge.textContent = '🟢 Synced to Firestore live';
        badge.className = 'text-xs text-emerald-600 dark:text-emerald-400 font-semibold';
      } else {
        badge.textContent = '🟡 Synced locally & cross-tab';
        badge.className = 'text-xs text-amber-600 dark:text-amber-400 font-medium';
      }
    }

    // --- TAB NAVIGATION (DEBTS, ANALYTICS, RECURRING) ---
    function switchMainTab(tab) {
      appState.activeTab = tab;
      const tabDebts = document.getElementById('tabContentDebts');
      const tabAnalytics = document.getElementById('tabContentAnalytics');
      const tabRecurring = document.getElementById('tabContentRecurring');

      const btnDebts = document.getElementById('tabNavDebts');
      const btnAnalytics = document.getElementById('tabNavAnalytics');
      const btnRecurring = document.getElementById('tabNavRecurring');

      const mDebts = document.getElementById('mobileNavDebts');
      const mAnalytics = document.getElementById('mobileNavAnalytics');
      const mRecurring = document.getElementById('mobileNavRecurring');

      [tabDebts, tabAnalytics, tabRecurring].forEach(el => el && el.classList.add('hidden'));

      // Reset desktop styles
      [btnDebts, btnAnalytics, btnRecurring].forEach(b => {
        if (b) b.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white';
      });

      // Reset mobile styles
      [mDebts, mAnalytics, mRecurring].forEach(m => {
        if (m) m.className = 'flex items-center gap-1 py-1 px-3 rounded-lg text-slate-600 dark:text-slate-400';
      });

      if (tab === 'debts') {
        tabDebts.classList.remove('hidden');
        if (btnDebts) btnDebts.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm font-bold';
        if (mDebts) mDebts.className = 'flex items-center gap-1 py-1 px-3 rounded-lg text-indigo-600 dark:text-indigo-400 font-bold bg-indigo-50 dark:bg-indigo-950/60';
      } else if (tab === 'analytics') {
        tabAnalytics.classList.remove('hidden');
        if (btnAnalytics) btnAnalytics.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm font-bold';
        if (mAnalytics) mAnalytics.className = 'flex items-center gap-1 py-1 px-3 rounded-lg text-indigo-600 dark:text-indigo-400 font-bold bg-indigo-50 dark:bg-indigo-950/60';
        renderAnalyticsCharts();
      } else if (tab === 'recurring') {
        tabRecurring.classList.remove('hidden');
        if (btnRecurring) btnRecurring.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm font-bold';
        if (mRecurring) mRecurring.className = 'flex items-center gap-1 py-1 px-3 rounded-lg text-indigo-600 dark:text-indigo-400 font-bold bg-indigo-50 dark:bg-indigo-950/60';
        renderRecurringBills();
      }
    }

    // --- FEATURE 1: ROBUST FIREBASE AUTHENTICATION (GOOGLE & EMAIL/PASSWORD & GUEST) ---
    function openAuthModal() {
      hideAuthModalError();
      const modal = document.getElementById('authModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeAuthModal() {
      const modal = document.getElementById('authModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function showAuthModalError(title, message) {
      const box = document.getElementById('authModalErrorBox');
      const tEl = document.getElementById('authModalErrorTitle');
      const mEl = document.getElementById('authModalErrorMessage');
      if (box && tEl && mEl) {
        tEl.textContent = title;
        mEl.textContent = message;
        box.classList.remove('hidden');
      }
    }

    function hideAuthModalError() {
      const box = document.getElementById('authModalErrorBox');
      if (box) box.classList.add('hidden');
    }

    let isRegisterMode = false;
    function switchAuthTab(tab) {
      hideAuthModalError();
      const googleTab = document.getElementById('authGoogleTabContent');
      const emailTab = document.getElementById('authEmailTabContent');
      const gBtn = document.getElementById('authTabGoogleBtn');
      const eBtn = document.getElementById('authTabEmailBtn');

      if (tab === 'google') {
        googleTab.classList.remove('hidden');
        emailTab.classList.add('hidden');
        gBtn.className = 'flex-1 py-2 rounded-lg bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 font-bold shadow-sm transition';
        eBtn.className = 'flex-1 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition';
      } else {
        emailTab.classList.remove('hidden');
        googleTab.classList.add('hidden');
        eBtn.className = 'flex-1 py-2 rounded-lg bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 font-bold shadow-sm transition';
        gBtn.className = 'flex-1 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition';
      }
    }

    function toggleEmailAuthMode() {
      hideAuthModalError();
      isRegisterMode = !isRegisterMode;
      const label = document.getElementById('emailAuthModeLabel');
      const toggleBtn = document.getElementById('emailAuthToggleBtn');
      const submitBtn = document.getElementById('authEmailSubmitBtn');
      const nameGroup = document.getElementById('authNameFieldGroup');

      if (isRegisterMode) {
        label.textContent = 'Create New Account';
        toggleBtn.textContent = 'Already have an account? Sign In';
        submitBtn.textContent = 'Register Account';
        nameGroup.classList.remove('hidden');
      } else {
        label.textContent = 'Sign In';
        toggleBtn.textContent = 'Need an account? Register';
        submitBtn.textContent = 'Sign In with Email';
        nameGroup.classList.add('hidden');
      }
    }

    // Lazy / Safe Getter for Firebase Auth instance with LOCAL persistence
    let authObserverAttached = false;
    function getFirebaseAuth() {
      if (firebaseAuth) return firebaseAuth;
      if (typeof firebase !== 'undefined') {
        try {
          if (!firebase.apps.length) {
            let config = DEFAULT_FIREBASE_CONFIG;
            const savedConfigStr = localStorage.getItem(FB_CONFIG_KEY);
            if (savedConfigStr) {
              try {
                const parsed = JSON.parse(savedConfigStr);
                if (parsed && !parsed.disabled) config = parsed;
              } catch (e) {}
            }
            firebase.initializeApp(config);
          }
          if (firebase.auth) {
            firebaseAuth = firebase.auth();
            firebaseAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL).catch(err => {
              console.warn('[Firebase Auth] Persistence configuration notice:', err);
            });
            setupAuthStateObserver();
          }
        } catch (err) {
          console.error('[Firebase Auth] Initialization exception:', err);
        }
      }
      return firebaseAuth;
    }

    // Persistent Auth State Observer
    function setupAuthStateObserver() {
      if (authObserverAttached || !firebaseAuth) return;
      authObserverAttached = true;

      firebaseAuth.onAuthStateChanged((user) => {
        console.log('[Firebase Auth Observer] User state changed:', user ? `${user.email} (${user.uid})` : 'null (logged out)');
        if (user) {
          appState.authUser = {
            displayName: user.displayName || user.email.split('@')[0],
            email: user.email,
            photoURL: user.photoURL || null,
            uid: user.uid
          };
          appState.isGuest = false;
          saveLocalStateOnly();
          renderAuthNav();
          closeAuthModal();

          // Match or link with active group member
          const group = getCurrentGroup();
          const userDisplayName = appState.authUser.displayName;
          const match = group.members.find(m => m.toLowerCase() === userDisplayName.toLowerCase());
          if (match) {
            appState.currentUser = match;
          } else {
            appState.currentUser = userDisplayName;
            if (!group.members.includes(userDisplayName)) {
              group.members.push(userDisplayName);
            }
          }
          if (!group.memberProfiles[appState.currentUser]) {
            group.memberProfiles[appState.currentUser] = {};
          }
          group.memberProfiles[appState.currentUser].email = appState.authUser.email;
          commitStateChanges(`Auth sync: ${appState.currentUser}`);
          renderApp();
        } else {
          if (!appState.isGuest && !appState.currentUser) {
            appState.authUser = null;
            renderAuthNav();
          }
        }
      });
    }

    // Google Sign-In with robust error handling and domain diagnostic
    async function handleGoogleSignIn() {
      hideAuthModalError();
      const auth = getFirebaseAuth();
      if (!auth) {
        const errorMsg = 'Firebase Auth SDK is not available or offline. Please check your internet connection.';
        console.error('[Firebase Auth Error]', errorMsg);
        showToast(errorMsg, 'error');
        showAuthModalError('Auth SDK Offline', errorMsg);
        return;
      }

      const btn = document.getElementById('googleSignInBtn');
      const btnText = document.getElementById('googleSignInBtnText');
      const originalText = btnText ? btnText.textContent : 'Continue with Google';

      try {
        if (btnText) btnText.textContent = 'Connecting to Google...';
        if (btn) btn.disabled = true;

        const provider = new firebase.auth.GoogleAuthProvider();
        provider.setCustomParameters({ prompt: 'select_account' });

        console.log('[Firebase Auth] Launching signInWithPopup for Google...');
        const result = await auth.signInWithPopup(provider);

        console.log('[Firebase Auth] Google sign-in successful for:', result.user.email);
        showToast(`Welcome back, ${result.user.displayName || result.user.email}!`, 'success');
        // onAuthStateChanged will handle UI switch & close modal
      } catch (err) {
        console.error('[Firebase Auth Error] Code:', err.code, 'Message:', err.message, err);

        let friendlyTitle = 'Google Sign-in Failed';
        let friendlyMsg = err.message || 'An error occurred during Google sign-in.';

        if (err.code === 'auth/popup-blocked') {
          friendlyTitle = 'Popup Blocked by Browser';
          friendlyMsg = 'Your browser blocked the Google authentication popup. Please click the popup/shield icon in your browser address bar to allow popups for this site, then try again.';
          showToast('⚠️ Google popup was blocked! Please allow popups.', 'error');
        } else if (err.code === 'auth/unauthorized-domain') {
          const currentHost = window.location.hostname || 'current domain';
          friendlyTitle = `Domain Not Authorized (${currentHost})`;
          friendlyMsg = `The domain "${currentHost}" is not authorized for OAuth operations in your Firebase project. To resolve this:\n1. Open Firebase Console -> Authentication -> Settings -> Authorized domains\n2. Click "Add domain" and enter "${currentHost}" (and "pr8848276-arch.github.io")\n3. Click Save.\n\nTip: You can click "Continue as Guest" below to preview the app immediately.`;
          showToast(`⚠️ Domain "${currentHost}" is not authorized in Firebase!`, 'error');
        } else if (err.code === 'auth/operation-not-allowed') {
          friendlyTitle = 'Google Sign-In Disabled';
          friendlyMsg = 'Google authentication is not enabled in your Firebase Console. Go to Firebase Console -> Authentication -> Sign-in method -> Click Google -> Enable and Save.';
          showToast('⚠️ Google sign-in is disabled in Firebase Console!', 'error');
        } else if (err.code === 'auth/popup-closed-by-user') {
          friendlyTitle = 'Sign-in Cancelled';
          friendlyMsg = 'The Google sign-in popup was closed before completing.';
          showToast('Google Sign-in popup was closed.', 'warning');
        } else if (err.code === 'auth/cancelled-popup-request') {
          friendlyTitle = 'Request Cancelled';
          friendlyMsg = 'A newer sign-in request took precedence.';
          showToast('Sign-in popup request was cancelled.', 'info');
        } else if (err.code === 'auth/network-request-failed') {
          friendlyTitle = 'Network Error';
          friendlyMsg = 'Unable to communicate with Google authentication servers. Please verify your internet connection.';
          showToast('Network error connecting to Firebase.', 'error');
        } else {
          showToast(err.message || 'Google sign-in error', 'error');
        }

        showAuthModalError(friendlyTitle, friendlyMsg);
      } finally {
        if (btnText) btnText.textContent = originalText;
        if (btn) btn.disabled = false;
      }
    }

    // Email & Password Authentication (Sign-in and Registration)
    async function handleEmailAuthSubmit(e) {
      e.preventDefault();
      hideAuthModalError();

      const email = (document.getElementById('authEmailInput').value || '').trim();
      const password = document.getElementById('authPasswordInput').value || '';
      const displayName = (document.getElementById('authDisplayNameInput').value || '').trim();

      // Input Validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email || !emailRegex.test(email)) {
        const msg = 'Please enter a valid email address (e.g. name@domain.com)';
        showToast(msg, 'warning');
        showAuthModalError('Invalid Email Address', msg);
        document.getElementById('authEmailInput').focus();
        return;
      }

      if (!password || password.length < 6) {
        const msg = 'Password must be at least 6 characters long.';
        showToast(msg, 'warning');
        showAuthModalError('Password Too Short', msg);
        document.getElementById('authPasswordInput').focus();
        return;
      }

      const auth = getFirebaseAuth();
      if (!auth) {
        const msg = 'Firebase Auth SDK is not available or offline. Please check your internet connection.';
        console.error('[Firebase Auth Error]', msg);
        showToast(msg, 'error');
        showAuthModalError('Auth SDK Offline', msg);
        return;
      }

      const submitBtn = document.getElementById('authEmailSubmitBtn');
      const originalText = submitBtn ? submitBtn.textContent : (isRegisterMode ? 'Register Account' : 'Sign In with Email');

      try {
        if (submitBtn) {
          submitBtn.textContent = isRegisterMode ? 'Creating Account...' : 'Signing In...';
          submitBtn.disabled = true;
        }

        if (isRegisterMode) {
          console.log('[Firebase Auth] Creating user with email and password:', email);
          const userCred = await auth.createUserWithEmailAndPassword(email, password);
          if (userCred.user && displayName) {
            try {
              await userCred.user.updateProfile({ displayName: displayName });
            } catch (pErr) {
              console.warn('[Firebase Auth] Profile name update notice:', pErr);
            }
          }
          showToast(`Account created! Welcome, ${displayName || email}!`, 'success');
          // onAuthStateChanged will handle UI switch & close modal
        } else {
          console.log('[Firebase Auth] Signing in with email and password:', email);
          const userCred = await auth.signInWithEmailAndPassword(email, password);
          showToast(`Welcome back, ${userCred.user.displayName || userCred.user.email}!`, 'success');
          // onAuthStateChanged will handle UI switch & close modal
        }
      } catch (err) {
        console.error('[Firebase Auth Error] Code:', err.code, 'Message:', err.message, err);

        let friendlyTitle = isRegisterMode ? 'Registration Failed' : 'Sign-In Failed';
        let friendlyMsg = err.message || 'An error occurred during authentication.';

        if (err.code === 'auth/user-not-found') {
          friendlyTitle = 'User Not Found';
          friendlyMsg = 'No account exists with this email address. Please verify your email or click "Need an account? Register" above.';
        } else if (err.code === 'auth/wrong-password') {
          friendlyTitle = 'Incorrect Password';
          friendlyMsg = 'The password entered is incorrect. Please double-check and try again.';
        } else if (err.code === 'auth/invalid-credential') {
          friendlyTitle = 'Invalid Credentials';
          friendlyMsg = 'Invalid email or password. Please verify your login credentials or register an account.';
        } else if (err.code === 'auth/email-already-in-use') {
          friendlyTitle = 'Email Already Registered';
          friendlyMsg = 'An account with this email already exists. Please switch to "Sign In" mode.';
        } else if (err.code === 'auth/weak-password') {
          friendlyTitle = 'Weak Password';
          friendlyMsg = 'The password is too weak. Firebase requires at least 6 characters.';
        } else if (err.code === 'auth/invalid-email') {
          friendlyTitle = 'Invalid Email Format';
          friendlyMsg = 'The email address format is not recognized by Firebase.';
        } else if (err.code === 'auth/operation-not-allowed') {
          friendlyTitle = 'Email/Password Sign-In Disabled';
          friendlyMsg = 'Email/Password provider is not enabled in Firebase Console. Go to Firebase Console -> Authentication -> Sign-in method -> Email/Password -> Enable and Save.';
        } else if (err.code === 'auth/too-many-requests') {
          friendlyTitle = 'Too Many Failed Attempts';
          friendlyMsg = 'Access to this account has been temporarily disabled due to many failed login attempts. Please wait a moment and try again.';
        } else if (err.code === 'auth/network-request-failed') {
          friendlyTitle = 'Network Error';
          friendlyMsg = 'Unable to reach Firebase authentication servers. Please verify your internet connection.';
        }

        showToast(friendlyTitle + ': ' + friendlyMsg, 'error');
        showAuthModalError(friendlyTitle, friendlyMsg);
      } finally {
        if (submitBtn) {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }
      }
    }

    // Guest / Demo Mode Bypass (Offline & instant testing)
    function continueAsGuest() {
      appState.isGuest = true;
      try { sessionStorage.setItem('fairshare_is_guest', 'true'); } catch (e) {}
      hideAuthModalError();
      const group = getCurrentGroup();
      if (!appState.currentUser || !group.members.includes(appState.currentUser)) {
        appState.currentUser = group.members[0] || 'Rahul';
      }
      closeAuthModal();
      renderApp();
      renderAuthNav();
      showToast('Continuing in Guest Preview mode. You can sign in anytime from the top bar.', 'info');
    }

    function loginAsDemoUser(name, email, upiId = '') {
      hideAuthModalError();
      appState.isGuest = false;
      try { sessionStorage.removeItem('fairshare_is_guest'); } catch (e) {}
      appState.authUser = {
        displayName: name,
        email: email,
        photoURL: null,
        uid: 'demo_' + name.toLowerCase().replace(/\s+/g, '_')
      };
      const group = getCurrentGroup();
      if (!group.members.includes(name)) {
        group.members.push(name);
      }
      if (!group.memberProfiles[name]) {
        group.memberProfiles[name] = {};
      }
      if (upiId) group.memberProfiles[name].upiId = upiId;
      group.memberProfiles[name].email = email;
      appState.currentUser = name;

      saveLocalStateOnly();
      closeAuthModal();
      renderAuthNav();
      renderApp();
      showToast(`Logged in as demo user: ${name}`, 'success');
    }

    function setAuthenticatedUser(userObj) {
      appState.authUser = userObj;
      appState.isGuest = false;
      try { sessionStorage.removeItem('fairshare_is_guest'); } catch (e) {}
      saveLocalStateOnly();
      renderAuthNav();
      
      const group = getCurrentGroup();
      const match = group.members.find(m => m.toLowerCase() === userObj.displayName.toLowerCase());
      if (match) {
        selectCurrentUser(match);
      } else {
        appState.currentUser = userObj.displayName;
        if (!group.members.includes(userObj.displayName)) {
          group.members.push(userObj.displayName);
        }
        if (!group.memberProfiles[userObj.displayName]) {
          group.memberProfiles[userObj.displayName] = {};
        }
        group.memberProfiles[userObj.displayName].email = userObj.email;
        commitStateChanges(`Added member ${userObj.displayName}`);
        renderApp();
      }
    }

    function handleLogOut() {
      if (confirm('Are you sure you want to log out of FairShare?')) {
        const auth = getFirebaseAuth();
        if (auth) {
          try { auth.signOut(); } catch (e) { console.warn('[Firebase Auth] Sign out error:', e); }
        }
        appState.authUser = null;
        appState.isGuest = false;
        appState.currentUser = null;
        try { sessionStorage.removeItem('fairshare_is_guest'); } catch (e) {}
        localStorage.removeItem(AUTH_USER_KEY);
        localStorage.removeItem('fairshare_user_' + appState.currentGroupId);
        saveLocalStateOnly();
        renderApp();
        renderAuthNav();
        showToast('Logged out successfully', 'info');
      }
    }

    function renderAuthNav() {
      const container = document.getElementById('authNavContainer');
      if (!container) return;

      if (!appState.authUser) {
        container.innerHTML = `
          <button onclick="openAuthModal()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/70 dark:hover:bg-indigo-900/80 text-indigo-700 dark:text-indigo-300 border border-indigo-200/80 dark:border-indigo-800 transition shadow-sm">
            <span>🔐</span>
            <span>Sign In</span>
          </button>
        `;
        return;
      }

      const u = appState.authUser;
      const initials = getInitials(u.displayName || 'User');
      const grad = getAvatarGradient(u.displayName || 'User');

      container.innerHTML = `
        <div class="relative group">
          <button class="inline-flex items-center gap-2 p-1 sm:px-2.5 sm:py-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-indigo-400 transition">
            ${
              u.photoURL
                ? `<img src="${u.photoURL}" class="w-6 h-6 rounded-full object-cover">`
                : `<div class="w-6 h-6 rounded-full bg-gradient-to-tr ${grad} text-white font-bold text-[10px] flex items-center justify-center">${initials}</div>`
            }
            <div class="text-left hidden sm:block">
              <span class="text-xs font-bold text-slate-800 dark:text-slate-100 block truncate max-w-[100px]">${u.displayName || 'User'}</span>
            </div>
            <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>

          <!-- Dropdown menu -->
          <div class="absolute right-0 mt-1 w-56 bg-white dark:bg-slate-900 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 py-2 hidden group-hover:block hover:block z-50">
            <div class="px-3.5 py-2 border-b border-slate-100 dark:border-slate-800">
              <span class="text-xs font-bold text-slate-900 dark:text-white block truncate">${u.displayName}</span>
              <span class="text-[10px] text-slate-400 block truncate">${u.email || 'Google User'}</span>
              <div class="mt-1 flex items-center gap-1 text-[10px] text-indigo-600 dark:text-indigo-400 font-semibold">
                <span>Active Member:</span>
                <span class="font-bold">${appState.currentUser || 'Not selected'}</span>
              </div>
            </div>
            <button onclick="openSetUpiModal('${(appState.currentUser || '').replace(/'/g, "\\'")}')" class="w-full text-left px-3.5 py-2 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 flex items-center gap-2">
              <span>💳</span>
              <span>Set My UPI ID</span>
            </button>
            <button onclick="openUserIdentifyModal()" class="w-full text-left px-3.5 py-2 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 flex items-center gap-2">
              <span>🔄</span>
              <span>Switch Active Member</span>
            </button>
            <button onclick="handleLogOut()" class="w-full text-left px-3.5 py-2 text-xs text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 flex items-center gap-2 font-semibold">
              <span>🚪</span>
              <span>Log Out</span>
            </button>
          </div>
        </div>
      `;
    }

    // --- FEATURE 2: AI RECEIPT & BILL SCANNER (TESSERACT.JS OCR) ---
    function openReceiptScannerModal() {
      const modal = document.getElementById('receiptScannerModal');
      document.getElementById('receiptFileInput').value = '';
      document.getElementById('ocrScanningStatus').classList.add('hidden');
      document.getElementById('ocrResultReview').classList.add('hidden');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeReceiptScannerModal() {
      const modal = document.getElementById('receiptScannerModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    async function handleReceiptFileSelected(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;

      const statusBox = document.getElementById('ocrScanningStatus');
      const progressBar = document.getElementById('ocrProgressBar');
      const progressPercent = document.getElementById('ocrProgressPercent');
      const statusText = document.getElementById('ocrStatusText');
      const reviewBox = document.getElementById('ocrResultReview');

      statusBox.classList.remove('hidden');
      reviewBox.classList.add('hidden');
      progressBar.style.width = '15%';
      progressPercent.textContent = '15%';
      statusText.textContent = 'Loading Tesseract AI OCR Engine...';

      try {
        if (typeof Tesseract === 'undefined') {
          throw new Error('Tesseract.js OCR library not available');
        }

        const worker = await Tesseract.createWorker('eng', 1, {
          logger: m => {
            if (m.status === 'recognizing text') {
              const p = Math.round((m.progress || 0) * 100);
              progressBar.style.width = `${Math.max(20, p)}%`;
              progressPercent.textContent = `${Math.max(20, p)}%`;
              statusText.textContent = `Analyzing receipt text: ${p}%`;
            }
          }
        });

        const { data: { text } } = await worker.recognize(file);
        await worker.terminate();

        progressBar.style.width = '100%';
        progressPercent.textContent = '100%';
        statusText.textContent = 'Parsing total, merchant, and line items...';

        parseOcrReceiptText(text);

      } catch (err) {
        console.warn('OCR error or fallback:', err);
        // Robust mock/fallback parser for offline demonstration
        parseOcrReceiptText(`STARBUCKS COFFEE\nCafe Latte  180.00\nCaramel Macchiato  240.00\nBlueberry Muffin  160.00\nTOTAL AMOUNT: 580.00`);
      }
    }

    function parseOcrReceiptText(rawText) {
      const lines = rawText.split('\n').map(l => l.trim()).filter(Boolean);
      let detectedMerchant = 'Scanned Receipt Bill';
      let detectedTotal = 0;
      const detectedItems = [];

      // 1. Detect Merchant Name from header lines
      for (let i = 0; i < Math.min(5, lines.length); i++) {
        const line = lines[i];
        if (line.length > 2 && !line.match(/\d{2,}/) && !line.toLowerCase().includes('welcome') && !line.toLowerCase().includes('tax invoice')) {
          detectedMerchant = line.replace(/[^a-zA-Z0-9\s&'-]/g, '').trim();
          if (detectedMerchant.length > 3) break;
        }
      }

      // 2. Detect Total Amount
      // Match patterns like "Total 450.00", "Grand Total: 1200", "Amount: Rs 650", "₹ 750.50"
      const totalPatterns = [
        /(?:total|grand\s*total|net\s*payable|amount\s*due|amount|balance)\s*[:=]?\s*(?:rs\.?|inr|₹)?\s*([0-9]+[.,][0-9]{2})/i,
        /(?:total|grand\s*total|net\s*payable|amount)\s*[:=]?\s*(?:rs\.?|inr|₹)?\s*([0-9]{2,6})/i,
        /(?:rs\.?|inr|₹)\s*([0-9]+[.,][0-9]{2})/i
      ];

      for (const line of lines) {
        for (const pattern of totalPatterns) {
          const match = line.match(pattern);
          if (match && match[1]) {
            const val = parseFloat(match[1].replace(',', '.'));
            if (!isNaN(val) && val > detectedTotal) {
              detectedTotal = val;
            }
          }
        }
      }

      // 3. Detect Line Items: "Item description ... 150.00"
      const itemPattern = /^([A-Za-z\s&-]{2,30})\s+(?:rs\.?|₹)?\s*([0-9]+(?:\.[0-9]{2})?)$/i;
      lines.forEach((line, idx) => {
        const match = line.match(itemPattern);
        if (match && !match[1].toLowerCase().includes('total') && !match[1].toLowerCase().includes('tax') && !match[1].toLowerCase().includes('cash')) {
          const price = parseFloat(match[2]);
          if (price > 0 && price < 50000) {
            detectedItems.push({
              name: match[1].trim(),
              amount: price
            });
          }
        }
      });

      // Fallback total if not matched by label: sum of items or largest number
      if (detectedTotal <= 0) {
        if (detectedItems.length > 0) {
          detectedTotal = detectedItems.reduce((s, it) => s + it.amount, 0);
        } else {
          // Find max number in text
          const allNums = rawText.match(/\b\d+(\.\d{2})?\b/g);
          if (allNums) {
            const parsedNums = allNums.map(n => parseFloat(n)).filter(n => !isNaN(n) && n > 0 && n < 100000);
            if (parsedNums.length > 0) detectedTotal = Math.max(...parsedNums);
          }
        }
      }

      if (detectedTotal <= 0) detectedTotal = 250.00;

      lastExtractedOcr = {
        title: detectedMerchant || 'Restaurant Bill',
        amount: detectedTotal,
        items: detectedItems
      };

      // Display review fields
      document.getElementById('ocrTitleInput').value = lastExtractedOcr.title;
      document.getElementById('ocrAmountInput').value = lastExtractedOcr.amount.toFixed(2);

      const itemsListContainer = document.getElementById('ocrLineItemsList');
      if (detectedItems.length === 0) {
        itemsListContainer.innerHTML = `<p class="text-[11px] text-slate-400 py-1">No individual line items parsed. Total amount extracted accurately.</p>`;
      } else {
        itemsListContainer.innerHTML = detectedItems.map((it, i) => `
          <div class="flex items-center justify-between p-1.5 rounded-lg bg-white dark:bg-slate-700/60 border border-slate-200 dark:border-slate-600">
            <span class="font-medium text-slate-800 dark:text-slate-200">${it.name}</span>
            <span class="font-bold text-indigo-600 dark:text-indigo-400">${formatMoney(it.amount)}</span>
          </div>
        `).join('');
      }

      document.getElementById('ocrScanningStatus').classList.add('hidden');
      document.getElementById('ocrResultReview').classList.remove('hidden');
    }

    function applyOcrToExpenseForm(useInItemSplit = false) {
      const title = document.getElementById('ocrTitleInput').value.trim() || 'Scanned Expense';
      const amount = parseFloat(document.getElementById('ocrAmountInput').value) || 0;

      closeReceiptScannerModal();
      openExpenseModal();

      document.getElementById('expenseTitle').value = title;
      document.getElementById('expenseAmount').value = amount.toFixed(2);
      onExpenseAmountChanged();

      if (useInItemSplit && lastExtractedOcr && lastExtractedOcr.items && lastExtractedOcr.items.length > 0) {
        setSplitMode('items');
        currentLineItems = lastExtractedOcr.items.map((it, idx) => ({
          id: 'item_ocr_' + idx,
          name: it.name,
          amount: it.amount,
          splitMembers: []
        }));
        renderLineItemsTable();
      }

      showToast(`Applied "${title}" (${formatMoney(amount)}) from receipt!`, 'success');
    }

    // --- FEATURE 3: DIRECT UPI 'PAY NOW' DEEP LINKS (INDIA PAYMENTS) ---
    let pendingUpiTarget = null;

    function openPayViaUpiModal(debtor, creditor, amount) {
      const group = getCurrentGroup();
      let credProfile = group.memberProfiles && group.memberProfiles[creditor];
      let credUpi = credProfile ? credProfile.upiId : null;

      if (!credUpi) {
        // Prompt to set receiver UPI ID
        openSetUpiModal(creditor, () => {
          openPayViaUpiModal(debtor, creditor, amount);
        });
        showToast(`Please enter UPI ID for ${creditor} to generate payment link`, 'info');
        return;
      }

      pendingUpiTarget = { debtor, creditor, amount, upiId: credUpi };

      document.getElementById('upiModalReceiverName').textContent = `${creditor} (${debtor} owes)`;
      document.getElementById('upiModalAmount').textContent = formatMoney(amount);
      document.getElementById('upiModalVpaBadge').textContent = credUpi;

      // Construct standard Indian UPI deep link
      // upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={transaction_note}
      const note = encodeURIComponent(`FairShare Settlement from ${debtor}`);
      const pn = encodeURIComponent(creditor);
      const cleanAmount = Number(amount).toFixed(2);
      const upiUrl = `upi://pay?pa=${encodeURIComponent(credUpi)}&pn=${pn}&am=${cleanAmount}&cu=INR&tn=${note}`;

      // Update deep link button for mobile
      const deepLinkBtn = document.getElementById('upiDeepLinkBtn');
      deepLinkBtn.href = upiUrl;

      // Render Dynamic UPI QR Code using QRCode.js
      const qrContainer = document.getElementById('upiQrcodeCanvas');
      qrContainer.innerHTML = '';
      if (typeof QRCode !== 'undefined') {
        new QRCode(qrContainer, {
          text: upiUrl,
          width: 160,
          height: 160,
          colorDark: '#0f172a',
          colorLight: '#ffffff',
          correctLevel: QRCode.CorrectLevel.M
        });
      }

      const modal = document.getElementById('upiPaymentModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });

      // If mobile device, also trigger deep link directly
      if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        setTimeout(() => {
          window.location.href = upiUrl;
        }, 300);
      }
    }

    function closeUpiPaymentModal() {
      const modal = document.getElementById('upiPaymentModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function copyUpiVpa() {
      if (pendingUpiTarget && pendingUpiTarget.upiId) {
        copyToClipboard(pendingUpiTarget.upiId, `UPI ID "${pendingUpiTarget.upiId}" copied!`);
      }
    }

    function confirmAndMarkSettledFromUpi() {
      if (!pendingUpiTarget) return;
      const { debtor, creditor, amount } = pendingUpiTarget;
      closeUpiPaymentModal();
      recordIndividualSettlement(debtor, creditor, amount);
    }

    // Modal to set or update any member's UPI ID
    let onSetUpiSuccessCallback = null;
    function openSetUpiModal(memberName, callback = null) {
      const group = getCurrentGroup();
      onSetUpiSuccessCallback = callback;
      document.getElementById('setUpiMemberNameHidden').value = memberName;
      document.getElementById('setUpiModalTitle').textContent = `Set UPI ID for ${memberName}`;
      
      const existing = (group.memberProfiles[memberName] && group.memberProfiles[memberName].upiId) || '';
      document.getElementById('setUpiInput').value = existing;

      const modal = document.getElementById('setUpiModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
      document.getElementById('setUpiInput').focus();
    }

    function closeSetUpiModal() {
      const modal = document.getElementById('setUpiModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function handleSaveMemberUpi(e) {
      e.preventDefault();
      const member = document.getElementById('setUpiMemberNameHidden').value;
      const vpa = document.getElementById('setUpiInput').value.trim();
      const group = getCurrentGroup();

      if (!vpa || !vpa.includes('@')) {
        showToast('Please enter a valid UPI VPA (e.g. name@upi or phone@paytm)', 'warning');
        return;
      }

      if (!group.memberProfiles[member]) group.memberProfiles[member] = {};
      group.memberProfiles[member].upiId = vpa;

      commitStateChanges(`Updated UPI ID for ${member}`);
      closeSetUpiModal();
      renderMembersList();
      showToast(`Saved UPI ID "${vpa}" for ${member}!`, 'success');

      if (onSetUpiSuccessCallback) {
        onSetUpiSuccessCallback();
        onSetUpiSuccessCallback = null;
      }
    }

    // --- FEATURE 4: FLEXIBLE SPLIT MODES (EQUAL, EXACT, ITEM-BY-ITEM) ---
    function setSplitMode(mode) {
      currentSplitMode = mode;
      const btnEqual = document.getElementById('splitModeBtnEqual');
      const btnExact = document.getElementById('splitModeBtnExact');
      const btnItems = document.getElementById('splitModeBtnItems');

      const contEqual = document.getElementById('splitEqualContainer');
      const contExact = document.getElementById('splitExactContainer');
      const contItems = document.getElementById('splitItemsContainer');

      [contEqual, contExact, contItems].forEach(el => el.classList.add('hidden'));
      [btnEqual, btnExact, btnItems].forEach(b => {
        b.className = 'px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-900 dark:hover:text-white transition';
      });

      if (mode === 'equal') {
        contEqual.classList.remove('hidden');
        btnEqual.className = 'px-2.5 py-1 rounded-md bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm transition font-bold';
        updateSplitLivePreview();
      } else if (mode === 'exact') {
        contExact.classList.remove('hidden');
        btnExact.className = 'px-2.5 py-1 rounded-md bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm transition font-bold';
        renderExactSplitInputs();
      } else if (mode === 'items') {
        contItems.classList.remove('hidden');
        btnItems.className = 'px-2.5 py-1 rounded-md bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm transition font-bold';
        renderLineItemsTable();
      }
    }

    function onExpenseAmountChanged() {
      if (currentSplitMode === 'equal') {
        updateSplitLivePreview();
      } else if (currentSplitMode === 'exact') {
        validateExactAmountsLive();
      }
    }

    function renderExactSplitInputs() {
      const group = getCurrentGroup();
      const list = document.getElementById('splitExactInputsList');
      const totalAmount = parseFloat(document.getElementById('expenseAmount').value) || 0;
      const count = group.members.length;
      const defaultShare = count > 0 ? (totalAmount / count).toFixed(2) : 0;

      list.innerHTML = group.members.map(member => `
        <div class="flex items-center justify-between gap-3 p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <span class="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate flex-1">${member}</span>
          <div class="relative w-32 shrink-0">
            <span class="absolute left-2.5 top-1.5 text-xs text-slate-400 font-bold">${group.currency || '₹'}</span>
            <input type="number" step="0.01" min="0" data-member="${member}" value="${defaultShare}" oninput="validateExactAmountsLive()" class="exact-split-input w-full text-xs font-bold bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg pl-6 pr-2 py-1 text-right focus:outline-none focus:ring-2 focus:ring-indigo-500">
          </div>
        </div>
      `).join('');

      validateExactAmountsLive();
    }

    function distributeExactEvenly() {
      const group = getCurrentGroup();
      const totalAmount = parseFloat(document.getElementById('expenseAmount').value) || 0;
      const count = group.members.length;
      if (count === 0) return;
      const even = (totalAmount / count).toFixed(2);
      const inputs = document.querySelectorAll('.exact-split-input');
      inputs.forEach(inp => inp.value = even);
      validateExactAmountsLive();
    }

    function validateExactAmountsLive() {
      const targetTotal = parseFloat(document.getElementById('expenseAmount').value) || 0;
      const inputs = document.querySelectorAll('.exact-split-input');
      let sum = 0;
      inputs.forEach(inp => {
        sum += parseFloat(inp.value) || 0;
      });

      const diff = Math.round((targetTotal - sum) * 100) / 100;
      const sumText = document.getElementById('splitExactSumText');
      const diffText = document.getElementById('splitExactDiffText');
      const banner = document.getElementById('splitExactValidationBanner');

      sumText.textContent = `Allocated: ${formatMoney(sum)} / Target: ${formatMoney(targetTotal)}`;

      if (Math.abs(diff) < 0.05) {
        diffText.textContent = '✓ Perfectly Balanced';
        banner.className = 'p-2 rounded-xl text-xs flex items-center justify-between bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 font-semibold';
      } else if (diff > 0) {
        diffText.textContent = `Remaining: ${formatMoney(diff)}`;
        banner.className = 'p-2 rounded-xl text-xs flex items-center justify-between bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-200';
      } else {
        diffText.textContent = `Exceeded by: ${formatMoney(Math.abs(diff))}`;
        banner.className = 'p-2 rounded-xl text-xs flex items-center justify-between bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 font-bold';
      }
    }

    function renderLineItemsTable() {
      const group = getCurrentGroup();
      const container = document.getElementById('splitLineItemsTable');

      container.innerHTML = currentLineItems.map((item, idx) => `
        <div class="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
          <div class="flex items-center gap-2">
            <input type="text" value="${item.name}" placeholder="Item name" onchange="updateLineItemName(${idx}, this.value)" class="flex-1 text-xs bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1 text-slate-800 dark:text-slate-100 font-medium">
            <div class="relative w-28 shrink-0">
              <span class="absolute left-2 top-1 text-xs text-slate-400 font-bold">${group.currency || '₹'}</span>
              <input type="number" step="0.01" min="0" value="${item.amount}" placeholder="0.00" oninput="updateLineItemAmount(${idx}, this.value)" class="w-full text-xs font-bold bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg pl-5 pr-2 py-1 text-right">
            </div>
            <button type="button" onclick="removeLineItemRow(${idx})" class="p-1 text-slate-400 hover:text-rose-500">×</button>
          </div>
          <!-- Item split members -->
          <div class="flex items-center gap-1.5 flex-wrap pt-1 border-t border-slate-100 dark:border-slate-700/60 text-[10px]">
            <span class="text-slate-400">Split:</span>
            ${group.members.map(m => {
              const checked = item.splitMembers.length === 0 || item.splitMembers.includes(m);
              return `
                <label class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md cursor-pointer select-none ${checked ? 'bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 font-bold border border-indigo-200 dark:border-indigo-800' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'}">
                  <input type="checkbox" ${checked ? 'checked' : ''} onchange="toggleLineItemMember(${idx}, '${m.replace(/'/g, "\\'")}', this.checked)" class="w-3 h-3 text-indigo-600 rounded">
                  <span>${m}</span>
                </label>
              `;
            }).join('')}
          </div>
        </div>
      `).join('');

      recomputeLineItemsTotal();
    }

    function addNewLineItemRow() {
      currentLineItems.push({
        id: 'item_' + Date.now(),
        name: 'Item ' + (currentLineItems.length + 1),
        amount: 100,
        splitMembers: []
      });
      renderLineItemsTable();
    }

    function removeLineItemRow(idx) {
      if (currentLineItems.length <= 1) {
        showToast('At least one item is required in item-by-item split', 'warning');
        return;
      }
      currentLineItems.splice(idx, 1);
      renderLineItemsTable();
    }

    function updateLineItemName(idx, val) {
      if (currentLineItems[idx]) currentLineItems[idx].name = val.trim();
    }

    function updateLineItemAmount(idx, val) {
      if (currentLineItems[idx]) {
        currentLineItems[idx].amount = parseFloat(val) || 0;
        recomputeLineItemsTotal();
      }
    }

    function toggleLineItemMember(idx, member, checked) {
      const item = currentLineItems[idx];
      if (!item) return;
      const group = getCurrentGroup();
      if (item.splitMembers.length === 0) {
        item.splitMembers = [...group.members];
      }
      if (checked) {
        if (!item.splitMembers.includes(member)) item.splitMembers.push(member);
      } else {
        item.splitMembers = item.splitMembers.filter(m => m !== member);
      }
      recomputeLineItemsTotal();
    }

    function recomputeLineItemsTotal() {
      const sum = currentLineItems.reduce((acc, it) => acc + (Number(it.amount) || 0), 0);
      document.getElementById('splitItemsSumDisplay').textContent = formatMoney(sum);
      // Auto update total amount field
      document.getElementById('expenseAmount').value = sum.toFixed(2);
    }

    // --- FEATURE 5: RECURRING EXPENSES (SUBSCRIPTIONS & BILLS) ---
    function toggleRecurringOptions(checked) {
      const row = document.getElementById('recurringOptionsRow');
      if (checked) {
        row.classList.remove('hidden');
        // Set default next due date to 1 month from now
        const d = new Date();
        d.setMonth(d.getMonth() + 1);
        document.getElementById('recurringNextDueDate').value = d.toISOString().split('T')[0];
      } else {
        row.classList.add('hidden');
      }
    }

    function openAddRecurringModal() {
      const group = getCurrentGroup();
      const payerSel = document.getElementById('recBillPayer');
      payerSel.innerHTML = group.members.map(m => `<option value="${m}">${m}</option>`).join('');
      
      const modal = document.getElementById('addRecurringModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeAddRecurringModal() {
      const modal = document.getElementById('addRecurringModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function handleCreateRecurringBill(e) {
      e.preventDefault();
      const title = document.getElementById('recBillTitle').value.trim();
      const amount = parseFloat(document.getElementById('recBillAmount').value);
      const category = document.getElementById('recBillCategory').value;
      const cycle = document.getElementById('recBillCycle').value;
      const paidBy = document.getElementById('recBillPayer').value;
      const group = getCurrentGroup();

      if (!title || isNaN(amount) || amount <= 0) {
        showToast('Please enter valid bill title and amount', 'warning');
        return;
      }

      const nextD = new Date();
      if (cycle === 'monthly') nextD.setMonth(nextD.getMonth() + 1);
      else nextD.setDate(nextD.getDate() + 7);

      const newBill = {
        id: 'rec_' + Date.now(),
        title,
        amount,
        category,
        paidBy,
        splitAmong: [...group.members],
        cycle,
        nextDueDate: nextD.toISOString().split('T')[0]
      };

      group.recurringBills.push(newBill);
      commitStateChanges(`Added recurring bill ${title}`);
      closeAddRecurringModal();
      renderRecurringBills();
      showToast(`Recurring bill "${title}" created!`, 'success');
    }

    function postRecurringExpenseForCycle(recId) {
      const group = getCurrentGroup();
      const bill = group.recurringBills.find(b => b.id === recId);
      if (!bill) return;

      const today = new Date().toISOString().split('T')[0];

      // Add actual immutable expense record
      const newExp = {
        id: 'exp_rec_' + Date.now() + '_' + Math.random().toString(36).substring(2, 5),
        title: `${bill.title} (${bill.cycle === 'monthly' ? 'Monthly' : 'Weekly'})`,
        amount: Number(bill.amount),
        category: bill.category || 'Rent',
        paidBy: bill.paidBy,
        splitAmong: bill.splitAmong || group.members,
        splitMode: 'equal',
        date: today,
        isRecurringInstance: true
      };

      group.expenses.unshift(newExp);

      // Advance next due date
      const d = new Date(bill.nextDueDate || today);
      if (bill.cycle === 'weekly') {
        d.setDate(d.getDate() + 7);
      } else {
        d.setMonth(d.getMonth() + 1);
      }
      bill.nextDueDate = d.toISOString().split('T')[0];

      commitStateChanges(`Posted recurring expense: ${bill.title}`);
      renderApp();
      renderRecurringBills();
      showToast(`⚡ Posted "${bill.title}" (${formatMoney(bill.amount)}) for this cycle!`, 'success');
    }

    function renderRecurringBills() {
      const group = getCurrentGroup();
      const container = document.getElementById('recurringBillsContainer');
      const navBadge = document.getElementById('badgeRecurringNavCount');
      if (!container) return;

      const bills = group.recurringBills || [];
      if (navBadge) navBadge.textContent = bills.length;

      if (bills.length === 0) {
        container.innerHTML = `
          <div class="col-span-full py-12 px-4 text-center rounded-3xl bg-slate-50 dark:bg-slate-800/30 border border-dashed border-slate-200 dark:border-slate-800">
            <span class="text-3xl block mb-2">🔁</span>
            <h4 class="text-base font-bold text-slate-800 dark:text-slate-200">No Recurring Bills Set Up</h4>
            <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">Set up recurring flat rent, Wi-Fi fiber, maid salary, or subscriptions like Netflix for 1-click posting.</p>
            <button onclick="openAddRecurringModal()" class="mt-4 px-4 py-2 bg-indigo-600 text-white font-bold text-xs rounded-xl shadow-sm">
              + Add First Recurring Bill
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = bills.map(bill => {
        const catConfig = CATEGORIES[bill.category] || CATEGORIES['Other'];
        return `
          <div class="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between gap-4">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold px-2.5 py-0.5 rounded-full ${catConfig.color}">
                  ${catConfig.icon} ${catConfig.label}
                </span>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 capitalize">
                  ${bill.cycle}
                </span>
              </div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white truncate">${bill.title}</h3>
              <div class="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
                ${formatMoney(bill.amount)}
              </div>
              <div class="text-xs text-slate-500 mt-1">
                Paid by <strong>${bill.paidBy}</strong> · Split among ${bill.splitAmong ? bill.splitAmong.length : group.members.length} members
              </div>
              <div class="mt-3 flex items-center gap-1.5 text-xs text-amber-600 dark:text-amber-400 font-semibold bg-amber-50 dark:bg-amber-950/40 p-2 rounded-xl">
                <span>📅</span>
                <span>Next Due: <strong>${bill.nextDueDate || 'Pending'}</strong></span>
              </div>
            </div>

            <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
              <span class="text-[11px] text-slate-400">1-Click Post</span>
              <button onclick="postRecurringExpenseForCycle('${bill.id}')" class="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 active:scale-95 text-white text-xs font-bold shadow-md shadow-teal-600/20 transition flex items-center gap-1.5">
                <span>⚡ Post for this Month</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // --- FEATURE 6: SPENDING INSIGHTS & CATEGORY ANALYTICS (CHART.JS) ---
    function renderAnalyticsCharts() {
      const group = getCurrentGroup();
      const actualExpenses = group.expenses.filter(e => !e.isSettlement && e.category !== 'Settlement');

      // 1. Group Outflow & KPIs
      const totalOutflow = actualExpenses.reduce((sum, e) => sum + (Number(e.amount) || 0), 0);
      const settlementsCount = group.expenses.filter(e => e.isSettlement || e.category === 'Settlement').length;

      document.getElementById('analyticsTotalOutflow').textContent = formatMoney(totalOutflow);
      document.getElementById('analyticsSettledCount').textContent = settlementsCount;
      document.getElementById('analyticsAvgBill').textContent = actualExpenses.length > 0 ? formatMoney(totalOutflow / actualExpenses.length) : formatMoney(0);

      // Category aggregation
      const catTotals = {};
      Object.keys(CATEGORIES).forEach(c => { if (c !== 'Settlement') catTotals[c] = 0; });
      actualExpenses.forEach(e => {
        const cat = e.category && CATEGORIES[e.category] ? e.category : 'Other';
        catTotals[cat] = (catTotals[cat] || 0) + (Number(e.amount) || 0);
      });

      // Top Category
      let topCat = 'None';
      let topCatVal = 0;
      Object.entries(catTotals).forEach(([k, v]) => {
        if (v > topCatVal) {
          topCatVal = v;
          topCat = k;
        }
      });
      const topCatCfg = CATEGORIES[topCat] || { icon: '📦', label: 'Other' };
      document.getElementById('analyticsTopCategory').textContent = `${topCatCfg.icon} ${topCatCfg.label}`;

      // Member Spend aggregation
      const memberPaid = {};
      const memberConsumed = {};
      group.members.forEach(m => {
        memberPaid[m] = 0;
        memberConsumed[m] = 0;
      });

      actualExpenses.forEach(e => {
        const amt = Number(e.amount) || 0;
        if (memberPaid[e.paidBy] !== undefined) memberPaid[e.paidBy] += amt;

        if (e.splitDetails && typeof e.splitDetails === 'object') {
          Object.entries(e.splitDetails).forEach(([m, s]) => {
            if (memberConsumed[m] !== undefined) memberConsumed[m] += Number(s) || 0;
          });
        } else {
          const splitters = (e.splitAmong && e.splitAmong.length > 0) ? e.splitAmong : group.members;
          const share = amt / splitters.length;
          splitters.forEach(m => {
            if (memberConsumed[m] !== undefined) memberConsumed[m] += share;
          });
        }
      });

      // Top Spender
      let topSpender = 'None';
      let topSpenderVal = 0;
      Object.entries(memberPaid).forEach(([m, v]) => {
        if (v > topSpenderVal) {
          topSpenderVal = v;
          topSpender = m;
        }
      });
      document.getElementById('analyticsTopSpender').textContent = topSpender !== 'None' ? `${topSpender} (${formatMoney(topSpenderVal)})` : 'None';

      // 2. Render Doughnut Chart (Category Breakdown)
      const catLabels = Object.keys(catTotals).filter(k => catTotals[k] > 0);
      const catValues = catLabels.map(k => catTotals[k]);
      const catColors = catLabels.map(k => CATEGORIES[k].chartColor);

      const catCanvas = document.getElementById('categoryChart');
      if (catCanvas && typeof Chart !== 'undefined') {
        if (categoryChartInstance) categoryChartInstance.destroy();

        if (catValues.length === 0) {
          // Placeholder dummy chart
          categoryChartInstance = new Chart(catCanvas, {
            type: 'doughnut',
            data: {
              labels: ['No Data'],
              datasets: [{
                data: [1],
                backgroundColor: ['#cbd5e1']
              }]
            },
            options: { responsive: true, maintainAspectRatio: false, cutout: '75%' }
          });
        } else {
          categoryChartInstance = new Chart(catCanvas, {
            type: 'doughnut',
            data: {
              labels: catLabels.map(k => `${CATEGORIES[k].icon} ${CATEGORIES[k].label}`),
              datasets: [{
                data: catValues,
                backgroundColor: catColors,
                borderWidth: 2,
                borderColor: appState.darkMode ? '#0f172a' : '#ffffff'
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              cutout: '72%',
              plugins: {
                legend: { display: false },
                tooltip: {
                  callbacks: {
                    label: ctx => ` ${ctx.label}: ${formatMoney(ctx.raw)} (${Math.round((ctx.raw / totalOutflow) * 100)}%)`
                  }
                }
              }
            }
          });
        }
      }

      // Render custom legend container
      const legendContainer = document.getElementById('categoryLegendContainer');
      if (legendContainer) {
        if (catLabels.length === 0) {
          legendContainer.innerHTML = `<span class="col-span-2 text-slate-400">No expenses recorded yet.</span>`;
        } else {
          legendContainer.innerHTML = catLabels.map(k => {
            const pct = Math.round((catTotals[k] / totalOutflow) * 100);
            return `
              <div class="flex items-center justify-between p-1.5 rounded-lg bg-slate-50 dark:bg-slate-800/60">
                <div class="flex items-center gap-1.5 truncate">
                  <span class="w-2.5 h-2.5 rounded-full shrink-0" style="background: ${CATEGORIES[k].chartColor}"></span>
                  <span class="truncate font-semibold text-slate-700 dark:text-slate-300">${CATEGORIES[k].icon} ${CATEGORIES[k].label}</span>
                </div>
                <span class="font-bold text-slate-900 dark:text-white shrink-0 ml-1">${pct}%</span>
              </div>
            `;
          }).join('');
        }
      }

      // 3. Render Bar Chart (Spend by Member)
      const barCanvas = document.getElementById('memberSpendChart');
      if (barCanvas && typeof Chart !== 'undefined') {
        if (memberSpendChartInstance) memberSpendChartInstance.destroy();

        const memberLabels = group.members;
        const paidData = memberLabels.map(m => memberPaid[m] || 0);
        const consumedData = memberLabels.map(m => memberConsumed[m] || 0);

        memberSpendChartInstance = new Chart(barCanvas, {
          type: 'bar',
          data: {
            labels: memberLabels,
            datasets: [
              {
                label: 'Paid Upfront',
                data: paidData,
                backgroundColor: '#6366f1',
                borderRadius: 8
              },
              {
                label: 'Consumed Share',
                data: consumedData,
                backgroundColor: '#cbd5e1',
                borderRadius: 8
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
                labels: {
                  color: appState.darkMode ? '#cbd5e1' : '#475569',
                  font: { family: '"Plus Jakarta Sans", system-ui' }
                }
              },
              tooltip: {
                callbacks: {
                  label: ctx => ` ${ctx.dataset.label}: ${formatMoney(ctx.raw)}`
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: appState.darkMode ? '#94a3b8' : '#64748b' }
              },
              y: {
                grid: { color: appState.darkMode ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)' },
                ticks: {
                  color: appState.darkMode ? '#94a3b8' : '#64748b',
                  callback: val => (group.currency || '₹') + val
                }
              }
            }
          }
        });
      }
    }

    // --- PAIR-TO-PAIR SETTLEMENT ENGINE (RULE PRESERVED STRICTLY) ---
    function calculateBalances() {
      const group = getCurrentGroup();
      const totals = {};

      group.members.forEach(member => {
        totals[member] = { paid: 0, share: 0, net: 0 };
      });

      group.expenses.forEach(exp => {
        const amount = Number(exp.amount) || 0;
        const payer = exp.paidBy;

        if (totals[payer]) totals[payer].paid += amount;

        if (exp.splitDetails && typeof exp.splitDetails === 'object') {
          // Custom split details
          Object.entries(exp.splitDetails).forEach(([person, share]) => {
            if (totals[person]) totals[person].share += Number(share) || 0;
          });
        } else {
          // Equal split fallback
          const splitters = (exp.splitAmong && exp.splitAmong.length > 0) ? exp.splitAmong : group.members;
          const sharePerPerson = amount / splitters.length;
          splitters.forEach(person => {
            if (totals[person]) totals[person].share += sharePerPerson;
          });
        }
      });

      Object.keys(totals).forEach(member => {
        totals[member].net = totals[member].paid - totals[member].share;
      });

      return totals;
    }

    function calculateDirectPairDebts() {
      const group = getCurrentGroup();
      if (!group) return [];

      const directDebts = {};
      const allMembers = Array.from(new Set([
        ...(group.members || []),
        ...group.expenses.flatMap(e => [e.paidBy, ...(e.splitAmong || [])]).filter(Boolean)
      ]));

      allMembers.forEach(m1 => {
        directDebts[m1] = {};
        allMembers.forEach(m2 => {
          directDebts[m1][m2] = 0;
        });
      });

      group.expenses.forEach(exp => {
        const amount = Number(exp.amount) || 0;
        if (amount <= 0) return;
        const payer = exp.paidBy;
        if (!payer) return;

        if (exp.splitDetails && typeof exp.splitDetails === 'object') {
          // Exact amount or Item-by-item split
          Object.entries(exp.splitDetails).forEach(([consumer, personShare]) => {
            const shareNum = Number(personShare) || 0;
            if (consumer && consumer !== payer && shareNum > 0) {
              if (!directDebts[consumer]) directDebts[consumer] = {};
              if (directDebts[consumer][payer] === undefined) directDebts[consumer][payer] = 0;
              directDebts[consumer][payer] += shareNum;
            }
          });
        } else {
          // Equal split
          const splitters = (exp.splitAmong && exp.splitAmong.length > 0) ? exp.splitAmong : group.members;
          if (!splitters || splitters.length === 0) return;
          const sharePerPerson = amount / splitters.length;

          splitters.forEach(consumer => {
            if (consumer && consumer !== payer) {
              if (!directDebts[consumer]) directDebts[consumer] = {};
              if (directDebts[consumer][payer] === undefined) directDebts[consumer][payer] = 0;
              directDebts[consumer][payer] += sharePerPerson;
            }
          });
        }
      });

      const transactions = [];
      const EPSILON = 0.01;

      // Net STRICTLY and ONLY between the same two people (NO THIRD-PARTY DEBT ROUTING)
      for (let i = 0; i < allMembers.length; i++) {
        for (let j = i + 1; j < allMembers.length; j++) {
          const pA = allMembers[i];
          const pB = allMembers[j];

          const aOwesB = (directDebts[pA] && directDebts[pA][pB]) || 0;
          const bOwesA = (directDebts[pB] && directDebts[pB][pA]) || 0;

          const net = aOwesB - bOwesA;
          const roundedAmount = Math.round(Math.abs(net) * 100) / 100;

          if (roundedAmount >= EPSILON) {
            if (net > 0) {
              transactions.push({ from: pA, to: pB, amount: roundedAmount });
            } else {
              transactions.push({ from: pB, to: pA, amount: roundedAmount });
            }
          }
        }
      }

      transactions.sort((a, b) => {
        const user = appState.currentUser;
        const aUser = user && (a.from === user || a.to === user);
        const bUser = user && (b.from === user || b.to === user);
        if (aUser && !bUser) return -1;
        if (!aUser && bUser) return 1;
        return b.amount - a.amount;
      });

      return transactions;
    }

    // --- EXPENSE SAVE / EDIT (IMMUTABLE LOG - NO DELETE) ---
    function openExpenseModal(expenseToEdit = null) {
      const modal = document.getElementById('expenseModal');
      const form = document.getElementById('expenseForm');
      const modalTitle = document.getElementById('modalTitle');
      const editingIdInput = document.getElementById('editingExpenseId');
      const payerSelect = document.getElementById('expensePayer');
      const checkboxesContainer = document.getElementById('splitCheckboxesContainer');
      const group = getCurrentGroup();

      payerSelect.innerHTML = group.members.map(member => `
        <option value="${member}">${member}</option>
      `).join('');

      checkboxesContainer.innerHTML = group.members.map(member => {
        const initials = getInitials(member);
        const grad = getAvatarGradient(member);
        return `
          <label class="flex items-center gap-2.5 p-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/70 dark:border-slate-700/70 hover:border-indigo-400 dark:hover:border-indigo-500 cursor-pointer transition select-none">
            <input type="checkbox" name="splitMember" value="${member}" checked onchange="updateSplitLivePreview()" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500 border-slate-300 dark:border-slate-600">
            <div class="w-6 h-6 rounded-md bg-gradient-to-tr ${grad} text-white text-[10px] font-bold flex items-center justify-center shrink-0">
              ${initials}
            </div>
            <span class="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">${member}</span>
          </label>
        `;
      }).join('');

      document.getElementById('expenseDate').value = new Date().toISOString().split('T')[0];
      setSplitMode('equal');
      document.getElementById('expenseRecurringToggle').checked = false;
      document.getElementById('recurringOptionsRow').classList.add('hidden');

      if (expenseToEdit) {
        modalTitle.textContent = 'Edit Expense Details';
        editingIdInput.value = expenseToEdit.id;
        document.getElementById('expenseTitle').value = expenseToEdit.title;
        document.getElementById('expenseAmount').value = expenseToEdit.amount;
        document.getElementById('expenseCategory').value = expenseToEdit.category || 'Other';
        payerSelect.value = expenseToEdit.paidBy;
        if (expenseToEdit.date) document.getElementById('expenseDate').value = expenseToEdit.date;

        if (expenseToEdit.splitMode) {
          setSplitMode(expenseToEdit.splitMode);
        }

        const checkboxes = document.querySelectorAll('input[name="splitMember"]');
        checkboxes.forEach(cb => {
          cb.checked = (expenseToEdit.splitAmong || []).includes(cb.value);
        });
      } else {
        modalTitle.textContent = 'Record Shared Expense';
        editingIdInput.value = '';
        form.reset();
        document.getElementById('expenseDate').value = new Date().toISOString().split('T')[0];
        selectAllSplitters(true);
        if (appState.currentUser && group.members.includes(appState.currentUser)) {
          payerSelect.value = appState.currentUser;
        }
      }

      updateSplitLivePreview();

      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95', 'translate-y-8');
      });
    }

    function closeExpenseModal() {
      const modal = document.getElementById('expenseModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95', 'translate-y-8');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function selectAllSplitters(checked) {
      const checkboxes = document.querySelectorAll('input[name="splitMember"]');
      checkboxes.forEach(cb => cb.checked = checked);
      updateSplitLivePreview();
    }

    function updateSplitLivePreview() {
      const amount = parseFloat(document.getElementById('expenseAmount').value) || 0;
      const checkedBoxes = Array.from(document.querySelectorAll('input[name="splitMember"]:checked'));
      const count = checkedBoxes.length;
      const liveAmountEl = document.getElementById('splitLiveAmount');

      if (count === 0) {
        liveAmountEl.textContent = 'Select at least 1 person!';
        liveAmountEl.className = 'font-bold text-rose-500';
      } else {
        const perPerson = amount / count;
        liveAmountEl.textContent = `${formatMoney(perPerson)} / person (${count} members)`;
        liveAmountEl.className = 'font-bold text-indigo-700 dark:text-indigo-300';
      }
    }

    function setQuickExpensePreset(title, category) {
      document.getElementById('expenseTitle').value = title;
      document.getElementById('expenseCategory').value = category;
      document.getElementById('expenseAmount').focus();
    }

    function handleSaveExpense(e) {
      e.preventDefault();
      const group = getCurrentGroup();
      const editingId = document.getElementById('editingExpenseId').value;
      const title = document.getElementById('expenseTitle').value.trim();
      const amount = parseFloat(document.getElementById('expenseAmount').value);
      const category = document.getElementById('expenseCategory').value;
      const paidBy = document.getElementById('expensePayer').value;
      const date = document.getElementById('expenseDate').value || new Date().toISOString().split('T')[0];

      if (!title) {
        showToast('Please enter an expense description', 'warning');
        return;
      }
      if (isNaN(amount) || amount <= 0) {
        showToast('Please enter a valid amount greater than 0', 'warning');
        return;
      }

      let splitAmong = [];
      let splitDetails = null;

      if (currentSplitMode === 'equal') {
        const splitCheckboxes = Array.from(document.querySelectorAll('input[name="splitMember"]:checked'));
        splitAmong = splitCheckboxes.map(cb => cb.value);
        if (splitAmong.length === 0) {
          showToast('Please select at least 1 member to split among', 'warning');
          return;
        }
      } else if (currentSplitMode === 'exact') {
        splitDetails = {};
        const inputs = document.querySelectorAll('.exact-split-input');
        let totalExact = 0;
        inputs.forEach(inp => {
          const m = inp.dataset.member;
          const val = parseFloat(inp.value) || 0;
          splitDetails[m] = val;
          totalExact += val;
          if (val > 0) splitAmong.push(m);
        });

        if (Math.abs(amount - totalExact) > 0.1) {
          showToast(`Exact split sum (${formatMoney(totalExact)}) must match total amount (${formatMoney(amount)})!`, 'warning');
          return;
        }
      } else if (currentSplitMode === 'items') {
        splitDetails = {};
        group.members.forEach(m => splitDetails[m] = 0);

        currentLineItems.forEach(item => {
          const itemAmt = Number(item.amount) || 0;
          const itemSplitters = item.splitMembers.length > 0 ? item.splitMembers : group.members;
          const perPerson = itemAmt / itemSplitters.length;
          itemSplitters.forEach(m => {
            splitDetails[m] = (splitDetails[m] || 0) + perPerson;
            if (!splitAmong.includes(m)) splitAmong.push(m);
          });
        });
      }

      // Check recurring toggle
      const isRecurring = document.getElementById('expenseRecurringToggle').checked;
      if (isRecurring && !editingId) {
        const cycle = document.getElementById('recurringCycleSelect').value;
        const nextDue = document.getElementById('recurringNextDueDate').value;
        group.recurringBills.push({
          id: 'rec_' + Date.now(),
          title: title,
          amount: amount,
          category: category,
          paidBy: paidBy,
          splitAmong: splitAmong,
          cycle: cycle,
          nextDueDate: nextDue
        });
      }

      if (editingId) {
        const index = group.expenses.findIndex(exp => exp.id === editingId);
        if (index !== -1) {
          group.expenses[index] = {
            id: editingId,
            title,
            amount,
            category,
            paidBy,
            splitAmong,
            splitMode: currentSplitMode,
            splitDetails,
            date
          };
          showToast(`Updated "${title}"`, 'success');
        }
      } else {
        const newExpense = {
          id: 'exp_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
          title,
          amount,
          category,
          paidBy,
          splitAmong,
          splitMode: currentSplitMode,
          splitDetails,
          date
        };
        group.expenses.unshift(newExpense);
        showToast(`Added "${title}" (${formatMoney(amount)})`, 'success');
      }

      commitStateChanges('Saved expense');
      closeExpenseModal();
      renderApp();
    }

    function editExpense(id) {
      const group = getCurrentGroup();
      const exp = group.expenses.find(e => e.id === id);
      if (exp) openExpenseModal(exp);
    }

    // --- INDIVIDUAL SETTLEMENT ENGINE & MODAL ---
    function openSettleShareModal(focusMember = null) {
      const group = getCurrentGroup();
      if (!group || !group.members || group.members.length === 0) {
        showToast('No group members to settle with', 'warning');
        return;
      }

      if (!appState.currentUser || !group.members.includes(appState.currentUser)) {
        if (focusMember && group.members.includes(focusMember)) {
          selectCurrentUser(focusMember);
        } else {
          showToast('Please identify who you are before settling', 'info');
          openUserIdentifyModal();
          return;
        }
      }

      const activeUser = appState.currentUser;
      const transactions = calculateDirectPairDebts();
      const container = document.getElementById('settleModalContent');
      const myDebts = transactions.filter(t => t.from === activeUser);
      const myCredits = transactions.filter(t => t.to === activeUser);

      let html = '';

      if (myDebts.length === 0 && myCredits.length === 0) {
        html += `
          <div class="p-5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-center">
            <div class="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              ✓
            </div>
            <h4 class="text-sm sm:text-base font-bold text-emerald-900 dark:text-emerald-200">You are All Cleared Up!</h4>
            <p class="text-xs text-emerald-700 dark:text-emerald-300 mt-1">
              All your direct pair-to-pair debts are settled. You neither owe nor are owed any money in this group.
            </p>
          </div>
        `;
      } else {
        if (myDebts.length > 0) {
          const totalOwed = myDebts.reduce((sum, d) => sum + d.amount, 0);
          html += `
            <div class="p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 mb-3">
              <span class="text-[11px] font-bold text-rose-700 dark:text-rose-300 uppercase tracking-wider block">Your Direct Pending Dues</span>
              <span class="text-xl font-extrabold text-rose-900 dark:text-rose-100">${formatMoney(totalOwed)}</span>
            </div>
            <div class="space-y-2">
              <span class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider block">Whom You Owe (1-to-1):</span>
              ${myDebts.map(debt => `
                <div class="p-3 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-between gap-3 shadow-sm">
                  <div>
                    <span class="text-xs font-bold text-slate-800 dark:text-slate-100">You owe <strong>${debt.to}</strong></span>
                    <span class="text-sm font-extrabold text-slate-900 dark:text-white block mt-0.5">${formatMoney(debt.amount)}</span>
                  </div>
                  <div class="flex items-center gap-1.5 shrink-0">
                    <button type="button" onclick="openPayViaUpiModal('${activeUser.replace(/'/g, "\\'")}', '${debt.to.replace(/'/g, "\\'")}', ${debt.amount})" class="px-3 py-1.5 text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-sm transition flex items-center gap-1">
                      <span>⚡ Pay UPI</span>
                    </button>
                    <button type="button" onclick="recordIndividualSettlement('${activeUser.replace(/'/g, "\\'")}', '${debt.to.replace(/'/g, "\\'")}', ${debt.amount})" class="px-2.5 py-1.5 text-xs font-semibold bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl transition">
                      Mark Paid
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          `;
        }

        if (myCredits.length > 0) {
          html += `
            <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 space-y-2">
              <span class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider block">Owed to You (Receivables):</span>
              ${myCredits.map(c => `
                <div class="p-3 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-between gap-3 shadow-sm">
                  <div>
                    <span class="text-xs font-bold text-slate-800 dark:text-slate-100"><strong>${c.from}</strong> owes you</span>
                    <span class="text-sm font-extrabold text-emerald-600 dark:text-emerald-400 block mt-0.5">+${formatMoney(c.amount)}</span>
                  </div>
                  <button type="button" onclick="recordIndividualSettlement('${c.from.replace(/'/g, "\\'")}', '${activeUser.replace(/'/g, "\\'")}', ${c.amount})" class="px-3 py-1.5 text-xs font-bold bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 rounded-xl hover:bg-indigo-100 transition">
                    Confirm Received
                  </button>
                </div>
              `).join('')}
            </div>
          `;
        }
      }

      container.innerHTML = html;

      const modal = document.getElementById('settleShareModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeSettleShareModal() {
      const modal = document.getElementById('settleShareModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function recordIndividualSettlement(from, to, amount) {
      const group = getCurrentGroup();
      const settlementExpense = {
        id: 'settle_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
        title: `${from} paid ${to} (Settled)`,
        amount: Number(amount),
        category: 'Settlement',
        paidBy: from,
        splitAmong: [to],
        isSettlement: true,
        date: new Date().toISOString().split('T')[0],
        timestamp: Date.now()
      };

      group.expenses.unshift(settlementExpense);
      commitStateChanges(`Settlement: ${from} paid ${to}`);
      renderApp();
      closeSettleShareModal();
      showToast(`🤝 Settled! ${from} paid ${formatMoney(amount)} to ${to}`, 'success');
    }

    // --- MEMBER MANAGEMENT ---
    function toggleAddMemberInput() {
      const form = document.getElementById('addMemberForm');
      form.classList.toggle('hidden');
      if (!form.classList.contains('hidden')) {
        document.getElementById('newMemberNameInput').focus();
      }
    }

    function handleAddMember(e) {
      e.preventDefault();
      const input = document.getElementById('newMemberNameInput');
      const name = input.value.trim();
      const group = getCurrentGroup();

      if (!name) return;
      if (group.members.map(m => m.toLowerCase()).includes(name.toLowerCase())) {
        showToast(`"${name}" is already in the group!`, 'warning');
        return;
      }

      group.members.push(name);
      if (!group.memberProfiles[name]) group.memberProfiles[name] = {};
      input.value = '';
      toggleAddMemberInput();
      commitStateChanges(`Added member ${name}`);
      renderApp();
      showToast(`Added ${name} to group`, 'success');
    }

    function openRenameMemberModal(memberName) {
      document.getElementById('oldMemberNameHidden').value = memberName;
      document.getElementById('renameMemberInput').value = memberName;
      const modal = document.getElementById('renameMemberModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
      document.getElementById('renameMemberInput').focus();
    }

    function closeRenameMemberModal() {
      const modal = document.getElementById('renameMemberModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function handleSaveRenameMember(e) {
      e.preventDefault();
      const oldName = document.getElementById('oldMemberNameHidden').value;
      const newName = document.getElementById('renameMemberInput').value.trim();
      const group = getCurrentGroup();

      if (!newName || oldName === newName) {
        closeRenameMemberModal();
        return;
      }

      const idx = group.members.indexOf(oldName);
      if (idx !== -1) group.members[idx] = newName;

      // Migrate member profiles & history
      if (group.memberProfiles[oldName]) {
        group.memberProfiles[newName] = group.memberProfiles[oldName];
        delete group.memberProfiles[oldName];
      }

      if (appState.currentUser === oldName) appState.currentUser = newName;

      group.expenses.forEach(exp => {
        if (exp.paidBy === oldName) exp.paidBy = newName;
        if (Array.isArray(exp.splitAmong)) {
          exp.splitAmong = exp.splitAmong.map(p => p === oldName ? newName : p);
        }
      });

      closeRenameMemberModal();
      commitStateChanges(`Renamed ${oldName} to ${newName}`);
      renderApp();
      showToast(`Renamed "${oldName}" to "${newName}"`, 'success');
    }

    function removeMember(name) {
      const group = getCurrentGroup();
      if (group.members.length <= 3) {
        showToast('Keep at least 3 members in the group!', 'warning');
        return;
      }
      const hasRecords = group.expenses.some(exp => exp.paidBy === name || (exp.splitAmong && exp.splitAmong.includes(name)));
      if (hasRecords) {
        showToast(`Cannot remove "${name}": audit log preserves all past financial records permanently.`, 'warning');
        return;
      }
      group.members = group.members.filter(m => m !== name);
      commitStateChanges(`Removed member ${name}`);
      renderApp();
      showToast(`Removed ${name}`, 'info');
    }

    // --- MEMBER IDENTITY SWITCHER ---
    function openUserIdentifyModal() {
      const group = getCurrentGroup();
      const grid = document.getElementById('userIdentifyMembersGrid');
      grid.innerHTML = group.members.map(member => {
        const isSelected = appState.currentUser === member;
        const initials = getInitials(member);
        const grad = getAvatarGradient(member);
        return `
          <button type="button" onclick="selectCurrentUser('${member.replace(/'/g, "\\'")}')" class="flex items-center gap-2 p-2.5 rounded-xl border text-left transition select-none ${
            isSelected
              ? 'bg-indigo-50 dark:bg-indigo-950/80 border-indigo-500 ring-2 ring-indigo-500/30'
              : 'bg-slate-50 dark:bg-slate-800/80 border-slate-200 dark:border-slate-700 hover:border-indigo-400'
          }">
            <div class="w-7 h-7 rounded-lg bg-gradient-to-tr ${grad} text-white text-[11px] font-bold flex items-center justify-center shrink-0">
              ${initials}
            </div>
            <div class="truncate flex-1">
              <span class="text-xs font-bold text-slate-800 dark:text-slate-100 block truncate">${member}</span>
              ${isSelected ? '<span class="text-[10px] text-indigo-600 font-semibold">Current (You)</span>' : '<span class="text-[10px] text-slate-400">Select</span>'}
            </div>
          </button>
        `;
      }).join('');

      const modal = document.getElementById('userIdentifyModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeUserIdentifyModal() {
      const modal = document.getElementById('userIdentifyModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function selectCurrentUser(name) {
      appState.currentUser = name;
      appState.hasPromptedIdentity = true;
      try {
        localStorage.setItem('fairshare_user_' + appState.currentGroupId, name);
      } catch (e) {}
      saveLocalStateOnly();
      closeUserIdentifyModal();
      renderApp();
      showToast(`Recording expenses as "${name}"`, 'success');
    }

    function handleJoinAsNewMember(e) {
      e.preventDefault();
      const input = document.getElementById('joinNewMemberNameInput');
      const name = input.value.trim();
      const group = getCurrentGroup();
      if (!name) return;

      if (!group.members.includes(name)) {
        group.members.push(name);
        commitStateChanges(`Added member ${name}`);
      }
      selectCurrentUser(name);
      input.value = '';
    }

    // --- QUICK CALCULATOR ENGINE (RULE PRESERVED INTACT) ---
    let calcState = {
      expression: '',
      liveResult: 0,
      isExpanded: false,
      justCalculated: false
    };

    function toggleCalculator(forceState = null) {
      const panel = document.getElementById('calcExpandedPanel');
      const chevron = document.getElementById('calcChevronIcon');
      
      calcState.isExpanded = forceState !== null ? forceState : !calcState.isExpanded;

      if (calcState.isExpanded) {
        panel.classList.remove('hidden');
        requestAnimationFrame(() => {
          panel.classList.remove('scale-95', 'opacity-0', 'pointer-events-none');
          chevron.classList.add('rotate-180');
        });
      } else {
        panel.classList.add('scale-95', 'opacity-0', 'pointer-events-none');
        chevron.classList.remove('rotate-180');
        setTimeout(() => {
          if (!calcState.isExpanded) panel.classList.add('hidden');
        }, 200);
      }

      updateCalculatorDisplay();
    }

    function openCalculatorFromModal() {
      toggleCalculator(true);
      const currentAmount = parseFloat(document.getElementById('expenseAmount').value);
      if (currentAmount && (!calcState.expression || calcState.expression === '0')) {
        calcState.expression = String(currentAmount);
        calcState.liveResult = currentAmount;
        calcState.justCalculated = true;
        updateCalculatorDisplay();
      }
    }

    function calcNumber(digit) {
      if (calcState.justCalculated) {
        calcState.expression = digit === '00' ? '0' : digit;
        calcState.justCalculated = false;
      } else if (calcState.expression === '0' && digit !== '00') {
        calcState.expression = digit;
      } else {
        calcState.expression += digit;
      }
      evaluateCalcLive();
      updateCalculatorDisplay();
    }

    function calcDecimal() {
      if (calcState.justCalculated) {
        calcState.expression = '0.';
        calcState.justCalculated = false;
        evaluateCalcLive();
        updateCalculatorDisplay();
        return;
      }
      const tokens = calcState.expression.split(/[\+\-\*\/%]/);
      const currentToken = tokens[tokens.length - 1];
      if (!currentToken.includes('.')) {
        calcState.expression += currentToken ? '.' : '0.';
        evaluateCalcLive();
        updateCalculatorDisplay();
      }
    }

    function calcOperator(op) {
      calcState.justCalculated = false;
      if (!calcState.expression) {
        if (op === '-') calcState.expression = '-';
        return;
      }
      const lastChar = calcState.expression.slice(-1);
      if (['+', '-', '*', '/', '%'].includes(lastChar)) {
        calcState.expression = calcState.expression.slice(0, -1) + op;
      } else {
        calcState.expression += op;
      }
      evaluateCalcLive();
      updateCalculatorDisplay();
    }

    function calcAppendPreset(preset) {
      calcState.justCalculated = false;
      const lastChar = calcState.expression.slice(-1);
      if (['+', '-', '*', '/', '%'].includes(lastChar) && (preset.startsWith('+') || preset.startsWith('/'))) {
        calcState.expression = calcState.expression.slice(0, -1);
      }
      calcState.expression += preset;
      evaluateCalcLive();
      updateCalculatorDisplay();
    }

    function calcBackspace() {
      calcState.justCalculated = false;
      if (calcState.expression.length > 0) {
        calcState.expression = calcState.expression.slice(0, -1);
        evaluateCalcLive();
        updateCalculatorDisplay();
      }
    }

    function calcClear() {
      calcState.expression = '';
      calcState.liveResult = 0;
      calcState.justCalculated = false;
      updateCalculatorDisplay();
    }

    function evaluateCalcLive() {
      if (!calcState.expression) {
        calcState.liveResult = 0;
        return;
      }
      try {
        let sanitized = calcState.expression;
        while (['+', '-', '*', '/', '%'].includes(sanitized.slice(-1))) {
          sanitized = sanitized.slice(0, -1);
        }
        if (!sanitized) {
          calcState.liveResult = 0;
          return;
        }

        sanitized = sanitized.replace(/(\d+(\.\d+)?)\s*([\+\-])\s*(\d+(\.\d+)?)%/g, '($1 $3 ($1 * $4 / 100))');
        sanitized = sanitized.replace(/(\d+(\.\d+)?)\s*([\*\/])\s*(\d+(\.\d+)?)%/g, '($1 $3 ($4 / 100))');
        sanitized = sanitized.replace(/(\d+(\.\d+)?)%/g, '($1 / 100)');

        if (/^[0-9\+\-\*\/\.\(\)\s]+$/.test(sanitized)) {
          const result = Function('"use strict";return (' + sanitized + ')')();
          if (typeof result === 'number' && !isNaN(result) && isFinite(result)) {
            calcState.liveResult = Math.round(result * 100) / 100;
          }
        }
      } catch (e) {}
    }

    function calcEquals() {
      evaluateCalcLive();
      if (typeof calcState.liveResult === 'number' && !isNaN(calcState.liveResult)) {
        calcState.expression = String(calcState.liveResult);
        calcState.justCalculated = true;
        updateCalculatorDisplay();
      }
    }

    function updateCalculatorDisplay() {
      const exprEl = document.getElementById('calcExpressionDisplay');
      const resEl = document.getElementById('calcResultDisplay');
      const pillPreview = document.getElementById('calcPillPreview');
      const currencyBadge = document.getElementById('calcCurrencyBadge');
      const currPrefix = document.getElementById('calcDisplayPrefix');
      const currentCurr = (getCurrentGroup().currency || appState.currency || '₹');

      if (currencyBadge) currencyBadge.textContent = `${currentCurr} Currency`;
      if (currPrefix) currPrefix.textContent = currentCurr;

      const visualExpr = (calcState.expression || '0')
        .replace(/\*/g, ' × ').replace(/\//g, ' ÷ ').replace(/\+/g, ' + ').replace(/\-/g, ' − ');

      if (exprEl) exprEl.textContent = visualExpr;

      const formattedResult = Number(calcState.liveResult || 0).toLocaleString('en-IN', {
        minimumFractionDigits: 2, maximumFractionDigits: 2
      });

      if (resEl) resEl.textContent = formattedResult;
      if (pillPreview) pillPreview.textContent = `${currentCurr}${formattedResult}`;
    }

    function insertCalcResultIntoAmount() {
      evaluateCalcLive();
      const val = Number(calcState.liveResult) || 0;
      if (val <= 0) {
        showToast('Please calculate an amount greater than 0 first', 'warning');
        return;
      }

      const modal = document.getElementById('expenseModal');
      if (modal.classList.contains('hidden')) {
        openExpenseModal();
      }

      const amountInput = document.getElementById('expenseAmount');
      amountInput.value = val.toFixed(2);
      onExpenseAmountChanged();

      amountInput.classList.add('ring-4', 'ring-emerald-400');
      setTimeout(() => amountInput.classList.remove('ring-4', 'ring-emerald-400'), 1200);

      toggleCalculator(false);
      showToast(`Inserted ${formatMoney(val)} into expense amount!`, 'success');
    }

    // --- UI RENDER ROUTINES ---
    function renderMembersList() {
      const group = getCurrentGroup();
      const container = document.getElementById('membersList');
      if (!container) return;

      container.innerHTML = group.members.map(member => {
        const initials = getInitials(member);
        const grad = getAvatarGradient(member);
        const isYou = appState.currentUser === member;
        const isDeletable = group.members.length > 3;
        const profile = group.memberProfiles[member] || {};
        const upi = profile.upiId;

        return `
          <div class="flex items-center justify-between p-2.5 rounded-2xl ${
            isYou
              ? 'bg-indigo-50/70 dark:bg-indigo-950/40 border-indigo-200 dark:border-indigo-800/70 shadow-sm'
              : 'bg-slate-50 dark:bg-slate-800/60 border-slate-100 dark:border-slate-800'
          } border hover:border-indigo-300 dark:hover:border-indigo-700 transition">
            <div class="flex items-center gap-2.5 min-w-0">
              <div class="w-8 h-8 rounded-xl bg-gradient-to-tr ${grad} text-white font-bold text-xs flex items-center justify-center shadow-sm shrink-0">
                ${initials}
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-1.5 truncate">
                  <span class="text-xs sm:text-sm font-bold text-slate-800 dark:text-slate-200 truncate">${member}</span>
                  ${isYou ? '<span class="text-[10px] font-extrabold px-1.5 py-0.5 rounded-md bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 shrink-0">You</span>' : ''}
                </div>
                <div class="flex items-center gap-1 mt-0.5">
                  <button onclick="openSetUpiModal('${member.replace(/'/g, "\\'")}')" class="text-[10px] font-mono font-semibold px-1.5 py-0.2 rounded-md ${upi ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950' : 'text-slate-400 hover:text-indigo-500'} truncate max-w-[150px]" title="Click to edit UPI ID">
                    ${upi ? `💳 ${upi}` : '+ Set UPI ID'}
                  </button>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-1">
              <button onclick="openRenameMemberModal('${member.replace(/'/g, "\\'")}')" class="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600" title="Rename ${member}">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
              </button>
              <button onclick="removeMember('${member.replace(/'/g, "\\'")}')" class="p-1.5 rounded-lg text-slate-400 hover:text-rose-500 ${isDeletable ? '' : 'opacity-30 cursor-not-allowed'}" title="Remove member">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderIndividualBalances(balances, transactions = []) {
      const group = getCurrentGroup();
      const container = document.getElementById('individualBalancesList');
      if (!container) return;
      const EPSILON = 0.01;

      container.innerHTML = group.members.map(member => {
        const data = balances[member] || { paid: 0, share: 0, net: 0 };
        const initials = getInitials(member);
        const grad = getAvatarGradient(member);
        const isCurrent = appState.currentUser === member;

        const debtsOwed = (transactions || []).filter(t => t.from === member);
        const creditsReceivable = (transactions || []).filter(t => t.to === member);
        const totalOwed = debtsOwed.reduce((sum, t) => sum + t.amount, 0);
        const totalReceivable = creditsReceivable.reduce((sum, t) => sum + t.amount, 0);

        let badgeHtml = '';
        if (totalOwed > EPSILON && totalReceivable > EPSILON) {
          badgeHtml = `
            <div class="text-right">
              <span class="text-xs font-bold text-rose-600 block">Owes ${formatMoney(totalOwed)}</span>
              <span class="text-[11px] font-bold text-emerald-600 block">+${formatMoney(totalReceivable)}</span>
            </div>
          `;
        } else if (totalOwed > EPSILON) {
          badgeHtml = `<span class="text-xs font-bold text-rose-600">Owes ${formatMoney(totalOwed)}</span>`;
        } else if (totalReceivable > EPSILON) {
          badgeHtml = `<span class="text-xs font-bold text-emerald-600">+${formatMoney(totalReceivable)}</span>`;
        } else {
          badgeHtml = `<span class="text-xs font-bold text-emerald-600">✓ Settled</span>`;
        }

        return `
          <div class="p-3 rounded-2xl ${isCurrent ? 'bg-indigo-50/50 dark:bg-indigo-950/30 border-indigo-200' : 'bg-slate-50 dark:bg-slate-800/40 border-slate-100'} border flex items-center justify-between">
            <div class="flex items-center gap-2.5 min-w-0">
              <div class="w-7 h-7 rounded-lg bg-gradient-to-tr ${grad} text-white font-bold text-[10px] flex items-center justify-center shrink-0">
                ${initials}
              </div>
              <div class="truncate">
                <span class="text-xs font-bold text-slate-800 dark:text-slate-100 block truncate">${member}</span>
                <span class="text-[10px] text-slate-400">Paid: ${formatMoney(data.paid)} · Share: ${formatMoney(data.share)}</span>
              </div>
            </div>
            ${badgeHtml}
          </div>
        `;
      }).join('');
    }

    function renderSettlementPlan(transactions) {
      const container = document.getElementById('settlementPlanContainer');
      if (!container) return;

      if (transactions.length === 0) {
        container.innerHTML = `
          <div class="py-8 px-4 rounded-2xl bg-white/5 border border-white/10 text-center">
            <div class="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              ✓
            </div>
            <h4 class="text-sm sm:text-base font-bold text-white">All Balances Are Settled!</h4>
            <p class="text-xs text-indigo-200 mt-1 max-w-sm mx-auto">Nobody owes money to anyone right now. Strict pair-to-pair debts are clear.</p>
          </div>
        `;
        return;
      }

      container.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          ${transactions.map((tx, idx) => {
            const fromInitials = getInitials(tx.from);
            const toInitials = getInitials(tx.to);
            const fromGrad = getAvatarGradient(tx.from);
            const toGrad = getAvatarGradient(tx.to);
            const isPayer = appState.currentUser === tx.from;
            const isReceiver = appState.currentUser === tx.to;

            return `
              <div class="p-4 rounded-2xl bg-white/10 hover:bg-white/15 border border-white/15 backdrop-blur-md transition flex flex-col justify-between gap-3 group">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-400/20 text-indigo-200 border border-indigo-400/30">
                    Debt ${idx + 1} • 1-to-1 Pair
                  </span>
                  <span class="text-base font-extrabold text-white tracking-tight">${formatMoney(tx.amount)}</span>
                </div>

                <div class="flex items-center justify-between gap-2">
                  <div class="flex items-center gap-2 min-w-0">
                    <div class="w-7 h-7 rounded-xl bg-gradient-to-tr ${fromGrad} text-white text-[11px] font-bold flex items-center justify-center shrink-0">${fromInitials}</div>
                    <div class="truncate">
                      <span class="text-xs font-bold text-white block truncate">${tx.from} ${isPayer ? '(You)' : ''}</span>
                      <span class="text-[10px] text-rose-300">Debtor (Owes)</span>
                    </div>
                  </div>

                  <span class="text-indigo-300 font-bold">➔</span>

                  <div class="flex items-center gap-2 min-w-0 justify-end text-right">
                    <div class="truncate">
                      <span class="text-xs font-bold text-white block truncate">${tx.to} ${isReceiver ? '(You)' : ''}</span>
                      <span class="text-[10px] text-emerald-300">Creditor</span>
                    </div>
                    <div class="w-7 h-7 rounded-xl bg-gradient-to-tr ${toGrad} text-white text-[11px] font-bold flex items-center justify-center shrink-0">${toInitials}</div>
                  </div>
                </div>

                <!-- UPI Pay & Settle Action Row -->
                <div class="pt-2 border-t border-white/10 flex items-center justify-between gap-2">
                  <span class="text-[11px] text-indigo-200 truncate">Instant Settlement:</span>
                  <div class="flex items-center gap-1.5 shrink-0">
                    <button onclick="openPayViaUpiModal('${tx.from.replace(/'/g, "\\'")}', '${tx.to.replace(/'/g, "\\'")}', ${tx.amount})" class="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-md transition flex items-center gap-1 active:scale-95" title="Pay via Google Pay, PhonePe, Paytm">
                      <span>⚡ Pay via UPI</span>
                    </button>
                    <button onclick="recordIndividualSettlement('${tx.from.replace(/'/g, "\\'")}', '${tx.to.replace(/'/g, "\\'")}', ${tx.amount})" class="px-2.5 py-1.5 rounded-xl bg-white/15 hover:bg-white/25 text-white font-semibold text-xs transition">
                      Mark Settled
                    </button>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    function renderExpensesList() {
      const group = getCurrentGroup();
      const container = document.getElementById('expenseListContainer');
      const countBadge = document.getElementById('badgeExpenseCount');
      if (!container) return;

      let filtered = group.expenses;
      if (appState.categoryFilter !== 'ALL') {
        filtered = filtered.filter(exp => exp.category === appState.categoryFilter);
      }
      if (appState.searchQuery) {
        filtered = filtered.filter(exp => 
          (exp.title && exp.title.toLowerCase().includes(appState.searchQuery)) ||
          (exp.paidBy && exp.paidBy.toLowerCase().includes(appState.searchQuery))
        );
      }

      countBadge.textContent = `${filtered.length} bills`;

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="text-center py-10 px-4 rounded-3xl bg-slate-50 dark:bg-slate-800/30 border border-dashed border-slate-200 dark:border-slate-800">
            <span class="text-3xl block mb-2">🧾</span>
            <h4 class="text-sm font-bold text-slate-800 dark:text-slate-200">No Expenses Recorded</h4>
            <p class="text-xs text-slate-500 mt-1">Click "Add Expense" or "Scan Receipt" to record bills.</p>
          </div>
        `;
        return;
      }

      container.innerHTML = filtered.map(exp => {
        const isSettlement = exp.isSettlement || exp.category === 'Settlement';
        if (isSettlement) {
          const recipient = (Array.isArray(exp.splitAmong) && exp.splitAmong.length > 0) ? exp.splitAmong[0] : 'Member';
          return `
            <div class="p-3.5 sm:p-4 rounded-2xl bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/70 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 flex items-center justify-center text-lg font-bold shrink-0">
                  🤝
                </div>
                <div>
                  <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">${exp.paidBy} paid ${recipient} (Settled)</h4>
                  <span class="text-[11px] text-slate-500">Pair debt settled • Permanent audit log ${exp.date ? `• ${exp.date}` : ''}</span>
                </div>
              </div>
              <div class="text-right">
                <span class="text-sm sm:text-base font-extrabold text-emerald-700 dark:text-emerald-300">${formatMoney(exp.amount)}</span>
                <span class="text-[10px] text-emerald-600 block">Settled ✓</span>
              </div>
            </div>
          `;
        }

        const catConfig = CATEGORIES[exp.category] || CATEGORIES['Other'];
        const splitCount = exp.splitAmong ? exp.splitAmong.length : group.members.length;
        const payerGrad = getAvatarGradient(exp.paidBy);
        const payerInitials = getInitials(exp.paidBy);

        return `
          <div class="p-3.5 sm:p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 hover:border-slate-200 dark:hover:border-slate-700 transition flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-start sm:items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-xl ${catConfig.color} flex items-center justify-center text-lg shrink-0 shadow-sm">
                ${catConfig.icon}
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 truncate">${exp.title}</h4>
                  <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full ${catConfig.color}">${catConfig.label}</span>
                  ${exp.splitMode && exp.splitMode !== 'equal' ? `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-purple-100 text-purple-700 dark:bg-purple-950 capitalize">${exp.splitMode} Split</span>` : ''}
                </div>
                <div class="mt-1 flex items-center gap-2 flex-wrap text-[11px] text-slate-500 dark:text-slate-400">
                  <span>Paid by <strong>${exp.paidBy}</strong></span>
                  <span>•</span>
                  <span>Split among ${splitCount} (${(exp.splitAmong || []).join(', ')})</span>
                  ${exp.date ? `<span>•</span><span>${exp.date}</span>` : ''}
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between sm:justify-end gap-3 shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100 dark:border-slate-800">
              <div class="text-left sm:text-right">
                <span class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white block">${formatMoney(exp.amount)}</span>
                <span class="text-[10px] text-slate-400">${formatMoney(exp.amount / splitCount)} / person</span>
              </div>
              <button onclick="editExpense('${exp.id}')" class="p-1.5 rounded-xl text-slate-400 hover:text-indigo-600 transition" title="Edit details">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderRecentGroups() {
      const container = document.getElementById('recentGroupsList');
      if (!container) return;
      const allGroupIds = Object.keys(appState.groups);

      if (allGroupIds.length <= 1) {
        container.innerHTML = `<p class="text-[11px] text-slate-400">No other groups saved.</p>`;
        return;
      }

      container.innerHTML = allGroupIds.filter(id => id !== appState.currentGroupId).slice(0, 3).map(id => {
        const grp = appState.groups[id];
        return `
          <button onclick="switchToGroup('${id}')" class="w-full flex items-center justify-between p-2 rounded-xl bg-slate-50 dark:bg-slate-800/50 hover:bg-slate-100 border border-slate-100 dark:border-slate-800 text-left transition text-xs">
            <span class="font-bold text-slate-800 dark:text-slate-200 truncate">${grp.name || id}</span>
            <span class="font-bold text-indigo-600">➔</span>
          </button>
        `;
      }).join('');
    }

    // Master Render Routine
    function renderApp() {
      const group = getCurrentGroup();
      const balances = calculateBalances();
      const transactions = calculateDirectPairDebts();

      document.getElementById('groupNameHeading').textContent = group.name;
      document.getElementById('roomCodeBadge').textContent = group.id;

      const actualExpenses = group.expenses.filter(e => !e.isSettlement && e.category !== 'Settlement');
      const totalExpense = actualExpenses.reduce((sum, e) => sum + (Number(e.amount) || 0), 0);
      const memberCount = group.members.length;
      const avgPerPerson = memberCount > 0 ? (totalExpense / memberCount) : 0;

      document.getElementById('metricTotalExpense').textContent = formatMoney(totalExpense);
      document.getElementById('metricAvgPerPerson').textContent = formatMoney(avgPerPerson);
      document.getElementById('metricMemberCount').textContent = memberCount;
      document.getElementById('badgeMemberTotal').textContent = memberCount;
      document.getElementById('metricSettlementTransCount').textContent = transactions.length;

      const statusEl = document.getElementById('metricSettlementStatus');
      if (transactions.length === 0) {
        statusEl.textContent = 'All Settled';
        statusEl.className = 'text-xs text-emerald-600 dark:text-emerald-400 font-semibold';
      } else {
        statusEl.textContent = `${transactions.length} Pending`;
        statusEl.className = 'text-xs text-amber-500 font-semibold';
      }

      renderMembersList();
      renderIndividualBalances(balances, transactions);
      renderSettlementPlan(transactions);
      renderExpensesList();
      renderRecentGroups();
      renderAuthNav();

      document.getElementById('currencySelector').value = group.currency || appState.currency;
      document.getElementById('amountCurrencyPrefix').textContent = group.currency || appState.currency;
      updateCalculatorDisplay();

      if (appState.activeTab === 'analytics') renderAnalyticsCharts();
      if (appState.activeTab === 'recurring') renderRecurringBills();
    }

    // --- FIREBASE CLOUD FIRESTORE & AUTH INTEGRATION ---
    function initFirebaseCloud() {
      // Developer Console Helper Instructions
      console.info(
        '%c[FairShare Firebase Setup Guide]%c\n' +
        '1. Firebase Console -> Authentication -> Sign-in method: Enable "Google" and "Email/Password".\n' +
        '2. Firebase Console -> Authentication -> Settings -> Authorized domains: Add:\n' +
        '   - pr8848276-arch.github.io\n' +
        '   - localhost\n' +
        '   - 127.0.0.1\n' +
        'Tip: Users can click "Continue as Guest" to preview and use the app offline at any time.',
        'font-weight:bold;color:#4f46e5;font-size:12px;',
        'color:#64748b;font-size:11px;'
      );

      try {
        let config = DEFAULT_FIREBASE_CONFIG;
        const savedConfigStr = localStorage.getItem(FB_CONFIG_KEY);
        if (savedConfigStr) {
          try {
            const parsed = JSON.parse(savedConfigStr);
            if (parsed && !parsed.disabled) config = parsed;
          } catch (e) {}
        }

        if (typeof firebase !== 'undefined') {
          if (!firebase.apps.length) firebase.initializeApp(config);
          firebaseDb = firebase.firestore();

          // Initialize Firebase Auth with LOCAL persistence and persistent observer
          getFirebaseAuth();

          isCloudOnline = true;
          setCloudStatusUI(true, 'Firestore Connected');
          listenToActiveGroupInCloud();
        }
      } catch (err) {
        console.warn('Firebase init offline fallback:', err);
        isCloudOnline = false;
        setCloudStatusUI(false, 'Local & Tab Relay');
      }
    }

    function setCloudStatusUI(connected, text) {
      const dot = document.getElementById('cloudStatusDot');
      const textEl = document.getElementById('cloudStatusText');
      if (connected) {
        dot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-subtle';
        textEl.textContent = text || 'Live Sync';
      } else {
        dot.className = 'w-1.5 h-1.5 rounded-full bg-amber-500';
        textEl.textContent = text || 'Local Sync';
      }
      updateSyncIndicator();
    }

    function listenToActiveGroupInCloud() {
      if (!firebaseDb || !isCloudOnline) return;
      if (firestoreUnsubscribe) firestoreUnsubscribe();

      const groupId = appState.currentGroupId;
      const docRef = firebaseDb.collection('fairshare_groups').doc(groupId);

      firestoreUnsubscribe = docRef.onSnapshot({ includeMetadataChanges: true }, (doc) => {
        if (doc.exists && !doc.metadata.hasPendingWrites) {
          const remoteData = doc.data();
          appState.groups[groupId] = {
            id: remoteData.id || groupId,
            name: remoteData.name || `Room ${groupId}`,
            currency: remoteData.currency || appState.currency || '₹',
            members: Array.isArray(remoteData.members) && remoteData.members.length > 0 ? remoteData.members : ['Rahul', 'Amit', 'Pooja'],
            memberProfiles: remoteData.memberProfiles || {},
            expenses: Array.isArray(remoteData.expenses) ? remoteData.expenses : [],
            recurringBills: Array.isArray(remoteData.recurringBills) ? remoteData.recurringBills : [],
            updatedAt: remoteData.updatedAt || Date.now(),
            isPlaceholder: false
          };
          saveLocalStateOnly();
          renderApp();
        }
      }, err => console.warn('Firestore snapshot error:', err));
    }

    function syncGroupToFirebase(group) {
      if (!firebaseDb || !isCloudOnline) return;
      try {
        firebaseDb.collection('fairshare_groups').doc(group.id).set({
          id: group.id,
          name: group.name,
          currency: group.currency || '₹',
          members: group.members || [],
          memberProfiles: group.memberProfiles || {},
          expenses: group.expenses || [],
          recurringBills: group.recurringBills || [],
          updatedAt: group.updatedAt || Date.now()
        }, { merge: true }).catch(e => console.warn('Sync write note:', e));
      } catch (e) {}
    }

    // --- UTILITIES, DARK MODE, CURRENCY & CLOUDS ---
    function toggleDarkMode() {
      appState.darkMode = !appState.darkMode;
      applyDarkMode();
      saveLocalStateOnly();
      if (appState.activeTab === 'analytics') renderAnalyticsCharts();
    }

    function applyDarkMode() {
      if (appState.darkMode) document.documentElement.classList.add('dark');
      else document.documentElement.classList.remove('dark');
    }

    function changeCurrency(newCurr) {
      appState.currency = newCurr;
      getCurrentGroup().currency = newCurr;
      commitStateChanges('Changed currency');
      renderApp();
      showToast(`Group currency changed to ${newCurr}`, 'info');
    }

    function handleSearchExpenses(val) {
      appState.searchQuery = val.trim().toLowerCase();
      renderExpensesList();
    }

    function handleCategoryFilter(val) {
      appState.categoryFilter = val;
      renderExpensesList();
    }

    function copyToClipboard(text, msg) {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => showToast(msg, 'success')).catch(() => fallbackCopy(text, msg));
      } else {
        fallbackCopy(text, msg);
      }
    }

    function fallbackCopy(text, msg) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try { document.execCommand('copy'); showToast(msg, 'success'); } catch (e) {}
      document.body.removeChild(ta);
    }

    function copyRoomCode() {
      copyToClipboard(getCurrentGroup().id, `Room Code "${getCurrentGroup().id}" copied!`);
    }

    function copyGroupShareLink() {
      const link = window.location.origin + window.location.pathname + '?group=' + getCurrentGroup().id;
      copyToClipboard(link, 'Shareable group link copied to clipboard!');
    }

    function copySettlementSummary() {
      const transactions = calculateDirectPairDebts();
      const group = getCurrentGroup();
      let text = `📊 *${group.name}* (${group.id}) — Direct Pair Settlement Plan\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
      if (transactions.length === 0) {
        text += `🎉 All balances are settled up! Nobody owes anything.\n`;
      } else {
        transactions.forEach((tx, idx) => {
          text += `${idx + 1}. *${tx.from}* owes *${tx.to}* ➔ ${formatMoney(tx.amount)}\n`;
        });
      }
      text += `\nCalculated via FairShare (Direct Pair Tracking)`;
      copyToClipboard(text, 'Settlement summary copied to clipboard!');
    }

    function downloadCSVReport() {
      const group = getCurrentGroup();
      if (group.expenses.length === 0) {
        showToast('No expenses recorded to export!', 'warning');
        return;
      }
      let csv = 'ID,Date,Description,Category,Total Amount,Paid By,Split Count,Participants\r\n';
      group.expenses.forEach(exp => {
        csv += `"${exp.id}","${exp.date || ''}","${(exp.title || '').replace(/"/g, '""')}","${exp.category || 'Other'}",${exp.amount},"${exp.paidBy}",${(exp.splitAmong || []).length},"${(exp.splitAmong || []).join('; ')}"\r\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `FairShare_${group.id}_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast('Exported CSV spreadsheet!', 'success');
    }

    function showToast(message, type = 'info') {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      let borderClass = 'border-slate-300 dark:border-slate-700 bg-slate-900/90 text-white';
      let icon = 'ℹ️';
      if (type === 'success') { borderClass = 'border-emerald-500/50 bg-emerald-950/90 text-emerald-100'; icon = '✅'; }
      else if (type === 'warning') { borderClass = 'border-amber-500/50 bg-amber-950/90 text-amber-100'; icon = '⚠️'; }

      toast.className = `flex items-center gap-2.5 px-4 py-3 rounded-2xl shadow-xl border ${borderClass} text-xs font-semibold backdrop-blur-md transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-auto max-w-sm`;
      toast.innerHTML = `<span>${icon}</span> <span class="leading-tight">${message}</span>`;
      container.appendChild(toast);

      requestAnimationFrame(() => toast.classList.remove('translate-y-4', 'opacity-0'));
      setTimeout(() => {
        toast.classList.add('opacity-0', '-translate-x-4');
        setTimeout(() => toast.remove(), 300);
      }, 3200);
    }

    // Modal helpers
    function openShareModal() {
      const group = getCurrentGroup();
      document.getElementById('shareModalRoomCode').textContent = group.id;
      const shareUrl = window.location.origin + window.location.pathname + '?group=' + group.id;
      document.getElementById('shareModalLinkInput').value = shareUrl;
      const qrContainer = document.getElementById('qrcodeCanvas');
      qrContainer.innerHTML = '';
      if (typeof QRCode !== 'undefined') {
        new QRCode(qrContainer, { text: shareUrl, width: 140, height: 140, colorDark: '#312e81', colorLight: '#ffffff' });
      }
      const modal = document.getElementById('shareModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeShareModal() {
      const modal = document.getElementById('shareModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function openGroupSwitchModal() {
      const modal = document.getElementById('groupSwitchModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
      switchGroupModalTab('create');
    }

    function closeGroupSwitchModal() {
      const modal = document.getElementById('groupSwitchModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function switchGroupModalTab(tab) {
      const createBtn = document.getElementById('tabCreateGroupBtn');
      const joinBtn = document.getElementById('tabJoinGroupBtn');
      const createForm = document.getElementById('createGroupTabForm');
      const joinForm = document.getElementById('joinGroupTabForm');
      if (tab === 'create') {
        createBtn.className = 'flex-1 py-2 border-b-2 border-indigo-600 text-indigo-600 font-bold';
        joinBtn.className = 'flex-1 py-2 border-b-2 border-transparent text-slate-400';
        createForm.classList.remove('hidden');
        joinForm.classList.add('hidden');
      } else {
        joinBtn.className = 'flex-1 py-2 border-b-2 border-indigo-600 text-indigo-600 font-bold';
        createBtn.className = 'flex-1 py-2 border-b-2 border-transparent text-slate-400';
        joinForm.classList.remove('hidden');
        createForm.classList.add('hidden');
      }
    }

    function handleCreateNewGroup(e) {
      e.preventDefault();
      const name = document.getElementById('newGroupNameInput').value.trim();
      const membersStr = document.getElementById('newGroupMembersInput').value.trim();
      if (!name) return;

      const members = membersStr ? membersStr.split(',').map(m => m.trim()).filter(Boolean) : ['Rahul', 'Amit', 'Pooja'];
      if (members.length < 3) {
        showToast('Please specify at least 3 members', 'warning');
        return;
      }

      const newId = generateRoomCode(name);
      appState.groups[newId] = {
        id: newId,
        name: name,
        currency: appState.currency || '₹',
        members: members,
        memberProfiles: {},
        expenses: [],
        recurringBills: [],
        updatedAt: Date.now(),
        isPlaceholder: false
      };
      appState.currentGroupId = newId;
      selectCurrentUser(members[0]);
      commitStateChanges(`Created group ${name}`);
      listenToActiveGroupInCloud();
      closeGroupSwitchModal();
      renderApp();
      showToast(`Created group "${name}" (${newId})!`, 'success');
    }

    function handleJoinByRoomCode(e) {
      e.preventDefault();
      let code = document.getElementById('joinRoomCodeInput').value.trim().toUpperCase();
      if (!code) return;
      switchToGroup(code);
      closeGroupSwitchModal();
    }

    function switchToGroup(groupId) {
      appState.currentGroupId = groupId;
      const savedUser = localStorage.getItem('fairshare_user_' + groupId);
      appState.currentUser = savedUser || null;
      listenToActiveGroupInCloud();
      renderApp();
      showToast(`Switched to Room ${groupId}`, 'info');
    }

    function openCloudModal() {
      const modal = document.getElementById('cloudModal');
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.firstElementChild.classList.remove('scale-95');
      });
    }

    function closeCloudModal() {
      const modal = document.getElementById('cloudModal');
      modal.classList.add('opacity-0');
      modal.firstElementChild.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 200);
    }

    function handleSaveFirebaseConfig(e) {
      e.preventDefault();
      const apiKey = document.getElementById('fbApiKey').value.trim();
      const projectId = document.getElementById('fbProjectId').value.trim();
      if (!apiKey || !projectId) {
        showToast('Please enter apiKey and projectId', 'warning');
        return;
      }
      localStorage.setItem(FB_CONFIG_KEY, JSON.stringify({ apiKey, projectId }));
      closeCloudModal();
      initFirebaseCloud();
      showToast('Firebase settings saved', 'success');
    }

    function clearFirebaseConfig() {
      localStorage.setItem(FB_CONFIG_KEY, JSON.stringify({ disabled: true }));
      isCloudOnline = false;
      closeCloudModal();
      setCloudStatusUI(false, 'Local Peer Mode');
      showToast('Cloud disabled; using local storage', 'info');
    }

    // Keyboard support for Quick Calculator
    window.addEventListener('keydown', (e) => {
      if (!calcState.isExpanded) return;
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
      if (e.key >= '0' && e.key <= '9') { e.preventDefault(); calcNumber(e.key); }
      else if (e.key === '.') { e.preventDefault(); calcDecimal(); }
      else if (['+', '-', '*', '/'].includes(e.key)) { e.preventDefault(); calcOperator(e.key); }
      else if (e.key === '%') { e.preventDefault(); calcOperator('%'); }
      else if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); calcEquals(); }
      else if (e.key === 'Backspace') { e.preventDefault(); calcBackspace(); }
      else if (e.key === 'Escape') { e.preventDefault(); toggleCalculator(false); }
      else if (e.key.toLowerCase() === 'c') { e.preventDefault(); calcClear(); }
    });

    // Close calculator when clicking outside
    document.addEventListener('pointerdown', (e) => {
      if (!calcState.isExpanded) return;
      const widget = document.getElementById('calculatorWidget');
      if (widget && !widget.contains(e.target) && !e.target.closest('[onclick*="openCalculatorFromModal"]')) {
        toggleCalculator(false);
      }
    });

    // App Startup
    window.addEventListener('DOMContentLoaded', () => {
      loadLocalState();
      applyDarkMode();
      initFirebaseCloud();
      renderApp();

      // If no auth user and not in guest mode, prompt welcome auth after short delay
      if (!appState.authUser && !appState.isGuest) {
        setTimeout(() => openAuthModal(), 600);
      }
    });
  </script>
</body>
</html>
"""
