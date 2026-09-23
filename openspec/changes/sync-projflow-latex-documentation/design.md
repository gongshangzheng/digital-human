## Context

本仓库的 `MarkdownRenderer.vue` 使用 markdown-it 并保持 `html: false`，已自定义任务清单、标题锚点、Mermaid、图片与 wiki 链接。当前没有 KaTeX 插件或样式，公式仅按普通文本输出。项目还保留一个未跟踪的 `.agents/skills/doc-writing/`，而上游共享工作流已将其门禁和内容规范收敛到 `documentation`。

本次只选择性适配 ProjFlow 已批准的共享提交 `4b7694b → d68b86b → bacb3e6 → 073a94b`。Digital Human 的静态文档构建、资产前缀、路由、端口和领域目录均不属于同步对象。

## Goals / Non-Goals

**Goals:**

- 让 Markdown 正文支持安全的 KaTeX 行内与块级公式，并为 Mermaid 的 KaTeX 输出载入样式。
- 让金额等普通美元文本保持字面显示，公式错误不破坏整个页面。
- 把数学行为拆分为独立的 `docs-math` capability，并将写作工作流收敛到一个 project-scoped `documentation` skill。
- 让 `article-note` 的写作与校验规则和渲染能力一致。

**Non-Goals:**

- 不修改后端 API、端口、页面路由、静态构建、文档资产机制或业务文档正文。
- 不迁入上游 OpenSpec archives、身份文案、登记表制度或不属于本项目的 management skill 约定。
- 不兼容保留 `doc-writing`：用户已批准将其移除的 breaking agent-workflow 变更。
- 不编辑由 `docs-order-tooling` 同步维护的主 `docs-page-content` spec；本 change 只写 delta，主 spec 的最终迁移由该 change 闭环后整合。

## Decisions

### 使用 markdown-it KaTeX 插件和显式 KaTeX 样式

直接依赖 `@vscode/markdown-it-katex` 与 `katex`，通过现有 MarkdownIt 实例注册插件并引入 `katex.min.css`。这保留 `html: false` 和现有 renderer rules；同时 Mermaid 已有的 KaTeX 标记可使用同一份样式。

插件以 CJS 默认导出发布，但 Vite dev 预打包与 production build 的模块形状不同。因此在注册前归一化 `default` / `default.default`，加载异常时不阻断正文渲染。选择该插件而不是手工 regex 置换，以保持公式 token、代码围栏和表格解析由 markdown-it 管理。

### 对行内美元定界符添加补充守卫

插件未拒绝首尾为空白的公式内容，可能把金额句中 `$10 不等，还有 $` 的片段误判为公式。包装插件注册的 `math_inline` rule：若生成的数学 token 内容首尾为空白，则恢复 token 和解析位置，交回普通文本规则。该守卫补足金额/普通美元边界，不改块级公式或代码围栏处理。

### 将数学契约单独建模，并延后主 spec 合并

本 change 的 `docs-math` delta 持有全部公式行为。`docs-page-content` delta 仅记录职责迁移，避免复制数学细节。由于活跃的 `docs-order-tooling` 正在维护同一主 spec，本次不直接编辑主 `openspec/specs/docs-page-content/spec.md`；其归档后的父级整合将把此 delta 的职责说明与现有 order 契约一起同步。

### 采用上游 documentation 作为内容基线，并按本仓库裁剪

新增 `.agents/skills/documentation/` 和 Mermaid 速查，保留 OpenSpec 门禁与内容格式规则，但替换为本仓库实际的 `management/docs/`、sidecar、排序、资产和 namespace 约定；不携带上游不存在于本仓库的 registry 或 management CRUD 假设。随后删除未跟踪的 `.agents/skills/doc-writing/`，避免两个冲突入口。

## Risks / Trade-offs

- [插件模块互操作性差异] → 归一化 CJS 默认导出，并通过 production build 验证。
- [数学语法覆盖范围有限] → 明确仅支持 `$...$` 和 `$$...$$`；非法公式由 `throwOnError: false` 降级，其他 TeX 定界符由 skill 和校验提示。
- [普通美元符号误判] → 通过 inline rule 的内容空白守卫验证金额示例；仍以 markdown-it 插件的 token 化规则为边界。
- [主 spec 同时被其他 change 修改] → 不触碰其主 spec，仅保留本 change delta 并报告后续同步需求。

## Migration Plan

1. 安装直接依赖并在现有 renderer 中注册 KaTeX 与美元守卫。
2. 运行构建和可执行的 renderer/Markdown token 检查，确认公式、金额、代码围栏和错误公式表现。
3. 新增 `documentation` skill，更新 article-note 的公式规则和校验提示，删除 `doc-writing`。
4. 严格验证本 OpenSpec change；不 archive、提交或 push。父级在 `docs-order-tooling` 归档后同步 `docs-page-content` 主 spec，并在独立归档流程中创建 `docs-math` 主 spec。
