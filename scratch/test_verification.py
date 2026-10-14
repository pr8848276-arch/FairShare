with open('c:/c+++/index.html', encoding='utf-8') as f:
    content = f.read()

required_ids = [
    'authModal', 'authGoogleTabContent', 'authEmailTabContent',
    'receiptScannerModal', 'receiptFileInput', 'ocrScanningStatus', 'ocrResultReview',
    'upiPaymentModal', 'upiDeepLinkBtn', 'upiQrcodeCanvas', 'setUpiModal',
    'expenseModal', 'expenseRecurringToggle', 'splitModeBtnEqual', 'splitModeBtnExact', 'splitModeBtnItems',
    'tabContentDebts', 'tabContentAnalytics', 'tabContentRecurring',
    'categoryChart', 'memberSpendChart', 'recurringBillsContainer',
    'calculatorWidget', 'calcExpandedPanel', 'calcExpressionDisplay', 'calcResultDisplay'
]

missing = [i for i in required_ids if f'id="{i}"' not in content and f"id='{i}'" not in content]
if missing:
    print('Missing IDs:', missing)
else:
    print('All 26 key interactive elements and modals present!')

required_fns = [
    'handleGoogleSignIn', 'handleEmailAuthSubmit', 'loginAsDemoUser', 'handleLogOut',
    'openReceiptScannerModal', 'handleReceiptFileSelected', 'parseOcrReceiptText', 'applyOcrToExpenseForm',
    'openPayViaUpiModal', 'handleSaveMemberUpi', 'setSplitMode', 'renderExactSplitInputs', 'renderLineItemsTable',
    'handleCreateRecurringBill', 'postRecurringExpenseForCycle', 'renderRecurringBills',
    'renderAnalyticsCharts', 'calculateDirectPairDebts', 'insertCalcResultIntoAmount'
]

missing_fns = [fn for fn in required_fns if f'function {fn}' not in content and f'async function {fn}' not in content]
if missing_fns:
    print('Missing functions:', missing_fns)
else:
    print('All 19 core workflow functions verified!')
