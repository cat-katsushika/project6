/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./django/templates/**/*.{html,js}",
    'node_modules/preline/dist/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('preline/plugin'),
  ],
}

