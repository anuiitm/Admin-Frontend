/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./index.html',
		'./src/**/*.{vue,js,ts,jsx,tsx}',
	],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				primary: {
					50: '#eef8ff',
					100: '#d8eeff',
					200: '#b8e1ff',
					300: '#86ceff',
					400: '#4bb2ff',
					500: '#1d94ff',
					600: '#0a76ea',
					700: '#075ec1',
					800: '#0a4f9c',
					900: '#0d427f',
				},
			},
			boxShadow: {
				soft: '0 10px 30px -10px rgba(0,0,0,0.2)'
			}
		}
	},
	plugins: [
		require('@tailwindcss/forms')({ strategy: 'class' })
	]
}

