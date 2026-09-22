## Why

ProjFlow 在本仓库最近一次同步（`[shared]` 主题与 favicon）之后新增了三项已提交的共享文档发布能力：构建期静态化文档、随构建发布文档图片，以及 GitHub Pages 部署通道。Digital Human 已有文档页与图片端点，却仍完全依赖本地 FastAPI；因此无法在无后端的静态站点上浏览已有文档和配图，也没有上游一致的发布路径。

## What Changes

- 选择性同步 ProjFlow 已提交的 `[shared]` 更新 `63f643a → 8506eaf → 6d2aa36`：构建期把 `management/docs/` 与 sidecar 编译为静态数据，生产环境读取该数据而开发环境继续请求 FastAPI，并为 history 路由生成 `404.html` 回退。
- 同步文档图片静态化：把 `management/docs/_assets/` 构建为前端静态资产，生产读取文档时将既有 `/api/management/docs-assets/` 引用改写为部署基路径下的资源；除为兼容上游轻量 frontmatter 构建器而扁平化 `management/docs/knowledge/project-README.md` 的非关键元数据外，源 Markdown 与开发行为不变。
- 新增 GitHub Pages Actions 部署流程；以 `/<仓库名>/` 作为构建 / preview 的基路径、本地开发保持 `/`，并让 Vue Router 使用运行时基路径。
- 按 Digital Human 的仓库名、端口、前端依赖、既有文档和存储键进行下游适配；不携带 ProjFlow 的 OpenSpec 历史、身份文案或未经审查的非共享功能。

## Capabilities

### New Capabilities

- `docs-static-build`: 在无 FastAPI 的静态托管环境中构建和读取管理文档、sidecar 与文档图片，并提供 SPA 文档深链接回退。
- `pages-deploy`: 将前端构建产物部署至 GitHub Pages，同时让构建与开发的基路径保持各自可用。

### Modified Capabilities

- `docs-page-content`: 文档详情的生产数据来源从仅后端 API 扩展为构建期静态数据；既有 Markdown 文档图片在静态托管时必须可解析。

## Impact

- 前端：新增构建脚本和 `api/docs.js`，修改 `DocPage.vue`、`web/package.json`、`web/vite.config.js`、Vue Router；新增 GitHub Actions workflow。
- 文档资产：构建时生成且不提交 `web/public/docs-data.json` 与 `web/public/docs-assets/`；`management/docs/_assets/` 保持原位，且仅将 `management/docs/knowledge/project-README.md` 的 frontmatter 降级为构建器支持的扁平字段。
- 后端：不改动，仍为本地开发提供实时文档接口和图片端点。
- 部署：需要仓库拥有 GitHub Pages 工作流发布权限；线上静态站点仅保证文档页可读，其他依赖 FastAPI / SQLite 的模块不在本 change 的降级范围内。
