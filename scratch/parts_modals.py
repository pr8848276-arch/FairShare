# Modals and Floating Calculator Widget
MODALS_HTML = r"""
  <!-- AUTHENTICATION / LANDING MODAL (GOOGLE & EMAIL/PASSWORD & DEMO) -->
  <div id="authModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-md w-full p-6 sm:p-7 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 max-h-[95vh] overflow-y-auto">
      
      <!-- Modal Header -->
      <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white font-extrabold flex items-center justify-center text-xl shadow-md shadow-indigo-500/30">
            🔐
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white" id="authModalTitle">Welcome to FairShare</h3>
            <p class="text-xs text-slate-500">Sign in to manage and view private group expenses</p>
          </div>
        </div>
        <button onclick="closeAuthModal()" class="p-1 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Auth Method Selector Tabs -->
      <div class="flex items-center gap-1 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl my-4 text-xs font-semibold">
        <button type="button" onclick="switchAuthTab('google')" id="authTabGoogleBtn" class="flex-1 py-2 rounded-lg bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 font-bold shadow-sm transition">
          Google Login
        </button>
        <button type="button" onclick="switchAuthTab('email')" id="authTabEmailBtn" class="flex-1 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition">
          Email & Password
        </button>
      </div>

      <!-- Tab 1: Google Sign In -->
      <div id="authGoogleTabContent" class="space-y-4">
        <p class="text-xs text-slate-600 dark:text-slate-400">
          Fast and secure authentication using your Google account via Firebase Auth.
        </p>

        <button type="button" onclick="handleGoogleSignIn()" class="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl border border-slate-300 dark:border-slate-700 hover:border-indigo-400 dark:hover:border-indigo-500 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 font-bold text-xs sm:text-sm shadow-sm transition hover:bg-slate-50 dark:hover:bg-slate-700/80 active:scale-98">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          <span>Continue with Google</span>
        </button>
      </div>

      <!-- Tab 2: Email & Password Registration / Sign-In -->
      <form id="authEmailTabContent" onsubmit="handleEmailAuthSubmit(event)" class="hidden space-y-3.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider" id="emailAuthModeLabel">Sign In</span>
          <button type="button" onclick="toggleEmailAuthMode()" id="emailAuthToggleBtn" class="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline">
            Need an account? Register
          </button>
        </div>

        <div id="authNameFieldGroup" class="hidden">
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Your Display Name</label>
          <input type="text" id="authDisplayNameInput" placeholder="e.g. Rahul Sharma" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
          <input type="email" id="authEmailInput" required placeholder="you@domain.com" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Password</label>
          <input type="password" id="authPasswordInput" required minlength="6" placeholder="••••••••" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
        </div>

        <button type="submit" id="authEmailSubmitBtn" class="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-md shadow-indigo-600/30 transition">
          Sign In with Email
        </button>
      </form>

      <!-- Instant Quick Test / Demo Accounts (No Firebase Auth Setup Blockers) -->
      <div class="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">⚡ Instant Demo / Test Sign-in:</span>
        <div class="grid grid-cols-3 gap-2">
          <button type="button" onclick="loginAsDemoUser('Rahul Sharma', 'rahul@fairshare.app', 'rahul@okhdfcbank')" class="p-2 rounded-xl bg-slate-100 hover:bg-indigo-50 dark:bg-slate-800 dark:hover:bg-slate-700 text-left border border-slate-200 dark:border-slate-700 transition">
            <span class="text-xs font-bold text-slate-900 dark:text-white block truncate">Rahul</span>
            <span class="text-[9px] text-slate-400 block truncate">rahul@upi</span>
          </button>
          <button type="button" onclick="loginAsDemoUser('Amit Verma', 'amit@fairshare.app', 'amit@okaxis')" class="p-2 rounded-xl bg-slate-100 hover:bg-indigo-50 dark:bg-slate-800 dark:hover:bg-slate-700 text-left border border-slate-200 dark:border-slate-700 transition">
            <span class="text-xs font-bold text-slate-900 dark:text-white block truncate">Amit</span>
            <span class="text-[9px] text-slate-400 block truncate">amit@okaxis</span>
          </button>
          <button type="button" onclick="loginAsDemoUser('Pooja Patel', 'pooja@fairshare.app', 'pooja@paytm')" class="p-2 rounded-xl bg-slate-100 hover:bg-indigo-50 dark:bg-slate-800 dark:hover:bg-slate-700 text-left border border-slate-200 dark:border-slate-700 transition">
            <span class="text-xs font-bold text-slate-900 dark:text-white block truncate">Pooja</span>
            <span class="text-[9px] text-slate-400 block truncate">pooja@paytm</span>
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- AI RECEIPT & BILL SCANNER MODAL (CAMERA / UPLOAD OCR) -->
  <div id="receiptScannerModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-lg w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 max-h-[92vh] overflow-y-auto">
      
      <!-- Modal Header -->
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-2xl bg-amber-100 dark:bg-amber-950/70 text-amber-700 dark:text-amber-300 flex items-center justify-center text-lg font-bold shadow-sm">
            📸
          </div>
          <div>
            <h3 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white">AI Receipt & Bill Scanner</h3>
            <p class="text-xs text-slate-500">Camera / image OCR extraction of total & line items</p>
          </div>
        </div>
        <button onclick="closeReceiptScannerModal()" class="p-1 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Upload / Camera Drop Area -->
      <div class="mt-4">
        <label for="receiptFileInput" class="flex flex-col items-center justify-center border-2 border-dashed border-indigo-300 dark:border-indigo-800 hover:border-indigo-500 rounded-2xl p-6 cursor-pointer bg-indigo-50/40 dark:bg-indigo-950/20 transition group">
          <input type="file" id="receiptFileInput" accept="image/*" capture="environment" onchange="handleReceiptFileSelected(event)" class="hidden">
          <div class="w-14 h-14 rounded-2xl bg-indigo-100 dark:bg-indigo-900/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-2xl mb-2 group-hover:scale-110 transition transform">
            📷
          </div>
          <span class="text-xs sm:text-sm font-bold text-slate-800 dark:text-slate-200 text-center">Take a Photo or Upload Receipt Image</span>
          <span class="text-[11px] text-slate-400 mt-1">Supports PNG, JPG, JPEG paper receipts or digital bills</span>
        </label>
      </div>

      <!-- OCR Processing Status Banner (Hidden by default) -->
      <div id="ocrScanningStatus" class="hidden mt-4 p-4 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 space-y-2">
        <div class="flex items-center justify-between text-xs font-bold text-indigo-700 dark:text-indigo-300">
          <span id="ocrStatusText">Reading receipt with Tesseract AI OCR...</span>
          <span id="ocrProgressPercent">0%</span>
        </div>
        <div class="w-full bg-indigo-200 dark:bg-indigo-900 rounded-full h-2 overflow-hidden relative">
          <div id="ocrProgressBar" class="bg-indigo-600 h-2 rounded-full transition-all duration-200" style="width: 15%"></div>
          <div class="absolute inset-0 bg-white/30 scan-laser-line pointer-events-none"></div>
        </div>
      </div>

      <!-- OCR Extracted Review Container (Editable fields) -->
      <div id="ocrResultReview" class="hidden mt-4 space-y-3.5">
        <div class="p-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-2xl text-xs text-emerald-800 dark:text-emerald-200 flex items-center gap-2">
          <span>✨</span>
          <span>Receipt scanned successfully! Review and edit extracted details before applying.</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Merchant / Title</label>
            <input type="text" id="ocrTitleInput" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white font-semibold">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Extracted Total</label>
            <input type="number" step="0.01" id="ocrAmountInput" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white font-extrabold text-indigo-600 dark:text-indigo-400">
          </div>
        </div>

        <!-- Extracted Line Items -->
        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Detected Line Items</label>
          <div id="ocrLineItemsList" class="max-h-40 overflow-y-auto space-y-1.5 p-2 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700 text-xs">
            <!-- Line items rendered by JS -->
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
          <button type="button" onclick="applyOcrToExpenseForm(false)" class="px-4 py-2 text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-md transition">
            Apply to Expense Form
          </button>
          <button type="button" onclick="applyOcrToExpenseForm(true)" class="px-4 py-2 text-xs font-bold bg-purple-600 hover:bg-purple-700 text-white rounded-xl shadow-md transition" title="Use extracted items in Item-by-Item split mode">
            Use in Item-by-Item Split ➔
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- DIRECT UPI PAYMENT MODAL (INDIA UPI DEEP LINKS & QR CODE) -->
  <div id="upiPaymentModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 text-center">
      
      <!-- Modal Header -->
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 text-left">
        <div class="flex items-center gap-2">
          <span class="w-8 h-8 rounded-xl bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-base">
            ⚡
          </span>
          <div>
            <h3 class="text-sm font-bold text-slate-900 dark:text-white">Pay via UPI Instant</h3>
            <p class="text-[11px] text-slate-500">Google Pay • PhonePe • Paytm • BHIM</p>
          </div>
        </div>
        <button onclick="closeUpiPaymentModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Payment Amount Banner -->
      <div class="my-4 p-3.5 bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-indigo-500/10 dark:from-emerald-950/40 dark:to-indigo-950/40 rounded-2xl border border-emerald-200 dark:border-emerald-800/60">
        <span class="text-xs text-slate-500 dark:text-slate-400 block font-medium">Paying to <strong id="upiModalReceiverName" class="text-slate-900 dark:text-white">Receiver</strong></span>
        <span id="upiModalAmount" class="text-2xl sm:text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 tracking-tight mt-1 block">₹0.00</span>
        <span id="upiModalVpaBadge" class="text-xs font-mono font-semibold text-slate-600 dark:text-slate-300 mt-1 inline-block bg-white dark:bg-slate-800 px-2 py-0.5 rounded-md border border-slate-200 dark:border-slate-700">user@upi</span>
      </div>

      <!-- Dynamic QR Code Container -->
      <div class="flex flex-col items-center justify-center p-3 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 mx-auto w-48 h-48 mb-3 shadow-inner">
        <div id="upiQrcodeCanvas" class="flex items-center justify-center"></div>
      </div>
      <p class="text-[11px] text-slate-400 mb-4">Scan with any UPI App on your phone or click below</p>

      <!-- Action Buttons -->
      <div class="space-y-2">
        <a id="upiDeepLinkBtn" href="#" class="w-full py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:scale-98 text-white font-bold text-xs sm:text-sm shadow-md transition flex items-center justify-center gap-2">
          <span>⚡ Open UPI App (PhonePe / GPay)</span>
        </a>
        <div class="grid grid-cols-2 gap-2">
          <button type="button" onclick="copyUpiVpa()" class="py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold transition">
            Copy UPI ID
          </button>
          <button type="button" onclick="confirmAndMarkSettledFromUpi()" class="py-2 px-3 rounded-xl bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/70 text-indigo-700 dark:text-indigo-300 text-xs font-bold border border-indigo-200 dark:border-indigo-800 transition">
            ✓ Mark Settled
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- SET MEMBER UPI ID MODAL -->
  <div id="setUpiModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-base font-bold text-slate-900 dark:text-white" id="setUpiModalTitle">Set Member UPI ID</h3>
        <button onclick="closeSetUpiModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <form onsubmit="handleSaveMemberUpi(event)" class="mt-4 space-y-3">
        <input type="hidden" id="setUpiMemberNameHidden" value="">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">UPI VPA ID (Virtual Payment Address)</label>
          <input type="text" id="setUpiInput" required placeholder="e.g. rahul@okhdfcbank or 9876543210@paytm" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono">
          <p class="text-[11px] text-slate-400 mt-1">Allows instant 1-click 'Pay via UPI' settlement directly to this member.</p>
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="closeSetUpiModal()" class="px-4 py-2 text-xs font-semibold text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl">Cancel</button>
          <button type="submit" class="px-4 py-2 text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-sm">Save UPI ID</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ADD / EDIT EXPENSE MODAL (WITH SCANNER BUTTON & CUSTOM SPLIT MODES & RECURRING) -->
  <div id="expenseModal" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-t-3xl sm:rounded-3xl max-w-lg w-full p-5 sm:p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform translate-y-8 sm:translate-y-0 sm:scale-95 transition-transform duration-200 max-h-[92vh] overflow-y-auto">
      
      <!-- Modal Header -->
      <div class="flex items-center justify-between pb-3 sm:pb-4 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2">
          <div>
            <h3 id="modalTitle" class="text-lg font-bold text-slate-900 dark:text-white">Record Shared Expense</h3>
            <p class="text-xs text-slate-500">Split costs equally, exact amounts, or item-by-item</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <!-- Scan Receipt Button -->
          <button type="button" onclick="openReceiptScannerModal()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 dark:bg-amber-950/70 text-amber-800 dark:text-amber-200 border border-amber-300 dark:border-amber-700 shadow-sm transition">
            <span>📸</span>
            <span>Scan Receipt</span>
          </button>
          <button onclick="closeExpenseModal()" class="p-1.5 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Quick Preset Category Chips -->
      <div class="flex items-center gap-1.5 overflow-x-auto py-2.5 no-scrollbar">
        <button type="button" onclick="setQuickExpensePreset('🍽️ Dinner / Drinks', 'Food')" class="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 text-slate-700 dark:text-slate-300 shrink-0 transition">🍽️ Dinner</button>
        <button type="button" onclick="setQuickExpensePreset('🏠 Room Rent', 'Rent')" class="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 text-slate-700 dark:text-slate-300 shrink-0 transition">🏠 Rent</button>
        <button type="button" onclick="setQuickExpensePreset('🚗 Cab / Uber Fare', 'Travel')" class="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 text-slate-700 dark:text-slate-300 shrink-0 transition">🚗 Cab / Travel</button>
        <button type="button" onclick="setQuickExpensePreset('🛒 Groceries', 'Groceries')" class="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 text-slate-700 dark:text-slate-300 shrink-0 transition">🛒 Groceries</button>
        <button type="button" onclick="setQuickExpensePreset('⚡ Wi-Fi Bill', 'Utilities')" class="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 text-slate-700 dark:text-slate-300 shrink-0 transition">⚡ Wi-Fi</button>
      </div>

      <!-- Expense Form -->
      <form id="expenseForm" onsubmit="handleSaveExpense(event)" class="mt-2 space-y-4">
        <input type="hidden" id="editingExpenseId" value="">

        <!-- Title -->
        <div>
          <label for="expenseTitle" class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Expense Description *</label>
          <input type="text" id="expenseTitle" required placeholder="e.g. Seafood Dinner at Cafe, Scooty Rental" class="w-full text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500">
        </div>

        <!-- Amount & Category Row (with Quick Calculator Button) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="expenseAmount" class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Total Amount *</label>
              <button type="button" onclick="openCalculatorFromModal()" class="inline-flex items-center gap-1 text-[11px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline">
                <span>🧮</span>
                <span>Open Calculator</span>
              </button>
            </div>
            <div class="relative flex gap-1.5">
              <div class="relative flex-1">
                <span id="amountCurrencyPrefix" class="absolute left-3.5 top-2.5 text-slate-500 dark:text-slate-400 font-bold text-sm">₹</span>
                <input type="number" id="expenseAmount" step="0.01" min="0.01" required placeholder="0.00" oninput="onExpenseAmountChanged()" class="w-full text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl pl-8 pr-3.5 py-2.5 text-slate-900 dark:text-white placeholder-slate-400 font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all">
              </div>
              <button type="button" onclick="openCalculatorFromModal()" class="px-3 py-2 bg-indigo-50 dark:bg-indigo-950/70 hover:bg-indigo-100 dark:hover:bg-indigo-900/80 text-indigo-700 dark:text-indigo-300 border border-indigo-200/80 dark:border-indigo-800 rounded-xl text-xs font-bold transition flex items-center gap-1 shadow-sm shrink-0" title="Calculate bill amount with arithmetic">
                <span>🧮</span>
                <span class="hidden sm:inline">Calc</span>
              </button>
            </div>
          </div>

          <div>
            <label for="expenseCategory" class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Category</label>
            <select id="expenseCategory" class="w-full text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
              <option value="Food">🍽️ Food & Dining</option>
              <option value="Rent">🏠 Rent & Living</option>
              <option value="Travel">🚗 Travel & Transport</option>
              <option value="Groceries">🛒 Groceries & Snacks</option>
              <option value="Utilities">⚡ Utilities & Wi-Fi</option>
              <option value="Entertainment">🎬 Entertainment</option>
              <option value="Other">📦 Other / General</option>
            </select>
          </div>
        </div>

        <!-- Paid By & Date Row -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label for="expensePayer" class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Paid By *</label>
            <select id="expensePayer" required class="w-full text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2.5 text-slate-900 dark:text-white font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
              <!-- Dynamically populated -->
            </select>
          </div>

          <div>
            <label for="expenseDate" class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">Date</label>
            <input type="date" id="expenseDate" class="w-full text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2.5 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
          </div>
        </div>

        <!-- FLEXIBLE SPLIT MODES SELECTOR -->
        <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between mb-2">
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Split Mode</label>
            <div class="flex items-center p-0.5 bg-slate-100 dark:bg-slate-800 rounded-lg text-[11px] font-bold">
              <button type="button" onclick="setSplitMode('equal')" id="splitModeBtnEqual" class="px-2.5 py-1 rounded-md bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm transition">Equal</button>
              <button type="button" onclick="setSplitMode('exact')" id="splitModeBtnExact" class="px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-900 dark:hover:text-white transition">Exact Amount</button>
              <button type="button" onclick="setSplitMode('items')" id="splitModeBtnItems" class="px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-900 dark:hover:text-white transition">Item-by-Item</button>
            </div>
          </div>

          <!-- Split Container 1: Equal Split Checkboxes -->
          <div id="splitEqualContainer">
            <div class="flex items-center justify-between mb-1.5 text-[11px]">
              <span class="text-slate-500">Select participants to divide equally:</span>
              <div class="flex items-center gap-2">
                <button type="button" onclick="selectAllSplitters(true)" class="font-semibold text-indigo-600 dark:text-indigo-400 hover:underline">Select All</button>
                <span class="text-slate-300 dark:text-slate-700">|</span>
                <button type="button" onclick="selectAllSplitters(false)" class="font-semibold text-slate-500 hover:underline">Clear</button>
              </div>
            </div>
            <div id="splitCheckboxesContainer" class="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-40 overflow-y-auto p-1 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200/80 dark:border-slate-800">
              <!-- Dynamic checkboxes -->
            </div>
            <div id="splitLivePreview" class="mt-2 p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 border border-indigo-100 dark:border-indigo-900/60 text-xs text-indigo-800 dark:text-indigo-300 flex items-center justify-between">
              <span class="font-medium">Each person pays:</span>
              <span id="splitLiveAmount" class="font-bold">₹0.00 / person</span>
            </div>
          </div>

          <!-- Split Container 2: Exact Amount Mode -->
          <div id="splitExactContainer" class="hidden space-y-2">
            <div class="flex items-center justify-between text-xs text-slate-500">
              <span>Enter custom amounts for each member:</span>
              <button type="button" onclick="distributeExactEvenly()" class="text-[11px] font-bold text-indigo-600 hover:underline">Distribute Evenly</button>
            </div>
            <div id="splitExactInputsList" class="space-y-2 max-h-44 overflow-y-auto p-1 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-800">
              <!-- Exact inputs rendered dynamically -->
            </div>
            <div id="splitExactValidationBanner" class="p-2 rounded-xl text-xs flex items-center justify-between bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-200">
              <span id="splitExactSumText">Allocated: ₹0.00 / Target: ₹0.00</span>
              <span id="splitExactDiffText" class="font-bold">Remaining: ₹0.00</span>
            </div>
          </div>

          <!-- Split Container 3: Item-by-Item Split Mode -->
          <div id="splitItemsContainer" class="hidden space-y-2">
            <div class="flex items-center justify-between text-xs text-slate-500">
              <span>Assign line items to specific members:</span>
              <button type="button" onclick="addNewLineItemRow()" class="text-xs font-bold text-indigo-600 hover:underline">+ Add Item</button>
            </div>
            <div id="splitLineItemsTable" class="space-y-2 max-h-48 overflow-y-auto p-1 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-800">
              <!-- Dynamic line item rows -->
            </div>
            <div class="p-2 rounded-xl bg-purple-50 dark:bg-purple-950/50 border border-purple-200 dark:border-purple-800 text-xs text-purple-800 dark:text-purple-200 flex items-center justify-between">
              <span>Total of all items:</span>
              <span id="splitItemsSumDisplay" class="font-bold text-sm">₹0.00</span>
            </div>
          </div>
        </div>

        <!-- RECURRING EXPENSE TOGGLE -->
        <div class="p-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200/80 dark:border-slate-800 rounded-2xl">
          <label class="flex items-center justify-between cursor-pointer">
            <div class="flex items-center gap-2">
              <span class="text-base">🔁</span>
              <div>
                <span class="text-xs font-bold text-slate-800 dark:text-slate-200 block">Make Recurring Expense</span>
                <span class="text-[11px] text-slate-400">Monthly Room Rent, Wi-Fi, Maid, Subscriptions</span>
              </div>
            </div>
            <input type="checkbox" id="expenseRecurringToggle" onchange="toggleRecurringOptions(this.checked)" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500 border-slate-300 dark:border-slate-600">
          </label>

          <!-- Recurring Cycle & Next Due Date (Hidden unless checked) -->
          <div id="recurringOptionsRow" class="hidden mt-3 pt-3 border-t border-slate-200 dark:border-slate-700 grid grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Recurrence Cycle</label>
              <select id="recurringCycleSelect" class="w-full bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-xl px-2.5 py-1.5 font-semibold">
                <option value="monthly">Monthly Cycle</option>
                <option value="weekly">Weekly Cycle</option>
              </select>
            </div>
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Next Due Date</label>
              <input type="date" id="recurringNextDueDate" class="w-full bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-xl px-2.5 py-1.5">
            </div>
          </div>
        </div>

        <!-- Submit & Cancel Buttons -->
        <div class="flex items-center justify-end gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <button type="button" onclick="closeExpenseModal()" class="px-4 py-2.5 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition">
            Cancel
          </button>
          <button type="submit" id="saveExpenseBtn" class="px-5 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 rounded-xl shadow-md shadow-indigo-600/30 transition">
            Save Expense
          </button>
        </div>

      </form>
    </div>
  </div>

  <!-- ADD RECURRING BILL MODAL -->
  <div id="addRecurringModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">New Recurring Bill</h3>
        <button onclick="closeAddRecurringModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <form onsubmit="handleCreateRecurringBill(event)" class="mt-4 space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Bill Name *</label>
          <input type="text" id="recBillTitle" required placeholder="e.g. Monthly Room Rent" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white">
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Amount *</label>
            <input type="number" step="0.01" id="recBillAmount" required placeholder="0.00" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white font-bold">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Category</label>
            <select id="recBillCategory" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2 py-2">
              <option value="Rent">🏠 Rent</option>
              <option value="Utilities">⚡ Utilities</option>
              <option value="Groceries">🛒 Groceries</option>
              <option value="Food">🍽️ Food</option>
              <option value="Entertainment">🎬 OTT / Sub</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Cycle</label>
            <select id="recBillCycle" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2 py-2">
              <option value="monthly">Monthly</option>
              <option value="weekly">Weekly</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Paid By</label>
            <select id="recBillPayer" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2 py-2">
              <!-- Dynamic members -->
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="closeAddRecurringModal()" class="px-4 py-2 text-xs font-semibold text-slate-500">Cancel</button>
          <button type="submit" class="px-4 py-2 text-xs font-bold bg-teal-600 hover:bg-teal-700 text-white rounded-xl shadow-sm">Create Recurring Bill</button>
        </div>
      </form>
    </div>
  </div>

  <!-- USER IDENTITY MODAL ("WHO ARE YOU?") -->
  <div id="userIdentifyModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-2xl bg-indigo-50 dark:bg-indigo-950/70 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-xl shadow-sm">
            👋
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Who are you?</h3>
            <p id="userIdentifyModalSubtitle" class="text-xs text-slate-500">Pick your name in this group</p>
          </div>
        </div>
        <button onclick="closeUserIdentifyModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div id="userIdentifyMembersGrid" class="grid grid-cols-2 gap-2 my-4 max-h-56 overflow-y-auto">
        <!-- Rendered by JS -->
      </div>
      <form onsubmit="handleJoinAsNewMember(event)" class="pt-3 border-t border-slate-100 dark:border-slate-800 flex gap-2">
        <input type="text" id="joinNewMemberNameInput" placeholder="Join as new member..." class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white">
        <button type="submit" class="text-xs font-bold px-3 py-2 bg-indigo-600 text-white rounded-xl shadow-sm shrink-0">Join</button>
      </form>
    </div>
  </div>

  <!-- INDIVIDUAL SETTLEMENT MODAL ("SETTLE MY SHARE") -->
  <div id="settleShareModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-lg w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2.5">
          <span class="text-xl">🤝</span>
          <div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Settle Balances & Dues</h3>
            <p id="settleModalSubtitle" class="text-xs text-slate-500">Instant 1-to-1 settlement with direct UPI payments</p>
          </div>
        </div>
        <button onclick="closeSettleShareModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div id="settleModalContent" class="my-4 space-y-3">
        <!-- Rendered dynamically via JS -->
      </div>
    </div>
  </div>

  <!-- EDIT / RENAME MEMBER MODAL -->
  <div id="renameMemberModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Rename Member</h3>
        <button onclick="closeRenameMemberModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <form onsubmit="handleSaveRenameMember(event)" class="mt-4 space-y-3">
        <input type="hidden" id="oldMemberNameHidden" value="">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">New Name</label>
          <input type="text" id="renameMemberInput" required class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-slate-900 dark:text-white">
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="closeRenameMemberModal()" class="px-4 py-2 text-xs font-semibold text-slate-500">Cancel</button>
          <button type="submit" class="px-4 py-2 text-xs font-bold bg-indigo-600 text-white rounded-xl shadow-sm">Save</button>
        </div>
      </form>
    </div>
  </div>

  <!-- SHARE GROUP & ROOM CODE MODAL -->
  <div id="shareModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 text-center">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 text-left">
        <div>
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Share Group Room</h3>
          <p class="text-xs text-slate-500">Scan or copy to open instantly</p>
        </div>
        <button onclick="closeShareModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="my-4">
        <span class="text-xs text-slate-400 uppercase tracking-wider block font-bold">Room Code</span>
        <span id="shareModalRoomCode" class="text-2xl font-mono font-extrabold text-indigo-600 dark:text-indigo-400 mt-1 block">ROOM-101</span>
      </div>
      <div class="p-3 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 mx-auto w-44 h-44 mb-3 flex items-center justify-center shadow-inner">
        <div id="qrcodeCanvas"></div>
      </div>
      <div class="flex gap-2">
        <input type="text" id="shareModalLinkInput" readonly class="w-full text-xs bg-slate-100 dark:bg-slate-800 rounded-xl px-3 py-2 font-mono text-slate-600 dark:text-slate-300">
        <button onclick="copyGroupShareLink()" class="px-3 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold shrink-0">Copy</button>
      </div>
    </div>
  </div>

  <!-- SWITCH OR CREATE GROUP MODAL -->
  <div id="groupSwitchModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-sm w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Switch or New Group</h3>
        <button onclick="closeGroupSwitchModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="flex border-b border-slate-200 dark:border-slate-700 my-3 text-xs font-bold">
        <button onclick="switchGroupModalTab('create')" id="tabCreateGroupBtn" class="flex-1 py-2 border-b-2 border-indigo-600 text-indigo-600">Create New</button>
        <button onclick="switchGroupModalTab('join')" id="tabJoinGroupBtn" class="flex-1 py-2 border-b-2 border-transparent text-slate-400">Join Room</button>
      </div>
      <form id="createGroupTabForm" onsubmit="handleCreateNewGroup(event)" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Group Name</label>
          <input type="text" id="newGroupNameInput" required placeholder="e.g. Goa Trip 2026" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Initial Members (comma-separated)</label>
          <input type="text" id="newGroupMembersInput" placeholder="Rahul, Amit, Pooja" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white">
        </div>
        <button type="submit" class="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm">Create Group</button>
      </form>
      <form id="joinGroupTabForm" onsubmit="handleJoinByRoomCode(event)" class="hidden space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Enter Room Code</label>
          <input type="text" id="joinRoomCodeInput" required placeholder="e.g. ROOM-101" class="w-full text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white font-mono uppercase">
        </div>
        <button type="submit" class="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm">Join Group</button>
      </form>
    </div>
  </div>

  <!-- FIREBASE CLOUD STORAGE CONFIG MODAL -->
  <div id="cloudModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-md w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl transform scale-95 transition-transform duration-200 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-base font-bold text-slate-900 dark:text-white">Firebase Cloud Settings</h3>
        <button onclick="closeCloudModal()" class="p-1 rounded-lg text-slate-400 hover:text-slate-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="my-3 p-3 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800 text-xs">
        <strong id="cloudModalStatusTitle" class="block font-bold text-emerald-800 dark:text-emerald-200">Firebase Live Active</strong>
        <p id="cloudModalStatusDesc" class="text-emerald-700 dark:text-emerald-300 mt-0.5">Syncs across multiple phones and tabs in real time.</p>
      </div>
      <form onsubmit="handleSaveFirebaseConfig(event)" class="space-y-2 text-xs">
        <div>
          <label class="block font-semibold text-slate-600 dark:text-slate-400 mb-1">API Key</label>
          <input type="text" id="fbApiKey" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 font-mono">
        </div>
        <div>
          <label class="block font-semibold text-slate-600 dark:text-slate-400 mb-1">Project ID</label>
          <input type="text" id="fbProjectId" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 font-mono">
        </div>
        <div>
          <label class="block font-semibold text-slate-600 dark:text-slate-400 mb-1">Auth Domain</label>
          <input type="text" id="fbAuthDomain" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 font-mono">
        </div>
        <div>
          <label class="block font-semibold text-slate-600 dark:text-slate-400 mb-1">App ID</label>
          <input type="text" id="fbAppId" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 font-mono">
        </div>
        <div class="flex justify-between items-center pt-3">
          <button type="button" onclick="clearFirebaseConfig()" class="text-xs text-rose-500 hover:underline">Disconnect Cloud</button>
          <button type="submit" class="px-4 py-2 bg-indigo-600 text-white font-bold rounded-xl shadow-sm">Save & Connect</button>
        </div>
      </form>
    </div>
  </div>

  <!-- DOCKED FLOATING BOTTOM QUICK CALCULATOR WIDGET (RULE PRESERVED INTACT) -->
  <div id="calculatorWidget" class="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-40 select-none">
    
    <!-- Expanded Calculator Drawer / Panel -->
    <div id="calcExpandedPanel" class="hidden mb-3 bg-white dark:bg-slate-900 rounded-3xl p-4 sm:p-5 border border-slate-200 dark:border-slate-800 shadow-2xl w-80 sm:w-88 transform transition-all duration-200 origin-bottom-right scale-95 opacity-0 pointer-events-none">
      
      <!-- Top Title & Controls -->
      <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2">
          <span class="text-lg">🧮</span>
          <span class="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">Quick Bill Calculator</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span id="calcCurrencyBadge" class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 font-bold">₹ INR</span>
          <button type="button" onclick="toggleCalculator(false)" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Calculator Display Screen -->
      <div class="my-3 p-3 bg-slate-50 dark:bg-slate-800/80 rounded-2xl border border-slate-200/80 dark:border-slate-700 text-right">
        <div id="calcExpressionDisplay" class="text-xs font-mono text-slate-400 h-4 truncate">0</div>
        <div class="flex items-baseline justify-end gap-1 mt-1">
          <span id="calcDisplayPrefix" class="text-xs text-indigo-600 dark:text-indigo-400 font-bold">₹</span>
          <span id="calcResultDisplay" class="text-2xl font-mono font-extrabold text-slate-900 dark:text-white tracking-tight">0.00</span>
        </div>
      </div>

      <!-- Quick Bill Split / Tip Chips -->
      <div class="flex items-center gap-1.5 pb-2.5 overflow-x-auto no-scrollbar text-[11px] font-semibold text-slate-600 dark:text-slate-300">
        <button type="button" onclick="calcAppendPreset('/2')" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 shrink-0">÷2</button>
        <button type="button" onclick="calcAppendPreset('/3')" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 shrink-0">÷3</button>
        <button type="button" onclick="calcAppendPreset('/4')" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 shrink-0">÷4</button>
        <button type="button" onclick="calcAppendPreset('+5%')" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 shrink-0">+5% Tip</button>
        <button type="button" onclick="calcAppendPreset('+10%')" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 shrink-0">+10% Tip</button>
      </div>

      <!-- Insert into Amount Button (RULE PRESERVED) -->
      <button type="button" onclick="insertCalcResultIntoAmount()" class="w-full mb-3 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:scale-98 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition flex items-center justify-center gap-1.5">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        <span>Insert into Expense Amount</span>
      </button>

      <!-- Calculator Keypad (4x5 Grid) -->
      <div class="grid grid-cols-4 gap-1.5 text-xs font-bold">
        <button type="button" onclick="calcClear()" class="p-2.5 rounded-xl bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 hover:bg-rose-100">C</button>
        <button type="button" onclick="calcBackspace()" class="p-2.5 rounded-xl bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200">⌫</button>
        <button type="button" onclick="calcOperator('%')" class="p-2.5 rounded-xl bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200">%</button>
        <button type="button" onclick="calcOperator('/')" class="p-2.5 rounded-xl bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 hover:bg-indigo-100">÷</button>

        <button type="button" onclick="calcNumber('7')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">7</button>
        <button type="button" onclick="calcNumber('8')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">8</button>
        <button type="button" onclick="calcNumber('9')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">9</button>
        <button type="button" onclick="calcOperator('*')" class="p-2.5 rounded-xl bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 hover:bg-indigo-100">×</button>

        <button type="button" onclick="calcNumber('4')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">4</button>
        <button type="button" onclick="calcNumber('5')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">5</button>
        <button type="button" onclick="calcNumber('6')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">6</button>
        <button type="button" onclick="calcOperator('-')" class="p-2.5 rounded-xl bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 hover:bg-indigo-100">−</button>

        <button type="button" onclick="calcNumber('1')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">1</button>
        <button type="button" onclick="calcNumber('2')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">2</button>
        <button type="button" onclick="calcNumber('3')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">3</button>
        <button type="button" onclick="calcOperator('+')" class="p-2.5 rounded-xl bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 hover:bg-indigo-100">+</button>

        <button type="button" onclick="calcNumber('0')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">0</button>
        <button type="button" onclick="calcNumber('00')" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">00</button>
        <button type="button" onclick="calcDecimal()" class="p-2.5 rounded-xl bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100 hover:bg-slate-200">.</button>
        <button type="button" onclick="calcEquals()" class="p-2.5 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm">=</button>
      </div>

    </div>

    <!-- Collapsed Bottom Floating Pill / Button -->
    <button type="button" onclick="toggleCalculator()" class="flex items-center gap-2.5 px-4 py-3 rounded-full bg-slate-900/90 dark:bg-indigo-600/95 hover:bg-indigo-600 text-white shadow-2xl backdrop-blur-md border border-slate-700/80 dark:border-indigo-500/50 transition-all transform hover:scale-105 active:scale-95 group">
      <span class="text-base sm:text-lg">🧮</span>
      <div class="text-left pr-1">
        <span class="text-[10px] text-slate-300 dark:text-indigo-200 block font-semibold leading-none">Bill Calc</span>
        <span id="calcPillPreview" class="text-xs font-mono font-extrabold text-white leading-none mt-0.5 block">₹0.00</span>
      </div>
      <svg id="calcChevronIcon" class="w-4 h-4 text-slate-400 group-hover:text-white transition transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/>
      </svg>
    </button>

  </div>

  <!-- TOAST NOTIFICATIONS CONTAINER -->
  <div id="toastContainer" class="fixed top-20 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>
"""
