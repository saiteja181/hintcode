/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './popup/**/*.{html,js}',
    './sidepanel/**/*.{html,js}',
    './options/**/*.{html,js}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#7C3AED',
        'primary-light': '#8B5CF6',
        'primary-dark': '#6D28D9',
        dark: {
          bg: '#1a1a2e',
          card: '#16213e',
          surface: '#0f3460',
          border: '#2a2a4a',
        },
      },
    },
  },
  plugins: [],
};
