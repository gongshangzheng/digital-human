# Tasks: internship-work-review-docs（体系级总 change）

> 本 change 不写正文。正文由各单篇 change（见 design 登记表）实施，每篇先「资料整理」后「动笔写作」。

## 1. 体系建立

- [x] 1.1 建立文档登记表（design 内，唯一权威）：各文档职责边界、依赖顺序、对应单篇 change
- [x] 1.2 确立双层流程规则：单篇 change = 整理任务组 + 写作任务组，整理产物经确认后再动笔
- [ ] 1.3 建 `management/docs/论文笔记/` 目录 + README（统一模板：论文层 + 可选工程层；命名挂 papers 库条目；含总纲《技术路线》与五篇深读清单）

## 2. 复盘单篇 change（按依赖顺序，逐篇创建与实施）

- [ ] 2.1 创建并实施 `docs-intern-fundamentals`（数字人要点.md，技术要素总览）
- [ ] 2.2 创建并实施 `docs-intern-identity`（身份.md）
- [ ] 2.3 创建并实施 `docs-intern-motion`（动作.md，分层框架：音唇同步→表情×语言→手部）
- [ ] 2.4 创建并实施 `docs-intern-engineering`（工程改进.md，含 PasteBack）
- [ ] 2.4 创建并实施 `docs-intern-realtime`（实时性改进.md）
- [ ] 2.5 创建并实施 `docs-intern-industry`（数字人行业全景.md，含 papers 库 related-work 扫描与模型横评数据汇总）
- [ ] 2.6 创建并实施 `docs-intern-paper-directions`（发文方向.md）
- [ ] 2.7 创建并实施 `docs-intern-overview`（总览.md，汇总前六篇成果）

## 2b. 论文笔记单篇 change（可并行推进）

- [ ] 2.8 创建并实施 `docs-note-routes`（技术路线.md 总纲索引）
- [ ] 2.9 创建并实施 `docs-note-avatar-forcing`
- [ ] 2.10 创建并实施 `docs-note-ditto`
- [ ] 2.11 创建并实施 `docs-note-liveact`
- [ ] 2.12 创建并实施 `docs-note-omnimate`
- [ ] 2.13 创建并实施 `docs-note-talker-t2av`

## 3. 体系级验收

- [ ] 3.1 复盘八篇 + 论文笔记（总纲 + 五篇深读）齐备且平铺于各自子文件夹，互链正确、无嵌套
- [ ] 3.2 抽查：量化成果总表每个数字可溯源到单篇文档；【已验证/待验证/已否证】标注齐全
- [ ] 3.3 openspec validate 全部通过，git 提交
