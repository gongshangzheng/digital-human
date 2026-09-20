# Tasks: docs-list-ordering

## 1. 服务端排序

- [ ] 1.1 `get_docs` 解析 `order` 字段并加入响应
- [ ] 1.2 排序链改为「文件夹优先级 → `order` → `id` → `date` 降序 → slug」；文件夹优先级用 `_DOCS_FOLDER_ORDER` 常量（默认 `实习复盘 → 论文笔记 → knowledge`）
- [ ] 1.3 验证：无 `order` 时知识库 22 篇顺序不变；同 date 同无 id 的两篇顺序确定且可复现

## 2. 文档补 `order`

- [ ] 2.1 `实习复盘/数字人介绍与技术路线.md` → `order: 1`；`实习复盘/CyberVerse框架.md` → `order: 2`（后续按登记表顺延）
- [ ] 2.2 验证：列表与左侧树中 实习复盘 文件夹排最前，入门篇在 CyberVerse 之前

## 3. 收尾

- [ ] 3.1 更新 `doc-writing` skill 的 frontmatter 表（`order` 字段与排序链）
- [ ] 3.2 记录 `[shared]` 回灌待办（排序逻辑 → ProjFlow）
- [ ] 3.3 `openspec validate docs-list-ordering` 通过并提交
