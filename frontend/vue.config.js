const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
      ? '/OmniTrack/'
      : '/',
  devServer: {
    host: '0.0.0.0',
    port: 8081
  }
})
