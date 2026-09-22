## 1. 固定上游来源与下游部署身份

- [x] 1.1 固定仅同步 ProjFlow 已提交的 `[shared]` 更新 `63f643a → 8506eaf → 6d2aa36`，逐文件核对，不带入上游 OpenSpec 历史或身份文案。
- [x] 1.2 核对并记录公开远端 `gongshangzheng/digital-human`、`/digital-human/` 部署子路径及首次推送后的 GitHub Pages workflow 启用状态。
- [x] 1.3 确认当前 `master` 是发布分支，前端本地端口为 3212，且 `management/docs/_assets/` 中的现有图片可作为静态化验证样本。
- [x] 1.4 将非关键 `management/docs/knowledge/project-README.md` 的 frontmatter 扁平化为上游轻量构建器支持的字段；删除未被文档页使用的嵌套元数据并保持正文不变。

## 2. 静态文档与资产构建

- [x] 2.1 从上游选择性引入并适配 `web/scripts/build-docs-data.mjs`：扫描文档 / sidecar，跳过资产目录，复刻后端字段与排序；支持扁平 frontmatter，并对其他不完整输入显式失败。
- [x] 2.2 在构建脚本中引入 `_assets` 清空后复制、文件计数与静态数据写入；更新 `.gitignore` 忽略生成的 JSON 和图片目录。
- [x] 2.3 新增 `web/scripts/copy-404.mjs`，并在 `web/package.json` 以 prebuild / postbuild 串接完整构建链。
- [x] 2.4 新增 `web/src/api/docs.js`，实现开发 API / 生产静态数据切换和静态图片 URL 改写；修改 `DocPage.vue` 仅从该层取得文档数据。

## 3. GitHub Pages 路径与部署

- [x] 3.1 按最终仓库子路径适配 `web/vite.config.js`：构建和 preview 使用子路径，开发使用根路径；保持 3212 端口和 `/api` 代理不变。
- [x] 3.2 修改 Vue Router 使用 `import.meta.env.BASE_URL`，确保根路径开发和子路径部署都能匹配文档详情路由。
- [x] 3.3 新增 `.github/workflows/deploy.yml`：`master` push / 手动触发、Node 22、`web/` 下 `npm install` 与 `npm run build`、Pages artifact / deploy 权限及并发控制。
- [x] 3.4 首次推送后启用 GitHub Pages 的 workflow 部署源；如权限或仓库设置阻断，则暂停部署步骤并向用户报告。
- [x] 3.5 更新 `AGENTS.md` 与 `README.md`，写明 Digital Human 的 Pages 地址、条件 base、完整构建命令和「线上仅文档页」边界。

## 4. 验证与交付

- [x] 4.1 运行 `npm run build`，确认产物含 `docs-data.json`、静态 `docs-assets/` 与内容一致的 `404.html`，且除已批准的 `project-README.md` frontmatter 适配外，源 Markdown 未被改写。
- [x] 4.2 比对静态数据与本地 `GET /api/management/docs` 的字段和排序；验证 sidecar、扁平 frontmatter / 无效 JSON 的失败信息以及删除源资产后不残留旧文件。
- [x] 4.3 验证开发模式仍从 FastAPI 加载，且 `http://localhost:3212/` 无需子路径；用 `npm run preview` 验证部署子路径下文档列表、详情、图片和刷新深链接。
- [x] 4.4 推送后检查 GitHub Actions 首次部署、线上文档首页 / 深链接 / 图片；记录非文档模块的无后端边界。
- [x] 4.5 运行 `openspec validate --change sync-projflow-round6`，提交共享同步改动并按流程归档。
