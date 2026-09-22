#!/usr/bin/env node
// 构建期把 management/docs/ 编译为前端可读的静态数据（web/public/docs-data.json）。
// 静态托管没有 FastAPI；生产文档页读取此快照，本地开发仍读取后端 API。
// 字段和排序复刻 server/routers/management.py，扫描跳过下划线前缀资产目录。

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { basename, dirname, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const WEB_DIR = resolve(__dirname, '..')
const REPO_ROOT = resolve(WEB_DIR, '..')
const DOCS_DIR = join(REPO_ROOT, 'management', 'docs')
const CONFIG_FILE = join(REPO_ROOT, 'server', 'config.py')
const OUT_FILE = join(WEB_DIR, 'public', 'docs-data.json')
const ASSETS_SRC = join(DOCS_DIR, '_assets')
const ASSETS_OUT = join(WEB_DIR, 'public', 'docs-assets')

function fail(message) {
  console.error(`[build-docs-data] ${message}`)
  process.exit(1)
}

/** 从 server/config.py 读取唯一的目录排序事实来源。 */
function readFolderOrder() {
  if (!existsSync(CONFIG_FILE)) fail(`找不到 ${relative(REPO_ROOT, CONFIG_FILE)}`)
  const source = readFileSync(CONFIG_FILE, 'utf8')
  const matched = source.match(/^\s*DOCS_FOLDER_ORDER\s*=\s*\[([^\]]*)\]/m)
  if (!matched) fail(`在 ${relative(REPO_ROOT, CONFIG_FILE)} 中找不到 DOCS_FOLDER_ORDER = [...]`)
  return matched[1]
    .split(',')
    .map((item) => item.trim().replace(/^['"]|['"]$/g, ''))
    .filter(Boolean)
}

function walkMarkdown(dir) {
  const found = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!entry.name.startsWith('_')) found.push(...walkMarkdown(join(dir, entry.name)))
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      found.push(join(dir, entry.name))
    }
  }
  return found
}

function countFiles(dir) {
  let count = 0
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) count += countFiles(join(dir, entry.name))
    else if (entry.isFile() && !entry.name.startsWith('.')) count += 1
  }
  return count
}

/** 每次先清空目标，确保已删除的源图不会残留在静态产物。 */
function syncAssets() {
  rmSync(ASSETS_OUT, { recursive: true, force: true })
  if (!existsSync(ASSETS_SRC)) return 0
  cpSync(ASSETS_SRC, ASSETS_OUT, {
    recursive: true,
    filter: (src) => !basename(src).startsWith('.'),
  })
  return countFiles(ASSETS_OUT)
}

function unquote(value) {
  const text = value.trim()
  if (text.length >= 2 && ((text[0] === '"' && text.at(-1) === '"') || (text[0] === "'" && text.at(-1) === "'"))) {
    return text.slice(1, -1)
  }
  return text
}

function parseScalar(raw) {
  const value = raw.trim()
  if (!value) return ''
  if (value.startsWith('[') && value.endsWith(']')) {
    const inner = value.slice(1, -1).trim()
    return inner ? inner.split(',').map((item) => unquote(item)) : []
  }
  if (/^-?\d+(\.\d+)?$/.test(value)) return Number(value)
  return unquote(value)
}

/** 只接受项目已规范化使用的单行标量和内联数组。 */
function parseFrontmatter(content, file) {
  if (!content.startsWith('---')) return [{}, content]
  const end = content.indexOf('---', 3)
  if (end < 0) fail(`${file}: frontmatter 起始 --- 之后没有结束 ---`)

  const meta = {}
  content.slice(3, end).split('\n').forEach((line, index) => {
    if (!line.trim() || /^\s*#/.test(line)) return
    if (/^\s/.test(line)) fail(`${file}:${index + 2} frontmatter 不支持缩进/多行：${line}`)
    const matched = line.match(/^([A-Za-z0-9_-]+):\s?(.*)$/)
    if (!matched) fail(`${file}:${index + 2} 无法解析的 frontmatter 行：${line}`)
    meta[matched[1]] = parseScalar(matched[2])
  })
  return [meta, content.slice(end + 3).trim()]
}

function docNumber(value) {
  if (value === null || value === undefined || value === '' || typeof value === 'boolean') return Infinity
  if (typeof value === 'number') return Number.isFinite(value) ? value : Infinity
  return /^-?\d+(\.\d+)?$/.test(String(value)) ? Number(value) : Infinity
}

function dateOrdinal(value) {
  if (!value) return 0
  const timestamp = Date.parse(String(value).slice(0, 10))
  return Number.isNaN(timestamp) ? 0 : timestamp
}

function cmp(a, b) {
  if (a === b) return 0
  return a < b ? -1 : 1
}

function main() {
  if (!existsSync(DOCS_DIR)) fail(`找不到文档目录：${DOCS_DIR}`)
  const files = walkMarkdown(DOCS_DIR)
  if (!files.length) fail(`文档目录中没有 .md 文件：${DOCS_DIR}`)

  const folderOrder = readFolderOrder()
  const docs = []
  const details = {}

  for (const file of files.sort()) {
    const [meta, content] = parseFrontmatter(readFileSync(file, 'utf8'), relative(REPO_ROOT, file))
    const slug = relative(DOCS_DIR, file).split(sep).join('/').replace(/\.md$/, '')
    const base = {
      slug,
      title: meta.title ?? slug,
      author: meta.author ?? '',
      date: meta.date === undefined || meta.date === null ? '' : String(meta.date),
      tags: Array.isArray(meta.tags) ? meta.tags : [],
      summary: meta.summary ?? '',
      id: meta.id ?? null,
      order: meta.order ?? null,
    }
    const sidecarFile = file.replace(/\.md$/, '.json')
    let sidecar = {}
    if (existsSync(sidecarFile)) {
      try {
        sidecar = JSON.parse(readFileSync(sidecarFile, 'utf8') || '{}')
      } catch (error) {
        fail(`${relative(REPO_ROOT, sidecarFile)} 不是合法 JSON：${error.message}`)
      }
    }
    docs.push(base)
    details[slug] = { ...base, content, sidecar }
  }

  const folderRank = (doc) => {
    const top = doc.slug.includes('/') ? doc.slug.split('/')[0] : ''
    const index = folderOrder.indexOf(top)
    return index === -1 ? folderOrder.length : index
  }
  docs.sort((a, b) =>
    cmp(folderRank(a), folderRank(b)) ||
    cmp(docNumber(a.order), docNumber(b.order)) ||
    cmp(docNumber(a.id), docNumber(b.id)) ||
    cmp(dateOrdinal(b.date), dateOrdinal(a.date)) ||
    cmp(a.slug, b.slug),
  )

  const orderedDetails = {}
  for (const doc of docs) orderedDetails[doc.slug] = details[doc.slug]

  const assetCount = syncAssets()
  mkdirSync(dirname(OUT_FILE), { recursive: true })
  writeFileSync(
    OUT_FILE,
    `${JSON.stringify({ generatedAt: new Date().toISOString(), folderOrder, assetCount, docs, details: orderedDetails }, null, 2)}\n`,
    'utf8',
  )
  console.log(`[build-docs-data] ${docs.length} 篇文档、${assetCount} 个图像资产 → ${relative(REPO_ROOT, OUT_FILE)}`)
}

main()
