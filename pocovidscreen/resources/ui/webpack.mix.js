let mix = require('laravel-mix');

require('laravel-mix-purgecss');
/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

const output_dir = '../../web_root/'

mix.setPublicPath(output_dir)

mix.react('src/app.js', output_dir + 'js')
  .version()
  .sass('assets/sass/app.scss', output_dir + 'css')
  .purgeCss()
  .webpackConfig({
    externals: [
      'child_process'
    ],
    node: {
      fs: 'empty'
    }
  })
  .sourceMaps();
