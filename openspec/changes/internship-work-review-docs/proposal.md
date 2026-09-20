# Proposal: internship-work-review-docs（实习工作复盘文档）

## Why

阿里（钉钉数字人）实习期间的工作沉淀分散在四处：CyberVerse 仓库（代码 + management 文档 + 任务树）、InternWiki 知识库、博客文章、记忆。目标是以自己为读者，把这段经验梳理成复盘文档，支撑工作汇报、为后续继续推进数字人方向提供素材，并循此提炼可发表的文章选题。

## What Changes

- 建立**实习复盘文档体系**（本 change 为体系级总 change，不直接写正文）：
  - **双层流程**：每篇文档一个独立 change（`docs-intern-<slug>`），先整理内容（资料研读、证据提取、数据表汇总），整理产物经确认后再动笔写正文
  - **文档登记表**（design 内，唯一权威）：5 篇文档的编号/职责边界/相互关系/对应单篇 change
  - 放置：单一子文件夹 `management/docs/实习复盘/` 内平铺，不嵌套
- 另建子文件夹 `management/docs/论文笔记/`（与实习复盘平级）：后续数字人论文精读笔记的写作位置，夹内平铺，命名与 papers 库条目对应（README 定规范）；本 change 只建目录与规范，不写笔记内容
- 另建子文件夹 `management/docs/模型介绍/`（平级）：五篇模型介绍——AvatarForcing、Ditto、LiveAct、OmniMate、Talker-T2AV，夹内平铺，各由独立单篇 change（`docs-model-<slug>`）实施，同样先整理后动笔
- 5 篇文档（各自单独 change 实施）：
  1. `总览.md`（`docs-intern-overview`）— 实习主线、时间轴、三项核心工作、量化成果总表
  2. `身份一致性.md`（`docs-intern-identity`）— AvatarForcing 身份漂移治理
  3. `PasteBack.md`（`docs-intern-pasteback`）— 两条贴回路径与接缝/波动修复
  4. `CyberVerse工程改进.md`（`docs-intern-cyberverse`）— 实时链路工程优化全集
  5. `发文方向.md`（`docs-intern-paper-directions`）— 从三项工作提炼候选选题（复盘的终极出口：循实习经验做出一篇文章）
- 知识库 knowledge/ 保持复制件不动；本 change 只写第一方复盘文档
- 引用锚定：涉及 CyberVerse 代码/文档处标注 `~/code/CyberVerse` 路径 + commit `4968280`

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

### Modified Capabilities
（无）

## Impact
- 仅新增 `management/docs/*.md` 4 个文件，不改动代码
- 写作素材来源登记见 design.md「资料调研」节
