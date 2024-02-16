module.exports = {
    content: [
      "../**/templates/**/**/*.html",
      "../**/templates/**/*.html",
      "../**/templates/*.html",
      "../**/**/**/*.js"
    ],
    theme: {
      extend: {},
    },  
    plugins: [
      require('@tailwindcss/forms'),
    ],
  }