/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/solo-entrepreneur.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Outfit', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'monospace'],
      },
      colors: {
        surface: '#FFFFFF',
        canvas: '#FAFAFA',
        ink: '#0F172A',
        steel: '#64748B',
        indigo: {
          DEFAULT: '#4F46E5',
          dark: '#4338CA',
          light: '#E0E7FF',
        },
      },
    },
  },
};
