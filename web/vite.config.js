import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command, isPreview }) => ({
  // GitHub Pages 部署在仓库子路径；开发仍从根路径访问。
  base: command === 'build' || isPreview ? '/digital-human/' : '/',
  plugins: [vue()],
  server: {
    port: 3212,
    proxy: {
      '/api': {
        target: 'http://localhost:8812',
        changeOrigin: true,
      },
    },
  },
}))
