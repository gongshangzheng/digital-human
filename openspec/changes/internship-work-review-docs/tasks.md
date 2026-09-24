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
- [x] 2.6 创建并实施 `docs-intern-acceleration`（数字人加速.md）— 已完成并归档（十篇加速笔记建成后回补 10 处链接）
- [x] 2.7 创建并实施 `docs-intern-industry`（数字人行业全景.md）— 已归档
- [x] 2.8 创建并实施 `docs-intern-summary`（总结.md）— 已归档
- [x] 2.8b 创建并实施 `docs-dh-field-problems`（数字人领域问题.md）— 已归档（design 登记表第 9 行）

## 2b. 论文笔记单篇 change（可并行推进）

- [x] 2.9 创建并实施 `docs-note-avatar-forcing`（avatar-forcing.md）— 含 `-rewrite` 重写，均已归档
- [x] 2.10 创建并实施 `docs-note-ditto`（ditto.md）— 任务 29/29 完成、正文通过 `validate-note`；change 尚未归档
- [x] 2.11 创建并实施 `docs-note-liveact`（liveact.md）— 已归档
- [x] 2.12 创建并实施 `docs-note-omnimate`（omnimate.md）— 10 节 + 5 图 + 2 Mermaid，已归档
- [x] 2.13 创建并实施 `docs-note-talker-t2av`（talker-t2av.md）— 10 节 + 1 图 + 2 Mermaid（论文仅 1 张正文图，替代方案已登记），已归档
- [x] 2.14 生成侧加速十篇笔记已齐备（fpsattention 由 `docs-note-fpsattention` 完成；其余九篇由 `docs-note-gen-acceleration` 完成，其中 worldattention / dax 为无同行评议论文的仓库类笔记）— 已完成《数字人加速》10 处链接回补
- [x] 2.15 创建并实施 `docs-note-liveportrait`（liveportrait.md）— 含 5 张论文原图，未接入故按定位层写（change 待归档）
- [x] 2.16 创建并实施 `docs-note-lia-x`（lia-x.md）— 含 5 张论文原图（含三面板拼接），未接入故按定位层写（change 待归档）

## 3. 体系级验收

- [x] 3.1 复盘九篇 + 论文笔记齐备且平铺于各自子文件夹，互链正确、无嵌套
  - 验收证据（2026-09-24）：概述 **10 篇平铺**（含《数字人领域问题》《数字人关键技术地图》）、论文笔记 **23 篇平铺**；全库 wiki 链接 **343 条**，失效仅 5 条且**全部位于 `knowledge/` 导入副本**（指向不存在的《数字人工程解读》系列与 `digital-human-backend-agent-design`），属历史遗留、不在本 change 范围；`论文笔记/README` 经接口校验为有效文档页（88 篇中在列）
  - 现状：**「五篇深读」与生成侧加速十篇均已齐备**（含 8 篇论文笔记 + 2 篇仓库类方案笔记）；其余为 3.1 之后其它变更新增的条目（`wan-streamer`、`tivtok` 等）（avatar-forcing、ditto、liveact、omnimate、talker-t2av），另完成 liveportrait / lia-x / float / face-vid2vid 等定位篇；待写：生成侧加速十篇、`wan-streamer` 等后续新增条目
- [x] 3.2 抽查：量化成果总表每个数字可溯源到单篇文档；证据状态按 design D5 以**自然语言**写明
  - 验收证据：抽查三项均回源成功——身份「锚点引导 300s CSIM 0.645 → 0.935」（数字人身份 §结论）、加速「GPU 38.5ms/帧 vs 40ms 预算（96%）」（数字人加速）、工程设计「丢包隐藏 2.5–3.6% → 0.022%」（工程设计）；同时更新了已过期的「平台资产」行（论文库 117 → **118 篇**，概述/笔记篇数改为实测值）
  - 说明：原任务措辞要求的【已验证/待验证/已否证】符号体系在实现中已被 **D5「数据诚实：不使用标注符号体系、用自然语言写明」** 取代，此处按实际实现的约定验收
- [x] 3.3 openspec validate 全部通过，git 提交
