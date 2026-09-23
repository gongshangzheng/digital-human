# Tasks: internship-work-review-docs（体系级总 change）

> 本 change 不写正文。正文由各单篇 change（见 design 登记表）实施，每篇先「资料整理」后「动笔写作」。
> 状态口径：已完成的条目在行尾登记实施它的单篇 change；归档位置见 `openspec/changes/archive/`。

## 1. 体系建立

- [x] 1.1 建立文档登记表（design 内，唯一权威）：各文档职责边界、依赖顺序、对应单篇 change
- [x] 1.2 确立双层流程规则：单篇 change = 整理任务组 + 写作任务组，整理产物经确认后再动笔
- [x] 1.3 建 `management/docs/论文笔记/` 目录 + README（10 节统一模板、命名挂 papers 库条目、清单含五篇深读 + liveportrait/lia-x + 生成侧加速十篇）

## 2. 复盘单篇 change（按依赖顺序，逐篇创建与实施）

- [x] 2.1 创建并实施 `docs-intern-intro`（数字人介绍与技术路线.md）— 已归档
- [x] 2.2 创建并实施 `docs-intern-identity`（数字人身份.md）— 已归档
- [x] 2.3 创建并实施 `docs-intern-motion`（数字人动作.md）— 已归档
- [x] 2.4 创建并实施 `docs-intern-cyberverse`（CyberVerse框架.md）— 已归档
- [x] 2.5 创建并实施 `docs-intern-design`（工程设计.md）— 已归档
- [ ] 2.6 创建并实施 `docs-intern-acceleration`（数字人加速.md）— 未归档，由进行中的 `docs-intern-acceleration` 承接（当前 10/11；剩余 3.1 待十篇笔记建成后补链接）
- [x] 2.7 创建并实施 `docs-intern-industry`（数字人行业全景.md）— 已归档
- [x] 2.8 创建并实施 `docs-intern-summary`（总结.md）— 已归档
- [x] 2.8b 创建并实施 `docs-dh-field-problems`（数字人领域问题.md）— 已归档（design 登记表第 9 行）

## 2b. 论文笔记单篇 change（可并行推进）

- [x] 2.9 创建并实施 `docs-note-avatar-forcing`（avatar-forcing.md）— 含 `-rewrite` 重写，均已归档
- [x] 2.10 创建并实施 `docs-note-ditto`（ditto.md）— 任务 29/29 完成、正文通过 `validate-note`；change 尚未归档
- [ ] 2.11 创建并实施 `docs-note-liveact`（liveact.md）
- [ ] 2.12 创建并实施 `docs-note-omnimate`（omnimate.md）
- [ ] 2.13 创建并实施 `docs-note-talker-t2av`（talker-t2av.md）
- [ ] 2.14 批量创建生成侧加速十篇笔记（fpsattention / blade / nar / flashar / latent-spatial-memory / worldattention / zipar / dax / turbodiffusion / inferix）— 由 `docs-intern-acceleration` 3.1 收口：建成后回《数字人加速》补链接
- [x] 2.15 创建并实施 `docs-note-liveportrait`（liveportrait.md）— 含 5 张论文原图，未接入故按定位层写（change 待归档）
- [x] 2.16 创建并实施 `docs-note-lia-x`（lia-x.md）— 含 5 张论文原图（含三面板拼接），未接入故按定位层写（change 待归档）

## 3. 体系级验收

- [ ] 3.1 复盘九篇 + 论文笔记齐备且平铺于各自子文件夹，互链正确、无嵌套
  - 现状：复盘九篇齐备；笔记已完成 `avatar-forcing`、`ditto`，待写 liveact / omnimate / talker-t2av / liveportrait / lia-x 与生成侧加速十篇
- [ ] 3.2 抽查：量化成果总表每个数字可溯源到单篇文档；【已验证/待验证/已否证】标注齐全
- [ ] 3.3 openspec validate 全部通过，git 提交
