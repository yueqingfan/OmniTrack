const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
      ? '/OmniTrack/frontend/'  // 仓库名为 OmniTrack
      : '/',
  devServer: {
    host: '0.0.0.0',
    port: 8081
  }
})
