## Context

本仓库是 ProjFlow 下游，最近一次同步 `sync-projflow-round5` 已取入上游主题能力，但当前 Digital Human 仍缺少 ProjFlow 最新的静态文档发布链路。上游 `~/code/ProjFlow` 工作树干净，固定以已提交的 `[shared]` 提交为来源：

| 上游提交 | 能力 | 下游现状 |
|---|---|---|
| `63f643a` | 文档静态数据、生产 / 开发取数切换、`404.html` | 缺 `web/scripts/`、`web/src/api/docs.js`；`DocPage.vue` 直连 `api/management` |
| `8506eaf` | `_assets` 构建期复制与正文图片 URL 改写 | 已有后端图片端点和实际 Avatar Forcing 图片，但静态部署会 404 |
| `6d2aa36` | Pages workflow、条件 base、Router base | 无 `.github/workflows/`；Vite / Router 未处理仓库子路径 |

下游与上游的必要差异：默认分支是 `master` 而非 `main`；本地端口为 8812 / 3212；新建且公开的 GitHub 仓库已确认是 `gongshangzheng/digital-human`，Pages 路径固定为 `/digital-human/`；源文档数量和 `management/docs/_assets/avatar-forcing/` 均已存在。`server/routers/management.py` 已定义文档扫描、frontmatter、sidecar 与排序链，可作为构建器与运行时行为的一致性基准。

## Goals / Non-Goals

**Goals:**

- 完整移植上游三项相互依赖的共享能力，并保留 Digital Human 的项目身份与本地开发行为。
- 让同一份源 Markdown 在开发时继续配合 FastAPI、在 GitHub Pages 上用构建快照和静态图片呈现。
- 使用 `npm run build` 作为唯一完整构建入口，并使 `vite preview` 能复现 Pages 的基路径。

**Non-Goals:**

- 不把 ProjFlow 的 `openspec/changes/**`、README / AGENTS 的上游身份文本、端口或菜单策略整体覆盖到下游。
- 不把 FastAPI、SQLite、论文、评测或项目树模块静态化；Pages 上这些模块没有数据后端不属于本次故障。
- 不修改 `management/docs/` 的正文、图片源目录或 DPO 技术介绍 change 的内容；唯一例外是将非关键的 `knowledge/project-README.md` 嵌套 frontmatter 扁平化为上游轻量构建器支持的字段。
- 不添加数据库迁移，也不在本地运行生产数据库迁移。

## Decisions

### 1. 以三个上游已提交的共享 commit 为唯一来源，选择性移植而非 merge / cherry-pick

实施时以 `git -C ~/code/ProjFlow show <commit> -- <path>` 逐文件核对并取用：`63f643a → 8506eaf → 6d2aa36`。不 merge 上游历史，也不整体 cherry-pick：两库 Git 历史无共同父提交，且上游 change、仓库名、端口、README 等不适合进入下游。

备选「只取最新 `6d2aa36`」不可用，因为其部署链依赖前两项生成的静态数据、图片与 `404.html`；备选「只同步静态化、不部署」不能实现用户要求的最新完整共享能力，因此不采用。

### 2. 静态文档生成复刻当前后端契约

新增 `web/scripts/build-docs-data.mjs`，由 `web/package.json` 的 `prebuild` 触发。脚本在构建期读取 `management/docs/`，跳过下划线目录；提取与后端一致的列表字段、去 frontmatter 后正文和 sidecar，按 `DOCS_FOLDER_ORDER → order → id → date 降序 → slug` 排序后写入被忽略的 `web/public/docs-data.json`。

脚本读取 `server/config.py` 的 `DOCS_FOLDER_ORDER` 字面量，避免在前后端维护两份目录顺序。为保持与上游共享实现一致且不增加 YAML 解析依赖，frontmatter 仅支持单行标量和内联数组；实施时将当前唯一含嵌套 YAML 的非关键文档 `management/docs/knowledge/project-README.md` 扁平化（删除不被列表/详情页面使用的 `timeline`，把 `tags` 改为内联数组）。其他不支持的 YAML 或非法 JSON 显式失败，避免静默发布残缺数据。

`web/src/api/docs.js` 是唯一来源切换层：开发调用现有 `api/management.js`，生产按 `BASE_URL` 拉取并缓存 `docs-data.json`。`DocPage.vue` 仅改为导入该层。备选「在组件内分支」会耦合页面与部署模式，因此不采用。

### 3. 静态化图片但不改写源 Markdown

在同一个构建脚本中，先清空 `web/public/docs-assets/`，再复制 `management/docs/_assets/` 的非隐藏文件，以确保构建产物是完整快照、删除的源图不会残留。生产取数层把正文 `/api/management/docs-assets/` 前缀改为 `${BASE_URL}docs-assets/`；开发分支与 Markdown 源文件不变。

备选「直接批量替换 Markdown 图片 URL」会破坏本地后端端点和 article-note 的资产约定；备选「不复制资产」会使已有 Avatar Forcing 配图在 Pages 中失效，均不采用。

### 4. 部署 / 预览基路径条件化，保持开发根路径

Vite 配置在 build 或 preview 时使用 `/digital-human/`，开发时使用 `/`；Router 改为 `createWebHistory(import.meta.env.BASE_URL)`。该路径已由新远端 `gongshangzheng/digital-human` 固定，不可沿用 `/ProjFlow/`。

这使 `http://localhost:3212/` 维持现状，而 `npm run preview` 可提前发现子路径资源、路由和静态数据问题。使用常设子路径 base 会改变日常开发 URL，故不采用。

### 5. GitHub Pages workflow 以 `master` 为触发分支

新增 `.github/workflows/deploy.yml`：`push` 到 `master` 或 `workflow_dispatch` → Node 22 → 在 `web/` 下 `npm install --no-audit --no-fund` 和 `npm run build` → `configure-pages` / `upload-pages-artifact` / `deploy-pages`。工作流使用 Pages 需要的最小权限及并发组。新公开仓库首次推送后，将部署源设置为 GitHub Actions 并检查首个 workflow。

备选复用上游的 `main` 触发器会使当前仓库 push 不触发，因此不采用。

### 6. 文档与可验证边界

更新本仓库 `AGENTS.md` 与 `README.md`，仅记录 Digital Human 的线上地址、条件 base、完整构建命令及「Pages 只保证文档页」边界。修改本 change 的相关 spec delta；不变更主 spec，直至 apply 完成并按流程同步。

## Risks / Trade-offs

- [错误沿用 `/ProjFlow/` 或 Pages 未启用] → 已固定 `gongshangzheng/digital-human` 和 `/digital-human/`；首次推送后将部署源设置为 GitHub Actions，并把该 base 统一写入 Vite、说明文档和验证 URL。
- [构建器只支持 YAML 子集，未来 frontmatter 改为多行嵌套结构] → 已扁平化唯一现有非关键实例；其余情况非零失败且定位行号，再单独扩展解析器，不发布错误快照。
- [生产构建绕过 npm lifecycle] → 文档明确 `npm run build` 是完整入口，workflow 不直接调用 `vite build`。
- [静态资产复制泄漏旧文件] → 每轮复制前清空输出目录，并以删除源图后重建的负向检查验证。
- [工作流仅有文档静态数据，读者误以为全站可用] → README / AGENTS 明确 Pages 无后端，非文档模块不保证数据。

## Migration Plan

1. 已确认远端为公开的 `gongshangzheng/digital-human`，发布分支为 `master`，部署 base 为 `/digital-human/`。
2. 将 `knowledge/project-README.md` 的 frontmatter 扁平化为受支持字段；正文保持不变。
3. 从上述上游提交选择性新增脚本、来源层和 workflow，按下游分支、端口与仓库名适配；更新 `.gitignore`、`package.json`、Vite / Router、README / AGENTS。
4. 运行 `npm run build`，核验 `docs-data.json`、`docs-assets/`、`404.html`；比对静态列表和本地文档 API 的字段与排序，确认除已批准的非关键 frontmatter 适配外，源 Markdown 未改写。
5. 以开发服务器和 `npm run preview` 分别验证根路径开发、子路径文档首页 / 详情 / 图片 / 刷新深链接；验证非文档模块的既定空态边界。
6. 首次推送 `master` 后，将 Pages 部署源设为 GitHub Actions，观察首个 workflow，检查线上文档和图片。若失败，revert 本 change 的共享提交并关闭 workflow；源文档正文、资产和数据库不会被修改。
