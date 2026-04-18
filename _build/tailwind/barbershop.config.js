/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/examples/barbershop.html'],
  theme: {
    extend: {
      colors: {
        espresso: '#0C0A09',
        surface: '#1C1917',
        cream: '#FAFAF9',
        stone: '#A8A29E',
        copper: '#B87333',
        'copper-dark': '#9A5F2A',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"Space Grotesk"', 'sans-serif'],
      },
    },
  },
};
