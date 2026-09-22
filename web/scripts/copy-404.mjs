#!/usr/bin/env node
// 静态托管直接访问 history 路由会命中平台 404；用入口 HTML 作为回退页后由 Vue Router 接管。

import { copyFileSync, existsSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const webDir = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const indexFile = join(webDir, 'dist', 'index.html')
const fallbackFile = join(webDir, 'dist', '404.html')

if (!existsSync(indexFile)) {
  console.error(`[copy-404] 未找到 ${indexFile}，请先执行 vite build（npm run build 会自动串联）`)
  process.exit(1)
}

copyFileSync(indexFile, fallbackFile)
console.log('[copy-404] dist/index.html → dist/404.html')
