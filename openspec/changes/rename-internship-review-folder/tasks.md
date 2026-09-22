## 1. 重命名目录与配置

- [ ] 1.1 `git mv management/docs/实习复盘 management/docs/数字人概述`
- [ ] 1.2 `server/config.py`：`DOCS_FOLDER_ORDER` 首项 `'实习复盘'` → `'数字人概述'`，同步该行注释

## 2. 更新在用引用

- [ ] 2.1 目录内 6 篇（总结 / 工程设计 / 数字人加速 / 数字人身份 / 数字人动作 / 数字人行业全景）的 `[[实习复盘/...]]` → `[[数字人概述/...]]`
- [ ] 2.2 `management/docs/论文笔记/README.md`、`avatar-forcing.md`、`avatar-forcing.json`
- [ ] 2.3 `.agents/skills/article-note/phases/4-change.md`、`references/sidecar-guide.md` 的命名空间示例

## 3. 校验

- [ ] 3.1 全仓 `rg "实习复盘"` 仅命中 `openspec/changes/**`（历史记录）与本次 change 自身
- [ ] 3.2 重启后端：`GET /api/management/docs` 分组顺序为 数字人概述 → 论文笔记 → knowledge，连续请求一致
- [ ] 3.3 新路径 `GET /api/management/docs/数字人概述/数字人介绍与技术路线` 返回 200；旧路径返回 404（预期）
- [ ] 3.4 `validate-note.py` 校验 `论文笔记/avatar-forcing.md`（内链指向 `数字人概述/...` 必须存在）
- [ ] 3.5 浏览器抽查：左侧分组显示为「数字人概述」、可折叠；正文内链可跳转

## 4. 规范与提交

- [ ] 4.1 `openspec validate rename-internship-review-folder --strict` 通过
- [ ] 4.2 归档 change（把 `docs-page-content` / `docs-page-layout` 两个 delta 同步进主 specs）
- [ ] 4.3 提交（`docs: 实习复盘/ 更名为 数字人概述/（含排序配置、内链与 specs 示例同步）`）
