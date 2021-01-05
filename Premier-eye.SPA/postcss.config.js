const autoprefixer = require('autoprefixer');
const vars = require('postcss-simple-vars');

module.exports = {
    plugins: [autoprefixer, vars],
};