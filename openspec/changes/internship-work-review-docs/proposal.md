# Proposal: internship-work-review-docs（实习工作复盘文档体系）

## Why

阿里（钉钉数字人）实习期间的工作沉淀分散在四处：CyberVerse 仓库（代码 + management 文档 + 任务树）、InternWiki 知识库、博客文章、记忆。目标是以自己为读者，把这段经验梳理成复盘文档，支撑工作汇报、为后续继续推进数字人方向提供素材，并循此提炼可发表的文章选题。

## What Changes

- 建立**实习复盘文档体系**（本 change 为体系级总 change，不直接写正文）：
  - **双层流程**：每篇文档一个独立 change，先整理内容（资料研读、证据提取、数据表汇总），整理产物经确认后再动笔写正文
  - **文档登记表**（design 内，唯一权威）：文档的职责边界、相互关系、对应单篇 change
  - 放置：单一子文件夹 `management/docs/实习复盘/` 内平铺，不嵌套
- 子文件夹两个：`management/docs/实习复盘/`（复盘 8 篇）与 `management/docs/论文笔记/`（统一笔记库，合并原"模型介绍"）：五篇深读笔记（AvatarForcing、Ditto、LiveAct、OmniMate、Talker-T2AV，一篇一个对象，含"在我们体系中的角色"工程层）+ 后续新读论文笔记；夹内平铺，各由独立单篇 change（`docs-note-<slug>`）实施，先整理后动笔
- **内容文档统一写作骨架**：为什么重要 → 现行做法（该方向的信息总结）→ 我们的工作 → 可能的改进方向；不是单纯写改进流水账
- 复盘 7 篇文档（各自单独 change 实施）：
  1. `数字人介绍与技术路线.md`（`docs-intern-intro`）— 数字人概览 + 主要技术路线（两轴框架 + 六条路线）+ 优缺点 + 评价体系（合并原"要点"与"技术路线"）
  2. `CyberVerse框架.md`（`docs-intern-cyberverse`）— 数字人 Agent 框架 CyberVerse 介绍：架构、插件体系、模型接入、部署形态
  3. `数字人身份.md`（`docs-intern-identity`）— 算法上的改进：身份漂移治理（模长/夹角实验）+ 身份资产与参考提供
  4. `数字人动作.md`（`docs-intern-motion`）— 算法上的改进：分层框架（音唇同步→表情×语言交互→手部/全身），含我们的实验与市面工作总结
  6. `工程改进.md`（`docs-intern-engineering`）— 工程上的改进合集：系统级基建 + PasteBack 贴回技术
  5. `实时性改进.md`（`docs-intern-realtime`）— 用户可感知的交互体验：首帧/开口、打断收声、待机静默、画质粒度权衡
  6. `数字人行业全景.md`（`docs-intern-industry`）— 由调研与测试成果合成：技术路线版图、15+ 模型横评（第一手数据）、竞品对标、选型结论、趋势判断
  6. `发文方向.md`（`docs-intern-paper-directions`）— 从实习工作提炼候选选题（复盘的终极出口：循实习经验做出一篇文章）
  8. `总览.md`（`docs-intern-overview`）— 实习主线、时间轴、核心工作互链、量化成果总表
- 知识库 knowledge/ 保持复制件不动；本 change 只写第一方复盘文档
- 引用锚定：涉及 CyberVerse 代码/文档处标注 `~/code/CyberVerse` 路径 + commit `4968280`

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

### Modified Capabilities
（无）

## Impact
- 新增子文件夹 2 个（实习复盘/论文笔记）+ 各 README；正文由单篇 change 产出
- 写作素材来源见 design.md 各登记表
