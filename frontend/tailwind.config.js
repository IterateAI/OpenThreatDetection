/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    colors: {
      'red': '#E30000',
      'black': '#242B33',
      'black-600': '#6B727B',
      'black-300': '#D3D3D3',
      'black-100': '#F3F6F9',
      'white': '#FFFFFF',
      'gray-dark': '#273444',
      'gray': '#8492a6',
      'gray-light': '#d3dce6',
    },
    extend: {
      backgroundImage: {
        
      },
    },
  },
  plugins: [],
}
