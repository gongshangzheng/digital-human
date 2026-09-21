# Tasks: sync-projflow-round2

## 1. 移植上游滚动位置恢复

- [ ] 1.1 取上游 `web/src/utils/scrollMemory.js` 到本仓库
- [ ] 1.2 按上游接入点在 `DocPage.vue` 合并（保留我们的侧栏收起 / sidecar / 子目录折叠 / 锚点接管）
- [ ] 1.3 浏览器验收：刷新恢复、切换文档分别记忆、首次进入停在顶部、锚点跳转仍正常

## 2. 回灌与登记

- [ ] 2.1 `docs/external-sources.md`：中文 slug 项标记为**已回灌**（上游 c47d588 pick 自本仓库）；新增**文内锚点接管**回灌待办
- [ ] 2.2 记录 `.agents/skills` 迁移不采纳的原因（本仓库无仓库级技能目录）
- [ ] 2.3 `openspec validate sync-projflow-round2 --strict` 通过并提交
