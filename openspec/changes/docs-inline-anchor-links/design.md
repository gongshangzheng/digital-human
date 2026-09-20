# Design: docs-inline-anchor-links

## Context

- 标题 id 由 `MarkdownRenderer` 的 `heading_open` 规则生成：`slugify(标题文本)`
- `slugify`（`web/src/utils/markdown.js`）：转小写 → 空格变 `-` → 删掉非 `\w`、非 CJK、非 `-` 的字符（所以全角冒号、顿号、括号都被删掉）
- TOC 跳转走 `DocPage.scrollToHeading(slug)`：`document.getElementById(slug)` + `scrollIntoView({ behavior: 'smooth', block: 'start' })`
- 正文渲染走 `MarkdownRenderer`，其 `handleClick` 目前只处理 `/management/` 前缀

## Goals / Non-Goals

**Goals：** 正文里的 `[文字](#slug)` 能像 TOC 一样平滑跳到目标小节；不改 URL；不引入新依赖。
**Non-Goals：** 不做自定义锚点 id 语法（如 `{#custom}`）；不做跨文档锚点（`[[slug#sec]]`）；不改 slugify 规则（避免破坏 TOC 与已写链接）。

## Decisions

- **D1 前端接管 `#` 链接**：在 `handleClick` 里判断 `href.startsWith('#')` → `preventDefault()` → 用 `document.getElementById(decodeURIComponent(href.slice(1)))` 找目标 → `scrollIntoView` 平滑滚动。理由：与 TOC 行为一致、零新依赖、不改 URL。
- **D2 不改 slugify**：规则已经稳定且被 TOC 使用，改动会让已写链接与 TOC 同时失效。代价是标题里的标点会被吃掉——由此得到写作规范：**标题不用冒号**，锚点靠"括号内容也被删掉"的规则推算（例如 `### 漂移出在哪（模长还是方向）` → `#漂移出在哪模长还是方向`）。
- **D3 写作规范与代码同批落地**：skill 已补"同文档内引用用 heading 链接、不用书名号""标题不用冒号""slug 生成规则"三条；文档里已写入的 4 处引用作为验收样本。

## Risks / Trade-offs

- [目标 id 不存在时点了没反应] → 找不到元素时静默返回（与 TOC 现状一致）；写作侧靠规范避免拼错 slug
- [中文 slug 手写易错] → 规范里给出推导步骤；若后续发现易错，再考虑加 `{#custom}` 语法（另开 change）

## Migration Plan

1. 改 `MarkdownRenderer.handleClick`
2. 用《数字人身份》里已有的 4 个文内链接验收（点击是否平滑跳转、URL 是否不变、TOC 行为是否不变）
3. 回滚 = 去掉 `#` 分支

## Open Questions

（无）
