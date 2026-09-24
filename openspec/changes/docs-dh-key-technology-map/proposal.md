## Why

数字人调研素材集中在博客仓库 `~/gongshangzheng.github.io` 的 `AI/数字人` 子分类（已发布 99 篇，另有约 20 篇草稿）。这些文章各自回答「某篇论文用什么技术解决什么问题」，但没有任何一篇把它们横向拉通。更关键的是：**当前所有信息都是散文式的，没有结构化数据**——无法按机构、时间、方法族筛选，也无法在文档里稳定地呈现一张随数据更新的总表。

本次要建立的最小数据单元是**每篇文章的「问题 → 解法」对**：一篇文章 = 一条 `question`/`answer` 记录，附带标题、作者、发布机构、venue·年份、以及指向库内详细笔记的位置。这个结构单元落盘为配套 JSON，文档中的表格直接由该 JSON 渲染，而不是手工维护。

## What Changes

- **定义论文信息对的数据结构**：每条记录含 `id / title / authors / institution / venue / year / question / answer / method_family / blog_url / blog_date / note / note_type / tags` 等字段（详见 design）。
- **生成配套 JSON**：从 `AI/数字人` 语料逐篇抽取「问题-解法」对，落盘为可与文档同名的 sidecar JSON（推荐）或 `_assets/<slug>/papers.json`（备选），作为表格的唯一数据源。
- **文档内表格由 JSON 实时渲染**：文档正文放置占位标记，文档页在该位置渲染一张由 JSON 驱动的表格，支持按列排序与按方法族筛选；「笔记」列把重点文章引向库内详细解读（站内文档）或博客原文（外链）。
- **新增说明性文档**：说明数字人领域关键技术（分线：问题 → 方法族 → 代表工作【机构·时间】 → 边界），并补充关键问题，附演进时间线与机构分布。
- **前端渲染能力**：新增 `PaperTable` 组件与占位标记解析（开发模式读 FastAPI 详情接口，生产静态构建读同等详情数据，行为一致）；扩展 `docs-page-content` 契约以覆盖 sidecar `papers` 与文档内表格。
- 不重复既有文档的数字与结论；表格「笔记」列以 slug 指向对应精读。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `docs-page-content`: 文档同名 sidecar json 在既有 `changelog` / `progress` / `appendix` / `related` 之外新增可选 `papers` 字段；文档页须支持正文占位标记并在该位置渲染由 `papers` 驱动的信息表；明确开发/生产两种取数来源必须渲染一致，无 `papers` 的文档不得渲染空表。

## Impact

- **文档**：新增一篇说明性文档（落点待裁决，推荐 `management/docs/数字人概述/`），并更新该目录 `order`。
- **数据**：新增配套 JSON（sidecar `<slug>.json` 的 `papers` 字段，或独立资产文件），以及可复跑的抽取脚本（推荐）。
- **前端**：`web/src/views/management/DocPage.vue`（占位标记解析与组件挂载）、新增 `web/src/components/common/PaperTable.vue`；生产构建沿用既有 sidecar 注入路径，`build-docs-data.mjs` 无需改动（若选独立资产方案则需确认资产复制）。
- **规格**：`docs-page-content` 新增一条需求（delta）。
- **不改**：论文精读目录与 `knowledge/` 复制件；前后端 API 路由契约（sidecar 透传已存在）。
- 素材源：`~/gongshangzheng.github.io`（`src/pages/*.html`、`drafts/*`、`public/search-index.json`）、库内 `papers/data/blog_papers.json`、`data/papers.db`。
