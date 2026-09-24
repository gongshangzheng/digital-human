# Proposal: internship-work-review-docs（实习工作复盘文档体系）

## Why

阿里（钉钉数字人）实习期间的工作沉淀分散在四处：CyberVerse 仓库（代码 + management 文档 + 任务树）、InternWiki 知识库、博客文章、记忆。目标是以自己为读者，把这段经验梳理成复盘文档，支撑工作汇报、为后续继续推进数字人方向提供素材，并循此提炼可发表的文章选题。

## What Changes

- 建立**数字人复盘文档体系**（本 change 为体系级总 change，不直接写正文）：
  - **双层流程**：每篇文档一个独立 change，先整理内容（资料研读、证据提取、数据表汇总），整理产物经确认后再动笔写正文
  - **文档登记表**（design 内，唯一权威）：文档的职责边界、相互关系、对应单篇 change
  - 放置：单一子文件夹 `management/docs/数字人概述/`（原 `实习复盘/`）内平铺，不嵌套
- 子文件夹两个：`management/docs/数字人概述/`（复盘 9 篇）与 `management/docs/论文笔记/`（统一笔记库，合并原"模型介绍"）：一篇一个论文/模型，按 10 节骨架成文（模板以 `论文笔记/README.md` 为唯一权威），深度接入过的模型含工程层内容；夹内平铺，各由独立单篇 change（`docs-note-<slug>`）实施，先整理后动笔
- **内容文档统一写作骨架**：为什么重要 → 现行做法（该方向的信息总结）→ 我们的工作 → 可能的改进方向；不是单纯写改进流水账
- 复盘 9 篇文档（各自单独 change 实施）：
  1. `数字人介绍与技术路线.md`（`docs-intern-intro`）— 数字人概览 + 主要技术路线（两轴框架 + 六条路线）+ 优缺点 + 评价体系（合并原"要点"与"技术路线"）
  2. `数字人领域问题.md`（`docs-dh-field-problems`）— 领域级开放问题：身份 / 动作 / 实时性 / 条件与任务定义 / 跨域约束各自的问题与难点
  3. `数字人身份.md`（`docs-intern-identity`）— 算法上的改进：身份漂移治理（模长/夹角实验）+ 身份资产与参考提供
  4. `数字人动作.md`（`docs-intern-motion`）— 算法上的改进：分层框架（音唇同步→表情×语言交互→手部/全身），含微调 Loss（geom/RKD）与注入点消融
  5. `CyberVerse框架.md`（`docs-intern-cyberverse`）— 数字人 Agent 框架介绍：架构、插件体系、模型接入、部署形态
  6. `工程设计.md`（`docs-intern-design`）— 工程上的改进合集：整体链路 / 贴回 / 传输与发布 / 音频链路 / 会话与资源生命周期 / 稳定性 / 未采纳设计（设计视角，非排障流水账）
  7. `数字人加速.md`（`docs-intern-acceleration`）— 只写"快"：实时性指标与延迟链、生成侧加速、系统侧加速、模型实时性横评、硬件档位与可行性、未采纳方案（原《实时性改进》独立成篇，理由与边界见 design D7）
  8. `数字人行业全景.md`（`docs-intern-industry`）— 由调研与测试成果合成：竞品与产品调研、未采纳与待复跑；选型结论与趋势判断归《总结》
  9. `总结.md`（`docs-intern-summary`）— 总览 + 量化成果总表 + 选型结论 + 趋势判断 + 发文方向（原《发文方向》与《总览》合并至此）
- 知识库 `knowledge/` 保持复制件不动；本 change 只写第一方复盘文档
- 正文不写出处：出处/素材来源/代码 commit 只记在 change 的整理环节与登记表，不进正文

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

### Modified Capabilities
（无）

## Impact
- 新增子文件夹 2 个（`数字人概述/`、`论文笔记/`）+ README；正文由单篇 change 产出
- 各文档边界、素材来源与单篇 change 对应关系见 design.md 各登记表；完成状态见 `tasks.md` 与 `论文笔记/README.md`
