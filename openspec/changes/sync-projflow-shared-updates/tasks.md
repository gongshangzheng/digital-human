# Tasks: sync-projflow-shared-updates

## 1. 中文 slug 修复（docs-page-content）

- [x] 1.1 放宽 `server/routers/management.py` 的 `_SLUG_RE` 支持 Unicode/空格，并在取 slug 前 `unquote`；保留 `..` 与路径穿越防护
- [x] 1.2 验证：`GET /api/management/docs/knowledge/数字人基础` 与 `.../实习复盘/数字人介绍与技术路线` 返回 200；`..` 请求被拒

## 2. 采用上游 HIDDEN_KEYS，退役 menu.js（menu-visibility）

- [x] 2.1 引入上游 `web/src/config/hidden.js`（HIDDEN_KEYS + 分组/报告类型隐藏逻辑），并把我们的隐藏集合迁入
- [x] 2.2 `MainLayout.vue` 改用 hidden.js 过滤；`Home.vue` 的 `isMenuHidden` 引用同步迁移；删除 `web/src/config/menu.js`
- [x] 2.3 移植 `ReportPage.vue` 的报告类型 tab 隐藏逻辑
- [x] 2.4 验证：四项目标隐藏项不显示、路由直达可用、从 HIDDEN_KEYS 移除后恢复；分组自动隐藏正确

## 3. 移植文档页能力（docs-page-layout / docs-page-content）

- [x] 3.1 `server/routers/management.py`：读取 `<slug>.json` 并在详情返回 `sidecar`
- [x] 3.2 `web/src/utils/markdown.js`：TOC 去掉 `**` 强调符号
- [x] 3.3 `DocPage.vue`：移植 sidecar 区块（顶部演进/进度按钮 + 底部相关文档/附录）与左右侧栏收起（含 localStorage 持久化）
- [x] 3.4 `DocPage.vue`：移植左侧文档列表子目录折叠展开（含持久化）
- [x] 3.5 验证：侧栏收起/展开、刷新保持、窄屏断点不显示把手、sidecar 有/无两种情况渲染正确、章节列表无 `**`

## 4. 保留定制与回归

- [x] 4.1 核对端口仍为 8812/3212、身份名与 localStorage 键未被上游覆盖
- [x] 4.2 `cd web && npx vite build` 通过；`bash start_services.sh` 冷启动冒烟（后端 /api/health、前端 200）
- [x] 4.3 `diff -rq` 复核共享层，确认无遗漏的纯上游差异（仅剩我们的定制差异）

## 5. 收尾

- [x] 5.1 记录上游回灌待办（中文 slug 修复 + hidden.js 采用经验 → `[shared]` 回灌 ProjFlow）
- [x] 5.2 `openspec validate sync-projflow-shared-updates` 通过，提交
