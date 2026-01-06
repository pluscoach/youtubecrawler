/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f0f0f',
        card: '#1a1a1a',
        accent: '#ff0050',
        'text-primary': '#ffffff',
        'text-secondary': '#a0a0a0',
        border: '#333333',
      },
    },
  },
  plugins: [],
}
