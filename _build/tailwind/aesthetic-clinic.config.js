/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/aesthetic-clinic.html'],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'serif'],
        sans: ['"DM Sans"', 'sans-serif'],
        mono: ['"Geist Mono"', 'monospace'],
      },
      colors: {
        bg: '#0A0A0A',
        surface: '#161616',
        ivory: '#F5F0EB',
        silver: '#A39E99',
        rose: '#C4956A',
        deep: '#070707',
      },
    },
  },
};
