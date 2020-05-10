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

const public_root ='public/'
const output_dir = '../../web_root/'
const htaccess_file = '.htaccess'

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
  .copy(public_root + '*.*', output_dir)
  .copy(public_root + htaccess_file, output_dir + htaccess_file)
  .sourceMaps();
