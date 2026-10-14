# Tabs for Debts, Analytics, and Recurring Bills
TABS_HTML = r"""
    <!-- TAB 1: DEBTS & EXPENSES VIEW -->
    <div id="tabContentDebts" class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- LEFT COLUMN: MEMBER MANAGEMENT & INDIVIDUAL BALANCES (4 cols on lg) -->
      <section class="lg:col-span-4 space-y-6">

        <!-- MEMBER MANAGEMENT CARD (WITH UPI IDS) -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <span>Group Members</span>
                <span id="badgeMemberTotal" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">3</span>
              </h2>
              <p class="text-xs text-slate-500">Add, rename, or set member UPI IDs</p>
            </div>
            <button onclick="toggleAddMemberInput()" class="text-xs font-bold px-3 py-1.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/70 dark:hover:bg-indigo-900/80 text-indigo-700 dark:text-indigo-300 border border-indigo-200/70 dark:border-indigo-800 transition flex items-center gap-1">
              <span>+ Add</span>
            </button>
          </div>

          <!-- Add Member Inline Input -->
          <form id="addMemberForm" onsubmit="handleAddMember(event)" class="mb-3 hidden">
            <div class="flex items-center gap-2">
              <input type="text" id="newMemberNameInput" placeholder="Member name (e.g. Sneha)" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <button type="submit" class="text-xs font-bold px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-sm shrink-0">
                Add
              </button>
            </div>
          </form>

          <!-- Members List -->
          <div id="membersList" class="space-y-2">
            <!-- Rendered dynamically via JS -->
          </div>
        </div>

        <!-- INDIVIDUAL NET BALANCES CARD -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <div>
              <h2 class="text-base font-bold text-slate-900 dark:text-white">Individual Balances</h2>
              <p class="text-xs text-slate-500">Individual net status and settlement actions</p>
            </div>
            <button onclick="openSettleShareModal()" class="text-xs font-bold text-emerald-600 dark:text-emerald-400 hover:underline">
              Settle Share
            </button>
          </div>

          <!-- Balances List -->
          <div id="individualBalancesList" class="space-y-2.5 mt-3">
            <!-- Rendered dynamically via JS -->
          </div>
        </div>

        <!-- RECENT GROUPS & SWITCHER -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Saved Groups on this Device</h3>
          <div id="recentGroupsList" class="space-y-1.5">
            <!-- Rendered dynamically -->
          </div>
        </div>

      </section>

      <!-- RIGHT COLUMN: DIRECT PAIR SETTLEMENT & EXPENSE HISTORY (8 cols on lg) -->
      <section class="lg:col-span-8 space-y-6">

        <!-- DIRECT PAIR-TO-PAIR SETTLEMENT SECTION (WHO OWES WHOM WITH UPI PAY) -->
        <div class="bg-gradient-to-br from-indigo-900 via-indigo-950 to-slate-900 rounded-3xl p-5 sm:p-6 text-white shadow-xl border border-indigo-800/60 relative overflow-hidden">
          <div class="relative z-10">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
              <div>
                <div class="flex items-center gap-2">
                  <span class="p-1.5 bg-indigo-500/30 rounded-xl text-indigo-300 border border-indigo-400/30">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                  </span>
                  <h2 class="text-lg font-bold tracking-tight">Direct Pair-to-Pair Settlement (Who Owes Whom)</h2>
                </div>
                <p class="text-xs text-indigo-200 mt-0.5">Strict 1-to-1 pair debts with instant UPI Pay deep links (Google Pay, PhonePe, Paytm)</p>
              </div>

              <!-- Settlement Actions -->
              <div class="flex items-center gap-2 self-start sm:self-auto">
                <button onclick="copySettlementSummary()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 text-white border border-white/15 backdrop-blur-sm transition active:scale-95" title="Copy clean WhatsApp summary">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                  <span>WhatsApp</span>
                </button>
                <button onclick="downloadCSVReport()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 text-white border border-white/15 backdrop-blur-sm transition active:scale-95" title="Export as CSV spreadsheet">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                  <span>Export CSV</span>
                </button>
              </div>
            </div>

            <!-- Settlement Result Cards Container -->
            <div id="settlementPlanContainer" class="mt-4 space-y-3">
              <!-- Rendered via JS -->
            </div>
          </div>
        </div>

        <!-- EXPENSES HISTORY & MANAGEMENT -->
        <div class="bg-white dark:bg-slate-900 rounded-3xl p-5 border border-slate-200/90 dark:border-slate-800 shadow-sm">
          
          <!-- History Header & Controls -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-base font-bold text-slate-900 dark:text-white">Expense History</h2>
                <span id="badgeExpenseCount" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/70 text-indigo-700 dark:text-indigo-300">0 bills</span>
              </div>
              <p class="text-xs text-slate-500">Live synchronized • Permanent audit log (immutable history)</p>
            </div>

            <!-- Search & Filters -->
            <div class="flex flex-wrap items-center gap-2">
              <!-- Search -->
              <div class="relative flex-1 sm:w-44">
                <input type="text" id="expenseSearchInput" oninput="handleSearchExpenses(this.value)" placeholder="Search bills..." class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl pl-8 pr-3 py-1.5 text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              </div>

              <!-- Filter by Category -->
              <select id="categoryFilter" onchange="handleCategoryFilter(this.value)" class="text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2.5 py-1.5 text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
                <option value="ALL">All Categories</option>
                <option value="Food">🍽️ Food & Dining</option>
                <option value="Rent">🏠 Rent & Living</option>
                <option value="Travel">🚗 Travel & Transport</option>
                <option value="Groceries">🛒 Groceries</option>
                <option value="Utilities">⚡ Utilities</option>
                <option value="Entertainment">🎬 Entertainment</option>
                <option value="Settlement">🤝 Settlements</option>
                <option value="Other">📦 Other</option>
              </select>

              <!-- New Expense Button -->
              <button onclick="openExpenseModal()" class="text-xs font-bold px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition">
                + Add Expense
              </button>
            </div>
          </div>

          <!-- Expenses List -->
          <div id="expenseListContainer" class="space-y-3">
            <!-- Rendered dynamically -->
          </div>

        </div>

      </section>

    </div>

    <!-- TAB 2: VISUAL ANALYTICS & INSIGHTS VIEW -->
    <div id="tabContentAnalytics" class="hidden space-y-6">
      
      <!-- Analytics Summary Banner -->
      <div class="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 rounded-3xl p-5 sm:p-6 text-white shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-white/20 text-white uppercase tracking-wider">Visual Intelligence</span>
            <h2 class="text-xl sm:text-2xl font-extrabold mt-2">Spending Insights & Category Analytics</h2>
            <p class="text-xs sm:text-sm text-indigo-100 mt-1">Interactive breakdowns of group outflow, category distribution, and top spenders powered by Chart.js.</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="text-right">
              <span class="text-xs text-indigo-200 block">Total Active Outflow</span>
              <span id="analyticsTotalOutflow" class="text-2xl sm:text-3xl font-extrabold text-white">₹0.00</span>
            </div>
          </div>
        </div>

        <!-- 4 Analytics Metric Chips -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5 pt-4 border-t border-white/20">
          <div class="bg-white/10 rounded-2xl p-3 backdrop-blur-sm">
            <span class="text-[11px] text-indigo-200 block">Top Category</span>
            <span id="analyticsTopCategory" class="text-sm sm:text-base font-extrabold text-white truncate block">🍽️ Food</span>
          </div>
          <div class="bg-white/10 rounded-2xl p-3 backdrop-blur-sm">
            <span class="text-[11px] text-indigo-200 block">Biggest Spender</span>
            <span id="analyticsTopSpender" class="text-sm sm:text-base font-extrabold text-white truncate block">None</span>
          </div>
          <div class="bg-white/10 rounded-2xl p-3 backdrop-blur-sm">
            <span class="text-[11px] text-indigo-200 block">Average Bill Size</span>
            <span id="analyticsAvgBill" class="text-sm sm:text-base font-extrabold text-white truncate block">₹0.00</span>
          </div>
          <div class="bg-white/10 rounded-2xl p-3 backdrop-blur-sm">
            <span class="text-[11px] text-indigo-200 block">Settled Transactions</span>
            <span id="analyticsSettledCount" class="text-sm sm:text-base font-extrabold text-emerald-300 truncate block">0</span>
          </div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Doughnut Chart: Category Distribution (5 cols on lg) -->
        <div class="lg:col-span-5 bg-white dark:bg-slate-900 rounded-3xl p-5 sm:p-6 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span>Category Breakdown</span>
                </h3>
                <p class="text-xs text-slate-500">Distribution of group spend by category</p>
              </div>
              <span class="text-lg">🍩</span>
            </div>
            <div class="relative h-64 flex items-center justify-center">
              <canvas id="categoryChart"></canvas>
            </div>
          </div>
          <!-- Category List Legend -->
          <div id="categoryLegendContainer" class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 grid grid-cols-2 gap-2 text-xs">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- Bar Chart: Spend by Member (7 cols on lg) -->
        <div class="lg:col-span-7 bg-white dark:bg-slate-900 rounded-3xl p-5 sm:p-6 border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span>Spend & Contribution by Member</span>
                </h3>
                <p class="text-xs text-slate-500">Comparison of who paid vs who consumed</p>
              </div>
              <span class="text-lg">📊</span>
            </div>
            <div class="relative h-64">
              <canvas id="memberSpendChart"></canvas>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-500 flex items-center justify-between">
            <span>💡 Bars compare total upfront payment vs equal/custom share consumption.</span>
          </div>
        </div>

      </div>

    </div>

    <!-- TAB 3: RECURRING EXPENSES & SUBSCRIPTIONS VIEW -->
    <div id="tabContentRecurring" class="hidden space-y-6">
      
      <div class="bg-gradient-to-r from-emerald-600 via-teal-600 to-indigo-700 rounded-3xl p-5 sm:p-6 text-white shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-white/20 text-white uppercase tracking-wider">Automated Dues</span>
          <h2 class="text-xl sm:text-2xl font-extrabold mt-2">Recurring Bills & Subscriptions</h2>
          <p class="text-xs sm:text-sm text-teal-100 mt-1">Manage shared monthly bills (Room Rent, Wi-Fi, Maid, Netflix) with 1-click posting for current cycle dues.</p>
        </div>
        <button onclick="openAddRecurringModal()" class="px-4 py-2.5 bg-white text-teal-800 hover:bg-teal-50 font-bold text-xs sm:text-sm rounded-xl shadow-lg transition self-start sm:self-auto flex items-center gap-1.5 shrink-0">
          <span>+ Add Recurring Bill</span>
        </button>
      </div>

      <!-- Recurring Bills Cards Grid -->
      <div id="recurringBillsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Rendered dynamically via JS -->
      </div>

    </div>

  </main>
"""
