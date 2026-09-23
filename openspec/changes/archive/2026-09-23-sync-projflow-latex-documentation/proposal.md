## Why

ProjFlow 已在最近一次文档静态发布同步后完善了共享文档基础设施：Markdown 正文可渲染 LaTeX、Mermaid 图内公式有正确样式，并把文档写作门禁与内容规范收敛为单一 project-scoped skill。本仓库当前正文将公式作为普通文本，且仍保留与上游已合并设计不同的 `doc-writing` skill，需要选择性同步已提交的上游能力以避免共享契约继续分叉。

## What Changes

- 同步 ProjFlow 已提交的 `[shared]` 更新 `4b7694b → d68b86b → bacb3e6 → 073a94b`，逐文件适配 Digital Human，不携带上游 OpenSpec change 历史、身份文案或无关业务内容。
- 在 Markdown 文档正文中支持 `$...$` 行内公式与 `$$...$$` 块级公式；公式无法解析时保留可见原文，金额等普通美元符号不应被误识别为公式。
- 载入 KaTeX 样式，使 Mermaid 图内已经生成的 KaTeX 标记正确显示。
- 新建 `docs-math` 主规格，并从 `docs-page-content` 移出数学渲染契约，保持行为不变但使其可独立发现。
- **BREAKING（Agent workflow）**：引入项目级 `.agents/skills/documentation/`，将 OpenSpec 门禁、文档登记、内容格式、图片、Mermaid 与 LaTeX 约定集中在该 skill；移除项目级 `.agents/skills/doc-writing/`。后续文档任务应使用 `documentation` 作为唯一入口。
- 同步文章笔记 skill 的公式书写与校验规则，使其与渲染能力保持一致。

## Capabilities

### New Capabilities
- `docs-math`: 文档正文与 Mermaid 图中 LaTeX 数学表达式的渲染、失败降级和美元符号边界契约。

### Modified Capabilities
- `docs-page-content`: 从该综合文档能力中移除并迁移数学渲染要求至独立的 `docs-math` capability，不改变其他正文内容行为。
- `repository-agent-skills`: 将文档写作流程与内容规范收敛为唯一的 project-scoped `documentation` skill，并规定不再保留重叠的 `doc-writing` skill。

## Impact

- 前端：`web/package.json`、锁文件和 `web/src/components/common/MarkdownRenderer.vue`，新增直接 KaTeX/markdown-it 插件依赖与样式。
- 规范：新增 `openspec/specs/docs-math/spec.md`，更新 `docs-page-content` 与 `repository-agent-skills`。
- 项目 skill：更新 `.agents/skills/article-note/` 的公式约定与校验，新增 `.agents/skills/documentation/`，删除未跟踪的 `.agents/skills/doc-writing/`。
- 文档正文中的现有代码块、wiki 链接、图题与 Mermaid 渲染须保持兼容；后端 API、端口、GitHub Pages base 和菜单策略不变。
