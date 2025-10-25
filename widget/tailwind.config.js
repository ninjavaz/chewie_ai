/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      spacing: {
        '15': '3.75rem', // 60px for toggle button
      },
      colors: {
        chewie: {
          primary: '#3b82f6',
          'primary-hover': '#2563eb',
          background: '#ffffff',
          surface: '#f8fafc',
          border: '#e2e8f0',
          text: '#1e293b',
          'text-muted': '#64748b',
        },
        'chewie-dark': {
          primary: '#60a5fa',
          'primary-hover': '#3b82f6',
          background: '#0f172a',
          surface: '#1e293b',
          border: '#334155',
          text: '#f1f5f9',
          'text-muted': '#94a3b8',
        }
      },
      fontFamily: {
        'chewie': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'chewie': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'chewie-lg': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'chewie-dark': '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2)',
        'chewie-dark-lg': '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      },
      borderRadius: {
        'chewie': '12px',
        'chewie-sm': '8px',
      },
      animation: {
        'chewie-slide-up': 'chewie-slide-up 0.3s ease-out',
        'chewie-loading-bounce': 'chewie-loading-bounce 1.4s ease-in-out infinite both',
      },
      keyframes: {
        'chewie-slide-up': {
          from: {
            opacity: '0',
            transform: 'translateY(20px)',
          },
          to: {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        'chewie-loading-bounce': {
          '0%, 80%, 100%': {
            transform: 'scale(0)',
          },
          '40%': {
            transform: 'scale(1)',
          },
        },
      },
    },
  },
  plugins: [],
  darkMode: ['class', '[data-chewie-theme="dark"]'],
}
