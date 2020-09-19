const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const path = require('path');
const {CheckerPlugin} = require('awesome-typescript-loader')
const fs = require('fs')
const dotenv = require('dotenv')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const root = path.resolve(".")


module.exports = (env) => {
    console.log(env)

    const currentEnivronment = env.NODE_ENV || env.nodeEnv // почему-то devServer и обычная сборка по-разному прокидывают аргументы
    console.log(currentEnivronment)
    const isProduction = currentEnivronment === "prod"

    const basePath = root + '/.env';

    const envPath = basePath + '.' + currentEnivronment;

    const finalPath = fs.existsSync(envPath) ? envPath : basePath;
    const fileEnv = dotenv.config({path: finalPath}).parsed;

    const envKeys = Object.keys(fileEnv).reduce((prev, next) => {
        prev[`process.env.${next}`] = JSON.stringify(fileEnv[next]);
        return prev;
    }, {});
    const devtool = isProduction ? '' : 'eval-cheap-module-source-map'
    console.log(isProduction)
    console.log(envKeys)

    return {
        entry: "./src/index.tsx",
        output: {
            path: path.resolve(__dirname, 'dist'),
            publicPath: '/', // этот путь будет добавляться в пути до каждого бандла внутри хтмл и других бандлов
            filename: "js/[name].[hash].bundle.js",
            chunkFilename: 'js/[name].[hash].bundle.js',
        },
        devtool,
        resolve: {
            extensions: ['.tsx', '.ts', ".js"]
        },
        optimization: {
            runtimeChunk: 'single',
            splitChunks: {
                chunks: 'all',
                maxInitialRequests: Infinity,
                minSize: 0,
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name(module) {
                            // получает имя, то есть node_modules/packageName/not/this/part.js
                            // или node_modules/packageName
                            const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];

                            // имена npm-пакетов можно, не опасаясь проблем, использовать
                            // в URL, но некоторые серверы не любят символы наподобие @
                            return `npm.${packageName.replace('@', '')}`;
                        },
                    },
                },
            },
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /(node_modules)/,
                    loader: 'awesome-typescript-loader',
                    options: {
                        compilerOptions: {
                            "sourceMap": !isProduction,
                        }
                    }
                },
                {
                    test: /\.css$/,
                    use: [
                        "style-loader",
                        {
                            loader: "css-loader",
                            options: {
                                modules: false,
                            }
                        }
                    ]
                },
                {
                    test: /\.(scss|module.(scss))$/,
                    exclude: /\.$/,
                    loader: [
                        !isProduction ? 'style-loader' : MiniCssExtractPlugin.loader,
                        'css-loader',
                        {
                            loader: 'sass-loader',
                            options: {
                                sourceMap: !isProduction
                            }
                        }
                    ]
                },
                {
                    test: /\.(pcss)$/,
                    exclude: /node_modules/,
                    loader: [
                         'style-loader',
                        'css-loader',
                        {
                            loader: 'postcss-loader',
                            options: {
                                sourceMap: !isProduction,
                            }
                        }
                    ]
                },
                {
                    test: /\.(jpg|jpeg|gif|png|svg)$/,
                    loader: ['file-loader?context=src/images&name=images/[path][name].[ext]'],
                },
                {
                    test: /\.(woff|woff2|eot|ttf)$/,
                    loader: 'file-loader?name=fonts/[name].[hash].[ext]',
                }
            ]
        },
        devServer: {
            contentBase: path.join(__dirname, 'public'),
            port: 3000,
            watchContentBase: true,
            progress: true,
            compress: true,
            hot: true,
            historyApiFallback: true
        },
        plugins: [
            new webpack.ProgressPlugin(),
            new CleanWebpackPlugin(),
            new webpack.DefinePlugin(envKeys),
            new CopyPlugin({
                patterns: [
                    {from: 'public', to: '.'},
                ],
            }),
            new HtmlWebpackPlugin({template: './public/index.html'}),
            new CheckerPlugin()
        ]
    }
}
