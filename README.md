# FairShare — Real-Time Shared Expense Splitter & Settlement App

FairShare is a modern, responsive, real-time shared expense splitting web application (like Splitwise) designed for roommates, group trips, and shared events. It enables multi-person expense tracking, instant link/Room Code sharing without logins or passwords, greedy debt simplification, and an integrated bottom-docked bill calculator.

---

## ✨ Features

- **🔗 Instant Group Sharing & Room Codes**:
  - Unique Room Codes (e.g., `ROOM-101`) and direct shareable links.
  - Interactive QR Code generator for quick camera scans on smartphones.
  - Join or create groups without logins or passwords.

- **🧮 Built-in Docked Bill Calculator**:
  - Docked bottom floating widget that easily expands/collapses.
  - Basic arithmetic operations: addition (`+`), subtraction (`−`), multiplication (`×`), division (`÷`), percentage (`%`), clear (`C`), backspace (`⌫`), equals (`=`).
  - Quick split & tip chips (`+5% Tip`, `+10% Tip`, `+18% GST`, `÷2`, `÷3`, `÷4`).
  - **"Insert into Expense Amount"**: One-click insertion into the expense amount field with automatic 1/N equal split preview recalculation.

- **👥 Member Management & History Integrity**:
  - Add members and inline rename members.
  - Renaming automatically cascades across all recorded expenses, paid-by records, split participant lists, net balances, and settlement plans.

- **📊 1/N Equal Splitting & Net Balances**:
  - Automatically calculates each member's share ($Amount / N$).
  - Computes real-time Individual Net Balances ($\text{Total Paid} - \text{Total Share}$).

- **🤝 Smart Debt Minimization ("Who Owes Whom")**:
  - Greedy Minimum Cash Flow algorithm simplifies debts down to the minimal number of direct transfers.
  - One-click "Mark Settled ✓" records settlement transactions cleanly.

- **⚡ Real-Time Cloud Sync**:
  - Firebase Firestore integration (`onSnapshot`) for cross-device live updates.
  - Cross-tab `BroadcastChannel` communication for instant local multi-tab synchronization.

- **🎨 Modern Responsive UI**:
  - Mobile-first Tailwind CSS theme with light/dark mode support.
  - Clean touch targets and smooth animations.

---

## 🚀 Getting Started

Simply open `index.html` in any modern web browser, or serve it locally:

```bash
python -m http.server 3000
```

Then visit [http://localhost:3000/index.html](http://localhost:3000/index.html).

---

## 🛠 Tech Stack

- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Tailwind CSS (CDN).
- **Icons & QR**: Lucide/SVG Icons, QRCode.js.
- **Backend / Real-Time**: Firebase Firestore SDK (CDN) + HTML5 BroadcastChannel API.
