import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command, isPreview }) => ({
  // GitHub Pages 部署在仓库子路径；开发仍从根路径访问。
  base: command === 'build' || isPreview ? '/digital-human/' : '/',
  plugins: [vue()],
  optimizeDeps: {
    // 预打包器会把 katex 的字符串拼接常量折叠掉、破坏控制字正则
    // （\begin → \b），导致 \begin{cases}、\qquad 等命令在 dev 下渲染失败。
    // 让 katex 独立成 chunk、不被内联进插件包即可规避。
    include: ['katex'],
  },
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
