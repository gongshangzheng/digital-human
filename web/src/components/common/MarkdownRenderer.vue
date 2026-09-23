<template>
  <div class="markdown-body" ref="containerRef" v-html="rendered" @click="handleClick"></div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownIt from 'markdown-it'
import checkbox from 'markdown-it-task-checkbox'
import { slugify } from '../../utils/markdown'
import mermaid from 'mermaid'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import { useThemeStore } from '../../stores/theme'

const props = defineProps({
  content: { type: String, default: '' },
})

const containerRef = ref(null)
const themeStore = useThemeStore()
const router = useRouter()

function handleClick(e) {
  const anchor = e.target.closest('a')
  if (!anchor) return
  const href = anchor.getAttribute('href')
  if (!href) return
  // 文内锚点：按 id 找到标题并平滑滚动，与右侧 TOC 行为一致（不改 URL）
  if (href.startsWith('#')) {
    e.preventDefault()
    const el = document.getElementById(decodeURIComponent(href.slice(1)))
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }
  if (href.startsWith('/management/')) {
    e.preventDefault()
    router.push(href)
  }
}

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true,
})
  .use(checkbox, {
    disabled: true,
    divWrap: false,
    liClass: 'task-list-item',
  })

// 公式直接用 katex 渲染，不经第三方 markdown-it 插件：
// Vite dev 依赖预打包会把插件内联的 katex 常量折叠出错，破坏内部控制字正则
// （`\\begin` → `\b`），使 `\begin{cases}`、`\qquad` 等命令渲染错乱；
// katex 作为直接依赖会单独成 chunk，dev 与 build 行为一致。
function renderMath(tex, displayMode) {
  try {
    return katex.renderToString(tex, { displayMode, throwOnError: false })
  } catch (error) {
    return `<span class="katex-error">${md.utils.escapeHtml(tex)}</span>`
  }
}

// 从 `from` 起找未被反斜杠转义的定界符；找不到返回 -1。
function findMathEnd(src, from, delim) {
  let index = src.indexOf(delim, from)
  while (index !== -1) {
    let escapes = 0
    for (let pos = index - 1; pos >= 0 && src[pos] === '\\'; pos -= 1) escapes += 1
    if (escapes % 2 === 0) return index
    index = src.indexOf(delim, index + delim.length)
  }
  return -1
}

// 行内 `$...$` 与段内 `$$...$$`。单 `$` 内容首尾带空白时判为普通文本
// （如 "$5 到 $10 不等"），保持字面量而非公式。
md.inline.ruler.before('escape', 'math_inline', (state, silent) => {
  const start = state.pos
  const src = state.src
  if (src[start] !== '$') return false
  const isDisplay = src.startsWith('$$', start)
  const delim = isDisplay ? '$$' : '$'
  const contentStart = start + delim.length
  const end = findMathEnd(src, contentStart, delim)
  if (end === -1) return false
  const content = src.slice(contentStart, end)
  if (!content.trim()) return false
  if (!isDisplay && /^\s|\s$/.test(content)) return false
  if (!silent) {
    const token = state.push(isDisplay ? 'math_display' : 'math_inline', 'math', 0)
    token.markup = delim
    token.content = content
  }
  state.pos = end + delim.length
  return true
})

// 块级公式：整行以 `$$` 开头，闭合定界符可在同行或后续行。
md.block.ruler.before('fence', 'math_block', (state, startLine, endLine, silent) => {
  const begin = state.bMarks[startLine] + state.tShift[startLine]
  const lineEnd = state.eMarks[startLine]
  if (state.src.slice(begin, begin + 2) !== '$$') return false
  const rest = state.src.slice(begin + 2, lineEnd)
  const sameLineEnd = rest.indexOf('$$')
  let content
  let nextLine
  if (sameLineEnd !== -1) {
    // 同行闭合且后面还有内容时，交回段落由行内规则处理
    if (rest.slice(sameLineEnd + 2).trim()) return false
    content = rest.slice(0, sameLineEnd)
    nextLine = startLine + 1
  } else {
    const end = findMathEnd(state.src, begin + 2, '$$')
    if (end === -1) return false
    content = state.src.slice(begin + 2, end)
    nextLine = startLine + content.split('\n').length
  }
  if (silent) return true
  const token = state.push('math_block', 'math', 0)
  token.block = true
  token.content = content
  token.map = [startLine, nextLine]
  state.line = nextLine
  return true
}, { alt: ['paragraph', 'reference', 'blockquote', 'list'] })

md.renderer.rules.math_block = (tokens, idx) =>
  `<p class="katex-block">${renderMath(tokens[idx].content, true)}</p>\n`
md.renderer.rules.math_inline = (tokens, idx) => renderMath(tokens[idx].content, false)
md.renderer.rules.math_display = (tokens, idx) => renderMath(tokens[idx].content, true)

// Heading auto-ID
const defaultHeadingRender = md.renderer.rules.heading_open ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const nextToken = tokens[idx + 1]
  if (nextToken && nextToken.children) {
    const text = nextToken.children
      .filter(t => t.type === 'text' || t.type === 'code_inline')
      .map(t => t.content)
      .join('')
    if (text) {
      token.attrSet('id', slugify(text))
    }
  }
  return defaultHeadingRender(tokens, idx, options, env, self)
}

// Mermaid code block: render as <pre class="mermaid"> instead of <pre><code>
const defaultFence = md.renderer.rules.fence ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

md.renderer.rules.fence = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const info = token.info ? token.info.trim() : ''
  if (info === 'mermaid') {
    const escaped = md.utils.escapeHtml(token.content)
    return `<pre class="mermaid">${escaped}</pre>\n`
  }
  return defaultFence(tokens, idx, options, env, self)
}

// Image: 统一输出 <img loading="lazy">；图题由所在段落的 figure 包装负责（见下）
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const src = md.utils.escapeHtml(token.attrGet('src') || '')
  const alt = md.utils.escapeHtml(token.content || '')
  const title = token.attrGet('title')
  const titleAttr = title ? ` title="${md.utils.escapeHtml(title)}"` : ''
  return `<img src="${src}" alt="${alt}" loading="lazy"${titleAttr}>`
}

// 整段只有一张带 alt 的图 → 包装为语义化 figure，alt 兼作图题
const defaultParagraphOpen = md.renderer.rules.paragraph_open ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }
const defaultParagraphClose = md.renderer.rules.paragraph_close ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

function loneFigureImage(tokens, idx) {
  const inline = tokens[idx + 1]
  if (!inline || inline.type !== 'inline' || !Array.isArray(inline.children)) return null
  // 忽略纯空白文本节点（breaks:true 下可能残留）
  const kids = inline.children.filter(t => !(t.type === 'text' && !t.content.trim()))
  if (kids.length !== 1) return null
  const only = kids[0]
  if (only.type !== 'image' || !only.content) return null
  return only
}

md.renderer.rules.paragraph_open = function (tokens, idx, options, env, self) {
  const img = loneFigureImage(tokens, idx)
  if (img) {
    env.__figureAlt = img.content
    return '<figure>'
  }
  return defaultParagraphOpen(tokens, idx, options, env, self)
}

md.renderer.rules.paragraph_close = function (tokens, idx, options, env, self) {
  if (env && env.__figureAlt) {
    const alt = md.utils.escapeHtml(env.__figureAlt)
    delete env.__figureAlt
    return `<figcaption>${alt}</figcaption></figure>`
  }
  return defaultParagraphClose(tokens, idx, options, env, self)
}

const rendered = computed(() => {
  if (!props.content) return '<p class="text-light">暂无内容</p>'
  let src = props.content
  // Slugs may contain spaces (Chinese/English file names). CommonMark forbids
  // spaces in bare link destinations, so each path/query segment is
  // percent-encoded; vue-router decodes the param back to the raw slug.
  const encodeSlugPath = (slug) => slug.trim().split('/').map(encodeURIComponent).join('/')
  // Task links: [[proj#t2-3]] or [[proj#t2-3|display]] → project tree with task selected
  src = src.replace(/\[\[([^#|\]]+)#([^|\]]+)\|([^\]]+)\]\]/g, (_, proj, task, text) =>
    `[${text.trim()}](/management/projects?slug=${encodeURIComponent(proj.trim())}&task=${encodeURIComponent(task.trim())})`)
  src = src.replace(/\[\[([^#|\]]+)#([^|\]]+)\]\]/g, (_, proj, task) =>
    `[${proj.trim()}/${task.trim()}](/management/projects?slug=${encodeURIComponent(proj.trim())}&task=${encodeURIComponent(task.trim())})`)
  // Doc links: [[slug]] or [[slug|display]] → doc detail page
  src = src.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, slug, text) => `[${text.trim()}](/management/docs/${encodeSlugPath(slug)})`)
  src = src.replace(/\[\[([^\]]+)\]\]/g, (_, slug) => `[${slug.trim()}](/management/docs/${encodeSlugPath(slug)})`)
  return md.render(src)
})

async function renderMermaid() {
  if (!containerRef.value) return
  const nodes = containerRef.value.querySelectorAll('pre.mermaid')
  if (!nodes.length) return

  for (const node of nodes) {
    if (!node.dataset.source) {
      node.dataset.source = node.textContent
    } else {
      node.textContent = node.dataset.source
      node.removeAttribute('data-processed')
    }
    const svgEl = node.querySelector('svg')
    if (svgEl) svgEl.remove()
  }

  try {
    mermaid.initialize({
      startOnLoad: false,
      theme: themeStore.isDark ? 'dark' : 'default',
      securityLevel: 'loose',
      fontFamily: 'system-ui, sans-serif',
    })
    await mermaid.run({ nodes: Array.from(nodes) })
  } catch (e) {
    console.warn('Mermaid render error:', e)
  }
}

watch(
  [rendered, () => themeStore.isDark],
  async () => {
    await nextTick()
    await renderMermaid()
  },
  { immediate: true }
)
</script>

<style scoped lang="scss">
.markdown-body {
  :deep(h1),
  :deep(h2),
  :deep(h3),
  :deep(h4) {
    scroll-margin-top: 4rem;
  }

  :deep(.task-list-item) {
    list-style: none;
    margin-left: -20px;
  }
  :deep(.task-list-item input[type='checkbox']) {
    margin-right: 8px;
    transform: translateY(1px);
    accent-color: var(--color-primary);
    width: 14px;
    height: 14px;
    cursor: default;
  }

  :deep(pre.mermaid) {
    background: transparent;
    padding: 16px;
    margin: 16px 0;
    text-align: center;
    overflow-x: auto;

    svg {
      max-width: 100%;
      height: auto;
    }
  }

  :deep(.d-error) {
    display: none;
  }

  :deep(a) {
    color: var(--color-primary);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
