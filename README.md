# FairShare — Smart Shared Expense Splitter, AI OCR & Instant Settlement App

FairShare is a modern, responsive, real-time shared expense splitting web application designed for roommates, group trips, and shared events. It provides Google & Email/Password authentication, AI camera receipt scanning (OCR), 1-click Indian UPI payments (Google Pay, PhonePe, Paytm), custom split modes (Equal, Exact, and Item-by-Item), automated recurring bills, visual analytics with Chart.js, strict direct pair-to-pair debt settlement, and an integrated floating quick calculator.

---

## ✨ Advanced Features

### 1. 🔐 Secure Authentication (Google & Email/Password)
- **Landing / Auth Modal**: Clean, responsive onboarding and sign-in modal.
- **Two Auth Options**:
  - **'Continue with Google'** via Firebase Auth popup.
  - **Email and Password** registration and sign-in.
  - **Instant One-Click Demo Mode** for testing without Firebase Auth configuration delays.
- **User Profile in Navigation**: Displays avatar, display name, email, member switcher, and 'Log Out' button.
- **Private Group Access**: Authenticated group membership ensuring only participants view and record expenses.

### 2. 📸 AI Receipt & Bill Scanner (Camera / Upload OCR)
- **Camera & File Upload**: Snap photos on mobile or upload receipt/bill images directly from disk.
- **Client-Side AI OCR**: Powered by Tesseract.js (via CDN) with animated laser-scanning indicator.
- **Smart Extraction**: Auto-extracts merchant name, total bill amount, and line items using robust regex pattern matching.
- **Review & Edit**: Review extracted values before applying, with 1-click import into **Item-by-Item Split** mode.

### 3. ⚡ Direct UPI 'Pay Now' Deep Links (India Payments)
- **Save Member UPI IDs**: Store VPAs (e.g., `user@okhdfcbank`, `9876543210@paytm`) for each member.
- **Prominent 'Pay via UPI' Button**: Added to every pending debt card in the "Who Owes Whom" settlement section.
- **Valid UPI Deep Link**: Triggers `upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}` so mobile users open Google Pay, PhonePe, or Paytm with 1 click.
- **Interactive QR Code Dialog**: On desktop, generates a dynamic UPI QR code with QRCode.js so users can scan and pay with their phone UPI app instantly.

### 4. 🎛 Flexible Split Options (Custom Split Modes)
- **Equal Split (Default)**: Divides total amount equally among selected members (1/N).
- **Exact Amount**: Enter custom amounts per member with real-time balance validation ensuring the sum matches the total bill.
- **Item-by-Item Split**: Assign specific dishes, groceries, or OCR-extracted items directly to the individuals who consumed them, with automatic total recalculation.

### 5. 🔁 Recurring Expenses (Subscriptions & Monthly Bills)
- **Recurring Toggle**: Flag recurring dues in the expense form (Room Rent, Wi-Fi, Maid, Netflix/Spotify).
- **Cycle & Due Dates**: Set Monthly or Weekly recurrence and track next due date.
- **Dedicated 'Recurring Bills' View**: Card grid displaying upcoming dues with a 1-click **'⚡ Post Expense for this Month'** action that logs the expense and advances the billing cycle automatically.

### 6. 📈 Spending Insights & Category Analytics
- **Curated Category Selector**:
  - 🍽️ Food & Dining
  - 🏠 Rent & Living
  - 🚗 Travel & Transport
  - 🛒 Groceries & Snacks
  - ⚡ Utilities & Bills
  - 🎬 Entertainment & OTT
  - 🤝 Settlements
  - 📦 Other
- **Visual Analytics Dashboard** (Chart.js via CDN):
  - **Category Breakdown**: Interactive responsive Doughnut chart showing percentage and amount by category.
  - **Spend by Member**: Bar chart comparing who paid upfront vs who consumed what.
  - **KPI Metrics**: Top Category, Biggest Spender, Total Group Outflow, Average Bill Size.

---

## 🔒 Core Rules Preserved

1. **Docked Floating Quick Calculator**: Kept intact with arithmetic operations, percentage tips, and the **"Insert into Expense Amount"** button.
2. **Strict Direct Pair-to-Pair Debts**: Direct 1-to-1 netting between debtor and creditor with **zero third-party debt routing** or simplification.
3. **Immutable Expense History**: Permanent financial audit log with no deletion of past records.
4. **Mobile-First Responsive Layout**: Tailwind CSS styling with smooth tab navigation and light/dark theme.

---

## 🚀 Getting Started

Simply open `index.html` in any modern web browser or serve it locally:

```bash
python -m http.server 8080
```

Then visit [http://localhost:8080/index.html](http://localhost:8080/index.html).

