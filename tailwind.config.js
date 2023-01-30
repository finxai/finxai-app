/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./resources/**/*.blade.php",
        "./resources/**/*.js",
        "./resources/**/*.vue",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#0BBDC8",
                dark: "#0A0A0A",
                silver: "#EAEAEA",
                light: "#F5F5F5",
            },
        },
    },
    plugins: [],
}
