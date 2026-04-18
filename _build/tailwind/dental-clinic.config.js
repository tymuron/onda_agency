/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/dental-clinic.html'],
  theme: {
    extend: {
      colors: {
        frost: '#F8FAFB',
        surface: '#FFFFFF',
        slate: { deep: '#1E293B' },
        cool: { gray: '#64748B' },
        sage: '#059669',
        'sage-dark': '#047857',
        mint: { wash: '#ECFDF5' },
      },
      fontFamily: {
        satoshi: ['Satoshi', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'monospace'],
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': 'calc(2rem - 0.375rem)',
      },
    },
  },
};
