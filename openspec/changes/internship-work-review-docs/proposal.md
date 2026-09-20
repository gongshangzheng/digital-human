# Proposal: internship-work-review-docs（实习工作复盘文档体系）

## Why

阿里（钉钉数字人）实习期间的工作沉淀分散在四处：CyberVerse 仓库（代码 + management 文档 + 任务树）、InternWiki 知识库、博客文章、记忆。目标是以自己为读者，把这段经验梳理成复盘文档，支撑工作汇报、为后续继续推进数字人方向提供素材，并循此提炼可发表的文章选题。

## What Changes

- 建立**实习复盘文档体系**（本 change 为体系级总 change，不直接写正文）：
  - **双层流程**：每篇文档一个独立 change，先整理内容（资料研读、证据提取、数据表汇总），整理产物经确认后再动笔写正文
  - **文档登记表**（design 内，唯一权威）：文档的职责边界、相互关系、对应单篇 change
  - 放置：单一子文件夹 `management/docs/实习复盘/` 内平铺，不嵌套
- 另建子文件夹 `management/docs/论文笔记/`（与实习复盘平级）：后续数字人论文精读笔记的写作位置，夹内平铺，命名与 papers 库条目对应（README 定规范）；本 change 只建目录与规范，不写笔记内容
- 另建子文件夹 `management/docs/模型介绍/`（平级）：六篇——总纲《技术路线》（视频基座模型 / 动作空间扩散 / 3D GS 三路线 + 代表模型 + 优缺点）+ 五篇模型介绍（AvatarForcing、Ditto、LiveAct、OmniMate、Talker-T2AV，**一篇一个模型**），夹内平铺，各由独立单篇 change 实施，同样先整理后动笔
- 复盘 7 篇文档（各自单独 change 实施）：
  1. `数字人要点.md`（`docs-intern-fundamentals`）— 道层导论：动作（音唇同步）、身份（一致性+身份资产）、渲染合成、实时性四要素，链各术篇
  2. `身份一致性.md`（`docs-intern-identity`）— 漂移治理（模长/夹角实验）+ 身份资产与参考提供
  3. `工程改进.md`（`docs-intern-engineering`）— 工程改进合集：系统级基建 + PasteBack 贴回技术
  4. `实时性改进.md`（`docs-intern-realtime`）— 用户可感知的交互体验：首帧/开口、打断收声、待机静默、画质粒度权衡
  5. `数字人行业全景.md`（`docs-intern-industry`）— 由调研与测试成果合成：技术路线版图、15+ 模型横评（第一手数据）、竞品对标、选型结论、趋势判断
  6. `发文方向.md`（`docs-intern-paper-directions`）— 从实习工作提炼候选选题（复盘的终极出口：循实习经验做出一篇文章）
  7. `总览.md`（`docs-intern-overview`）— 实习主线、时间轴、核心工作互链、量化成果总表
- 知识库 knowledge/ 保持复制件不动；本 change 只写第一方复盘文档
- 引用锚定：涉及 CyberVerse 代码/文档处标注 `~/code/CyberVerse` 路径 + commit `4968280`

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

### Modified Capabilities
（无）

## Impact
- 新增子文件夹 3 个（实习复盘/论文笔记/模型介绍）+ 各 README；正文由单篇 change 产出
- 写作素材来源见 design.md 各登记表
