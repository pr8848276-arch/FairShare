# Head, CSS, and CDNs
HEAD_HTML = r"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>FairShare — Smart Shared Expense Splitter, OCR & UPI Settlement</title>

  <!-- Google Fonts: Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              300: '#a5b4fc',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
            }
          }
        }
      }
    }
  </script>

  <!-- Firebase Compat SDKs (via CDN) -->
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>

  <!-- QR Code Generator CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

  <!-- Chart.js for Visual Analytics CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Tesseract.js for AI Client-side OCR Scanner CDN -->
  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>

  <style>
    /* Custom scrollbars */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.04);
    }
    .dark ::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.04);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(99, 102, 241, 0.25);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(99, 102, 241, 0.45);
    }
    @keyframes pulse-subtle {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.65; transform: scale(1.08); }
    }
    .pulse-subtle {
      animation: pulse-subtle 2.5s ease-in-out infinite;
    }
    @keyframes scan-laser {
      0% { top: 0%; opacity: 0.8; }
      50% { top: 95%; opacity: 1; }
      100% { top: 0%; opacity: 0.8; }
    }
    .scan-laser-line {
      animation: scan-laser 2s ease-in-out infinite;
    }
    /* Safe touch highlight */
    * {
      -webkit-tap-highlight-color: transparent;
    }
    .tab-active {
      border-color: #6366f1;
      color: #4f46e5;
      font-weight: 700;
    }
    .dark .tab-active {
      border-color: #818cf8;
      color: #a5b4fc;
    }
  </style>
</head>
"""
