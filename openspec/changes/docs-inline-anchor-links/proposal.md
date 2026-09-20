# Proposal: docs-inline-anchor-links（文档内小节跳转可用）

## Why

文档正文里引用**同一篇文档内的其他小节**时，目前只能写成《小节标题》文字，读者点不过去。而渲染器已经给每个标题生成了 `id`（`slugify(标题)`），右侧 TOC 也早就能用 `scrollToHeading()` 平滑跳到目标——只有正文里的 `#锚点` 链接没人管：

- `MarkdownRenderer.handleClick` 只拦截 `/management/` 前缀的链接
- `[文字](#slug)` 会走浏览器默认行为：改 URL hash + 跳转，既没有平滑滚动，也会在地址栏留下 hash（与站内路由混在一起）

结果就是"能写锚点但体验不一致"。写作侧需要一条明确规范：**文内引用小节用 heading 链接，不用书名号**。

## What Changes

- `MarkdownRenderer` 拦截 `href` 以 `#` 开头的链接：`preventDefault()` 后按 `id` 取元素并 `scrollIntoView({ behavior: 'smooth', block: 'start' })`，与 TOC 的跳转行为完全一致，**不改 URL**
- 文档写作规范同步：同文档内引用小节用 `[标题](#slug)`；标题不使用冒号（改用括号）；`#slug` 的生成规则写进 skill
- 现有文档里已经写成 heading 链接的引用（《数字人身份》里 4 处）由此获得一致的跳转体验

## Capabilities

### Modified Capabilities
- `docs-page-content`：新增「文内小节锚点跳转」要求（`#` 链接由前端接管，与 TOC 行为一致、不改 URL）

## Impact

- 代码：`web/src/components/common/MarkdownRenderer.vue`（`handleClick` 增加 `#` 分支，约 5 行）
- 文档：skill 的《文档内链接》已补规则；《数字人身份》的 4 处文内引用已改成 heading 链接
- 不影响：跨文档链接（`[[slug|名]]`）、外链、TOC、sidecar 渲染
