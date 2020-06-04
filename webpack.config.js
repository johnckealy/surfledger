const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


module.exports = {
  context: __dirname,
  entry: {
     main: ['@babel/polyfill', './ledger/static/ledger/js/index.js']
  },

  output: {
    path: path.resolve('./ledger/static/ledger/compiled_assets/'),
    filename: "[name]-[hash].js"
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader", "postcss-loader"]
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/,
        use: [
               {
                 loader: "file-loader",
                 options: {
                   outputPath: 'images'
                 }
               }
             ]
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          // {
          //   loader: 'style-loader', // inject CSS to page
          // },
          {
            loader: "css-loader",
          },
          {
            loader: 'postcss-loader',
            options: {
              ident: 'postcss',
              plugins: [
                require('autoprefixer')({}),
                require('cssnano')({ preset: 'default' })
              ],
              minimize: true
            }
          },
          {
            loader: "sass-loader",
            options: {
              implementation: require("sass")
              }
          }
        ]
      }
    ]
  },

  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          output: {
            comments: false,
          },
        },
        parallel: true,
        extractComments: false,
        cache: true,
        sourceMap: true,
      }),
    ],
  },

  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
    new MiniCssExtractPlugin({
        filename: "application-[hash].css"
    })
  ],
  mode: 'development'
}