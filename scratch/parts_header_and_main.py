# Header and Main Sections
BODY_TOP = r"""<body class="bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 min-h-full font-sans antialiased transition-colors duration-200 pb-20 sm:pb-16">

  <!-- TOP APP HEADER -->
  <header class="sticky top-0 z-30 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-2">
        
        <!-- Left: Logo & Room Pill -->
        <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
          <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 shrink-0">
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 sm:gap-2">
              <span class="font-extrabold text-lg sm:text-xl tracking-tight bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">FairShare</span>
              <!-- Cloud Status Pill -->
              <button onclick="openCloudModal()" id="cloudStatusBtn" class="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 hover:ring-2 hover:ring-emerald-400/40 transition shrink-0" title="Click to configure Cloud Firestore / view sync status">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 pulse-subtle" id="cloudStatusDot"></span>
                <span id="cloudStatusText">Live Sync</span>
              </button>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 truncate hidden sm:block">AI OCR • UPI Settlement • Direct Pair Debt Splitter</p>
          </div>
        </div>

        <!-- Center Nav Tabs (Desktop) -->
        <nav class="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-slate-800/80 p-1 rounded-2xl border border-slate-200 dark:border-slate-700/60 text-xs font-semibold">
          <button onclick="switchMainTab('debts')" id="tabNavDebts" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm font-bold">
            <span>💸</span>
            <span>Debts & Bills</span>
          </button>
          <button onclick="switchMainTab('analytics')" id="tabNavAnalytics" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
            <span>📈</span>
            <span>Analytics</span>
          </button>
          <button onclick="switchMainTab('recurring')" id="tabNavRecurring" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
            <span>🔁</span>
            <span>Recurring Bills</span>
            <span id="badgeRecurringNavCount" class="w-4 h-4 text-[10px] rounded-full bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300 flex items-center justify-center font-bold">0</span>
          </button>
        </nav>

        <!-- Right Header Actions -->
        <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
          
          <!-- Currency Selector -->
          <div class="relative">
            <select id="currencySelector" onchange="changeCurrency(this.value)" class="text-xs sm:text-sm font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-2 sm:px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
              <option value="₹">₹ INR</option>
              <option value="$">$ USD</option>
              <option value="€">€ EUR</option>
              <option value="£">£ GBP</option>
              <option value="AED">AED</option>
              <option value="¥">¥ JPY</option>
            </select>
          </div>

          <!-- Quick Calc Button in Header -->
          <button onclick="toggleCalculator()" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-slate-800 transition" title="Toggle Quick Calculator">
            <span class="text-base sm:text-lg">🧮</span>
          </button>

          <!-- Dark/Light Mode Button -->
          <button onclick="toggleDarkMode()" class="p-2 rounded-xl text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition" title="Toggle Dark/Light Mode">
            <svg id="sunIcon" class="w-4 h-4 sm:w-5 sm:h-5 hidden dark:block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg id="moonIcon" class="w-4 h-4 sm:w-5 sm:h-5 block dark:hidden text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>

          <!-- AUTHENTICATION PROFILE / SIGN IN BUTTON -->
          <div id="authNavContainer" class="relative">
            <!-- Rendered dynamically: either Sign In button or User Profile Pill -->
          </div>

          <!-- Primary Add Expense Button -->
          <button onclick="openExpenseModal()" class="inline-flex items-center gap-1.5 px-3 py-2 sm:px-4 sm:py-2 rounded-xl text-xs sm:text-sm font-bold bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white shadow-md shadow-indigo-600/30 transition transform hover:-translate-y-0.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Add Expense</span>
            <span class="sm:hidden">Add</span>
          </button>

        </div>
      </div>
    </div>

    <!-- Mobile Sub-Nav Tab Bar -->
    <div class="flex md:hidden items-center justify-around border-t border-slate-100 dark:border-slate-800/80 bg-white dark:bg-slate-900 px-2 py-1.5 text-xs font-semibold">
      <button onclick="switchMainTab('debts')" id="mobileNavDebts" class="flex items-center gap-1 py-1 px-3 rounded-lg text-indigo-600 dark:text-indigo-400 font-bold bg-indigo-50 dark:bg-indigo-950/60">
        <span>💸</span>
        <span>Debts</span>
      </button>
      <button onclick="switchMainTab('analytics')" id="mobileNavAnalytics" class="flex items-center gap-1 py-1 px-3 rounded-lg text-slate-600 dark:text-slate-400">
        <span>📈</span>
        <span>Analytics</span>
      </button>
      <button onclick="switchMainTab('recurring')" id="mobileNavRecurring" class="flex items-center gap-1 py-1 px-3 rounded-lg text-slate-600 dark:text-slate-400">
        <span>🔁</span>
        <span>Recurring</span>
      </button>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 space-y-6 pb-24 sm:pb-20">

    <!-- ACTIVE GROUP BAR & CONTROLS -->
    <section class="bg-gradient-to-r from-indigo-500/10 via-purple-500/10 to-pink-500/5 dark:from-indigo-950/40 dark:via-purple-950/30 dark:to-slate-900 border border-indigo-200/60 dark:border-indigo-900/60 rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
      <div class="flex items-start sm:items-center gap-3">
        <div class="w-12 h-12 rounded-2xl bg-indigo-600 text-white font-extrabold flex items-center justify-center text-xl shadow-md shadow-indigo-500/30 shrink-0">
          <span id="groupIcon">👥</span>
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h1 id="groupNameHeading" class="text-lg sm:text-xl font-extrabold text-slate-900 dark:text-white">Shared Expenses</h1>
            <!-- Room Code Badge -->
            <button onclick="copyRoomCode()" class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 hover:bg-indigo-200 dark:hover:bg-indigo-800/80 text-indigo-800 dark:text-indigo-200 text-xs font-mono font-bold border border-indigo-200 dark:border-indigo-700/60 transition" title="Click to copy Room Code">
              <span>Code:</span>
              <span id="roomCodeBadge">ROOM-101</span>
              <svg class="w-3.5 h-3.5 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
            </button>
            <span class="text-xs text-slate-400">·</span>
            <span id="groupSyncTimestamp" class="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Real-time sync active</span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Share room code with members. Supports receipt camera OCR, instant UPI settlement, and custom splits.</p>
        </div>
      </div>

      <!-- Group Action Buttons -->
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="openShareModal()" class="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 transition shadow-sm">
          <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/></svg>
          <span>QR & Link</span>
        </button>

        <button onclick="openReceiptScannerModal()" class="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 dark:bg-amber-950/70 dark:hover:bg-amber-900/80 text-amber-800 dark:text-amber-200 border border-amber-300 dark:border-amber-700 transition shadow-sm" title="Scan receipt with OCR">
          <span>📸</span>
          <span>Scan Receipt</span>
        </button>

        <button onclick="openGroupSwitchModal()" class="inline-flex items-center gap-1 px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition" title="Switch Group or Join Another Room">
          <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          <span>Switch / New</span>
        </button>

        <button onclick="openSettleShareModal()" class="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/70 dark:hover:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 border border-emerald-300/80 dark:border-emerald-700 transition shadow-sm" title="Settle individual balances without deleting bills">
          <span>🤝</span>
          <span>Settle Up</span>
        </button>
      </div>
    </section>

    <!-- METRICS DASHBOARD CARDS -->
    <section class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      
      <!-- Total Group Expense -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm relative overflow-hidden">
        <div class="flex items-center justify-between">
          <p class="text-xs sm:text-sm font-semibold text-slate-500 dark:text-slate-400">Total Group Expense</p>
          <div class="w-8 h-8 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <span id="metricTotalExpense" class="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">₹0.00</span>
        </div>
        <div class="mt-1 text-xs text-slate-400">Across all recorded bills</div>
      </div>

      <!-- Average Per Person -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm relative overflow-hidden">
        <div class="flex items-center justify-between">
          <p class="text-xs sm:text-sm font-semibold text-slate-500 dark:text-slate-400">Average / Person</p>
          <div class="w-8 h-8 rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7 7z"/></svg>
          </div>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <span id="metricAvgPerPerson" class="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">₹0.00</span>
        </div>
        <div class="mt-1 text-xs text-slate-400" id="metricAvgSubtitle">Equal split benchmark</div>
      </div>

      <!-- Active Group Members -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm relative overflow-hidden">
        <div class="flex items-center justify-between">
          <p class="text-xs sm:text-sm font-semibold text-slate-500 dark:text-slate-400">Group Members</p>
          <div class="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <span id="metricMemberCount" class="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">3</span>
          <span class="text-xs text-slate-500 font-medium">people</span>
        </div>
        <div class="mt-1 text-xs text-slate-400">Min 3 members required</div>
      </div>

      <!-- Direct Pair Settlements -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm relative overflow-hidden">
        <div class="flex items-center justify-between">
          <p class="text-xs sm:text-sm font-semibold text-slate-500 dark:text-slate-400">Direct Pair Debts</p>
          <div class="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          </div>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <span id="metricSettlementTransCount" class="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">0</span>
          <span class="text-xs text-emerald-600 dark:text-emerald-400 font-semibold" id="metricSettlementStatus">Settled</span>
        </div>
        <div class="mt-1 text-xs text-slate-400">Exact direct pair settlements</div>
      </div>

    </section>
"""
