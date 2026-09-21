# Tasks: internship-work-review-docs（体系级总 change）

> 本 change 不写正文。正文由各单篇 change（见 design 登记表）实施，每篇先「资料整理」后「动笔写作」。

## 1. 体系建立

- [x] 1.1 建立文档登记表（design 内，唯一权威）：各文档职责边界、依赖顺序、对应单篇 change
- [x] 1.2 确立双层流程规则：单篇 change = 整理任务组 + 写作任务组，整理产物经确认后再动笔
- [ ] 1.3 建 `management/docs/论文笔记/` 目录 + README（统一模板：论文层 + 可选工程层；命名挂 papers 库条目；五篇深读清单）

## 2. 复盘单篇 change（按依赖顺序，逐篇创建与实施）

- [ ] 2.1 创建并实施 `docs-intern-intro`（数字人介绍与技术路线.md）
- [ ] 2.2 创建并实施 `docs-intern-identity`（数字人身份.md）
- [ ] 2.3 创建并实施 `docs-intern-motion`（数字人动作.md，分层框架：音唇同步→表情×语言→手部；含微调 Loss（geom/RKD）与注入点消融）
- [ ] 2.4 创建并实施 `docs-intern-cyberverse`（CyberVerse框架.md）
- [ ] 2.5 创建并实施 `docs-intern-design`（工程设计.md，设计视角：整体链路 / 贴回 / 传输与发布 / 音频链路 / 会话与资源生命周期 / 稳定性 / 未采纳）
- [ ] 2.6 创建并实施 `docs-intern-acceleration`（数字人加速.md：只写"快"——实时性指标与延迟链、生成侧加速、系统侧加速、模型实时性横评、硬件档位与可行性、未采纳方案；按 D7 从《工程设计》《数字人行业全景》搬迁性能与实时性章节）
- [ ] 2.7 创建并实施 `docs-intern-industry`（数字人行业全景.md：模型横评（第一手待补）、竞品与产品调研、选型结论、未采纳与待复跑、趋势判断）
- [ ] 2.8 创建并实施 `docs-intern-summary`（总结.md：总览 + 发文方向，数字从 1–7 汇总）

## 2b. 论文笔记单篇 change（可并行推进）

- [ ] 2.9 创建并实施 `docs-note-avatar-forcing`
- [ ] 2.10 创建并实施 `docs-note-ditto`
- [ ] 2.11 创建并实施 `docs-note-liveact`
- [ ] 2.12 创建并实施 `docs-note-omnimate`
- [ ] 2.13 创建并实施 `docs-note-talker-t2av`

## 3. 体系级验收

- [ ] 3.1 复盘七篇 + 论文笔记五篇深读齐备且平铺于各自子文件夹，互链正确、无嵌套
- [ ] 3.2 抽查：量化成果总表每个数字可溯源到单篇文档；【已验证/待验证/已否证】标注齐全
- [ ] 3.3 openspec validate 全部通过，git 提交
