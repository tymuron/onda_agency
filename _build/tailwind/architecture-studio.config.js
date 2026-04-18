/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/architecture-studio.html'],
  theme: {
    extend: {
      colors: {
        bg: '#F5F3EF',
        surface: '#FFFFFF',
        graphite: '#1A1A1A',
        concrete: '#737373',
        terracotta: '#B85C38',
      },
      fontFamily: {
        display: ['"Cabinet Grotesk"', 'sans-serif'],
        body: ['"Outfit"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
};
