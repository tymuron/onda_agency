/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/real-estate.html'],
  theme: {
    extend: {
      colors: {
        vanta: '#050505',
        surface: 'rgba(255,255,255,0.03)',
        champagne: '#C9A84C',
        silver: '#94A3B8',
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', 'serif'],
        body: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
};
