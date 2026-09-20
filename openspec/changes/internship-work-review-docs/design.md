# Design: internship-work-review-docs

## Context

- 目标读者：**自己**。用途：① 工作汇报底稿；② 为后续继续推进数字人方向的工作提供素材；③ 循实习经验提炼可发表文章的选题依据。写作取向：事实与数字优先，每个结论给证据锚（代码路径/commit/指标表），区分"已验证/待验证/已被否证"。
- 素材四源：CyberVerse（`~/code/CyberVerse` @ `4968280`）、InternWiki（已复制至 `management/docs/knowledge/`）、博客精选（已复制）、InternWiki 项目树（`projects/digital-human/tasks.json` 已复制为 knowledge/project-tasks.json）。
- 放置规则（用户明确要求）：子文件夹夹内平铺、禁止再嵌套。现有三个子文件夹：`实习复盘/`（本体系 5 篇）、`论文笔记/`（后续论文精读笔记，只建规范）、`模型介绍/`（五篇模型介绍，见下表）。

## Goals / Non-Goals

**Goals:**
- 5 篇平铺文档，讲清三项核心工作（身份一致性 / PasteBack / CyberVerse 工程改进）的：问题是什么 → 怎么定位 → 做了什么 → 效果如何 → 哪些没成
- 支撑工作汇报：量化成果总表可直取直用
- 支撑后续推进：遗留问题、未采纳方案、下一步补实验清单清晰可执行
- 产出《发文方向》：每条候选选题一张"证据资产负债表"（已有/缺失/需补的实验），可据此决定下一步

**Non-Goals:**
- 不做团队交接文档（读者是自己，不解释项目背景常识）
- 不复制/搬运 knowledge/ 已有内容，只做第一方复盘并引用
- 不写教程向内容（知识库已有）；不虚构数字，查不到的写"待补"

## 文档结构与登记表（唯一权威，均在 `management/docs/实习复盘/` 下平铺）

> 双层流程：本表每行一篇文档，各由独立单篇 change（`docs-intern-<slug>`）实施——先完成「资料整理」任务组（产物先过目），再启动「动笔写作」任务组。本总 change 只管体系与验收，不写正文。

| # | 文件 | 职责边界（只写什么/不写什么） | 依赖 | 单篇 change |
|---|------|------------------------------|------|-------------|
| 1 | `身份一致性.md` | 只写 AvatarForcing 身份漂移：现象→诊断框架→两个实验→治理方案；不写音频微调/音唇同步 | — | `docs-intern-identity` |
| 2 | `PasteBack.md` | 只写贴回合成：两条路径、接缝/波动修复、历史勘误；不写渲染管线其他环节 | — | `docs-intern-pasteback` |
| 3 | `CyberVerse工程改进.md` | 只写实时链路工程优化：瓶颈定位、音频缺口、僵尸会话、Ditto TRT、silent-avatar、未采纳；不写模型算法本身 | — | `docs-intern-cyberverse` |
| 4 | `发文方向.md` | 只写选题评估：漏斗、三候选证据资产负债表、related-work 撞车扫描、决策建议；不写实施细节 | 1–3 | `docs-intern-paper-directions` |
| 5 | `总览.md` | 只写导览与汇总：背景、三项工作互链、方法沉淀、量化成果总表（数字从 1–3 汇总，不新造证据） | 1–4 | `docs-intern-overview` |

### 1. `身份一致性.md`（结构契约）

- `## 问题`：AvatarForcing 长视频生成身份漂移现象
- `## 定位方法`：motion latent 向量分解（模长=运动量 / 方向=走向）作为诊断框架
- `## 模长实验（否证）`：300s 三段测量表，范数撑开假说不成立的证据链与边界（引《Avatar Forcing 微调实践》§3.1）
- `## 夹角实验（单身份支持）`：方向漂移假说的证据与未验证边界（§3.2）
- `## 治理方案`：参考条件化 v2（待实现状态如实标注）
- `## 汇报要点与后续推进`：一页可直取的汇报结论 + 下一步实验（多身份夹角验证、治理消融）

### 2. `PasteBack.md`（结构契约）

- `## 问题`：512×512 人脸区域 → 全帧合成的必要性；贴回接缝/波动 badcase
- `## 两条实现路径`：AF 裁剪框+alpha 渐变（`pasteback_utils.py`）vs Ditto 逐帧 M_c2o 仿射（引 CyberVerse `management/docs/paste-back-compositing.md`，含历史勘误：affine 模式属 digital_human 项目而非 CyberVerse）
- `## 接缝与波动修复`：t11-3 进行中状态、commit d32fb74（只合成落点区域）、t24 贴回冻结的四次尝试与最终否证记录
- `## 汇报要点与后续推进`：路径选型依据 + 遗留问题清单

### 3. `CyberVerse工程改进.md`（结构契约）

- `## 瓶颈定位`：隔离基准 38.5ms/帧 vs 25fps 40ms 预算的测量方法（引《CyberVerse 工程专题》§一）
- `## 音频缺口修复`：H.264 段尾等待定位 → shortfall 修复 → 绝对播放锚点，两阶段验收数据表（§二）
- `## 僵尸会话治理`：三层兜底 + AvatarForcing 插件 1.4GB 残留泄漏的发现（§三）
- `## Ditto 实时化`：TRT 七步任务（t4-1~t4-7）、RTF 3→<1→0.75 冲刺（t7 active）、perf 提交链逐条归类
- `## silent-avatar 与交互体验`：feed gate、idle breathing（t23 A/B）、lead truncation（t24 四次否证）——已采纳/未采纳分明
- `## 明确未采纳的方案`：以工程专题 §五 为准，逐条写否证原因（防止后续推进时重走弯路）

### 4. `发文方向.md`（结构契约）

- `## 选题漏斗`：从全部工作 → 有增量证据的候选 → 推荐主攻方向（附淘汰理由）
- `## 候选 A：身份漂移的诊断与治理`：研究问题（LIA 系 latent 动画长时身份漂移的成因与治理）、已有证据（模长否证/夹角单身份支持/参考条件化 v2）、差异点（用 papers 库 related-work 扫描：id-sim、face-consistency-benchmark、avatarforcing 原文等）、需补实验（多身份夹角、治理消融、指标口径）
- `## 候选 B：流式 Talking-Head 系统论文`：测量→定位→修复的完整工程证据链（音频缺口/僵尸会话/RTF）、与 wan-streamer/opens2v 等系统工作的差异、发表形态（system/benchmark track、workshop）
- `## 候选 C：PasteBack 合成质量`：接缝/波动问题的形式化、两条路径的对比基准、小而美的 workshop/短文潜力与风险（工程增量是否足够）
- `## 决策建议`：推荐优先级 + 下一步 30 天可执行的补实验清单

### 5. `总览.md`（结构契约，依赖 1–4）

- `## 实习背景与主线`：钉钉数字人方向、会议面试官数字人目标、时间轴（2026-06 至今，引 project-tasks.json 里程碑）
- `## 三项核心工作`：身份一致性 / PasteBack / CyberVerse 工程改进各一段（问题→方法→结果一句话），互链三篇
- `## 工作方法沉淀`：任务树管理、实验记录规范（t24 四次否证作为方法论案例）、[shared] 脚手架协作
- `## 量化成果总表`：RTF 3→0.9、concealment 3.6%→0.022%、15 模型 SpeedRun 等关键数字汇总表（逐项标注来源文档，不新造数字）
- `## 与发文方向的关系`：指向《发文方向》

## 模型介绍登记表（`management/docs/模型介绍/`，夹内平铺，双层流程同 D0）

五篇统一结构契约：`## 是什么`（论文/机构/年份/一句话定位，arxiv id，papers 库链接）→ `## 架构核心`（驱动信号→表示→生成→渲染链路 + 与同类差异一表）→ `## 在我们体系中的角色`（CyberVerse 插件路径 @4968280、接入状态、我们的改动/优化/否证记录）→ `## 与复盘三线的关联` → `## 参考与延伸`（knowledge/ 精读链接、papers 库条目）。不重复精读内容，以"我们怎么用的"为主视角。

| 文件 | 依赖素材 | 单篇 change |
|------|----------|-------------|
| `avatar-forcing.md` | knowledge/《Avatar Forcing 模型精读》《Motion Latent AutoEncoder》《微调实践》+ models/avatarforcing/ @4968280 | `docs-model-avatar-forcing` |
| `ditto.md` | knowledge/《Ditto 模型精读》《Ditto 实时化与 TensorRT 加速复盘》+ models/ditto/ | `docs-model-ditto` |
| `liveact.md` | papers 库 paper-liveact + models/SoulX-LiveAct/ | `docs-model-liveact` |
| `omnimate.md` | papers 库 omnimate-2026 | `docs-model-omnimate` |
| `talker-t2av.md` | knowledge/《Talker-T2AV 模型精读》《Talker-T2AV 接入与验证》 | `docs-model-talker-t2av` |

## Decisions

- **D0 双层流程**：本 change 为体系级总 change（登记表/结构契约/验收）；每篇正文由独立单篇 change 实施，其 tasks 固定为两组——「1. 资料整理」（研读来源、提取证据与数据表，产物先行）与「2. 动笔写作」，整理未完成且未经确认不得启动写作
- **D1 目录与命名**：子文件夹夹内平铺；单篇 change 命名：复盘系 `docs-intern-<slug>`、模型系 `docs-model-<slug>`（与 ProjFlow docs-system 双层流程同构）
- **D2 引用规范**：CyberVerse 引用 = 路径 + `@4968280`；知识库引用 = 相对链接 `../knowledge/xxx.md`；不引用博客线上 URL（本地已复制）
- **D3 事实分级**：每节结论显式标注【已验证】【待验证】【已否证】，与 CyberVerse 任务树进度状态对齐

## Risks / Trade-offs

- [记忆缺失导致数字空缺] → 标"待补"而非编造；优先引用已归档文档中的数字
- [CyberVerse 仍在演进（t7/t11 active）] → 锚定 commit，文档注明"截至 2026-08-04 快照"
- [发文选题误判（增量不足或撞车）] → 用 papers 库做 related-work 扫描后再下结论；候选方向标注"撞车风险"与差异点，未扫描前不定主攻

## Open Questions

（无）
