# Design: docs-intern-cyberverse（含待审核大纲）

## Context

- 伞 change 登记表 #2；统一骨架（为什么重要 → 现行做法 → 我们的工作 → 改进方向）。
- 目标读者：**自己**（回顾 + 后续框架层推进 + 发文素材）。
- 依赖 #1《数字人介绍与技术路线》；被《工程改进》《数字人行业全景》《总结》引用。
- 定位：**框架介绍**（系统视角）；单个模型算法细节留给论文笔记五篇。**系统架构与实时性只在本篇讨论**（《数字人介绍与技术路线》是原理/路线入门篇，不写系统形态）。
- 正文目标路径：`management/docs/实习复盘/CyberVerse框架.md`

## Goals / Non-Goals

**Goals：** 说清"为什么需要统一框架、现有哪些框架、CyberVerse 长什么样（架构/插件/模型/部署）、我们改了哪里、还能往哪走"。
**Non-Goals：** 不写模型算法（链论文笔记）；不重复《工程改进》优化细节（只列落点+链接）；不写部署教程。

---

## 【待审核】正文大纲（到二级标题）

### 一、`## 为什么需要统一框架`
- 表达内容：模型碎片化（每个 avatar 模型接口/依赖/env 各不同）；实时 Agent 需要 ASR/LLM/TTS/Avatar 全链路编排；会话与媒体需要统一管理
- 论证/结论：没有统一框架，每换一个模型就要重搭一遍链路
- 素材：CyberVerse README 功能特性、`models/` 五模型接口差异

### 二、`## 现行做法`

#### 2.1 `### 开源框架版图`
- 表达内容:**一表对照 + 结论**（不逐家展开）——OpenAvatarChat（模块化对话式）、LiteAvatar（轻量 2D 数字人）、Ultralight（源码阅读类）；表列：定位 / 架构形态 / 支持模型 / 实时性 / 与我们的差距
- 论证/结论：现有框架多在"轻量 2D / 纯对话"或"重型离线"，实时 + 可插拔 3D/扩散模型是缺口
- **必须附一次对话的 mermaid `sequenceDiagram`**（用户 → 前端 → Go 编排 → Python 推理：ASR → LLM → TTS → Avatar 逐段产出），把"分块等待与排队"画在图上
- 素材：knowledge/《open-avatar-chat-liteavatar》《lite-avatar-source-code-analysis》《ultralight-digital-human-source-read》《cyberverse-realtime-digital-human-agent》
- 注意：竞品信息来自博客笔记（二手），**正文里用自然语言说明其性质**，不标出处、不写成定论

#### 2.2 `### 系统架构与实时性`（自《数字人介绍与技术路线》迁入，**只在本文讨论**）
- 表达内容：
  - **级联四组件**：ASR → LLM → TTS → Avatar 渲染
  - **三种架构对照**：级联（组件独立可控，流式链路约 3.2s）/ 端到端（单模型吃完整链路，A2-LLM TTFA 535ms）/ 混合（级联框架 + 端到端局部模块）
  - **结论**：延迟主要来自**分块等待与组件间排队**，不是单纯模型算得慢
  - **两条工程战线**：传输层（WebRTC 自带 jitter buffer、NetEQ 丢包隐藏、抗弱网；WebSocket 简单但平滑要自己做）与推理层（流式 TTS 分块 + Avatar 异步渲染；滑动窗口重叠融合、静音回退中性口型、说话/静音状态机）
  - **系统之上的 Agent 能力**：RAG 检索、工具调用、记忆人格（接 2.3 或第三章的角色记忆）
- 论证/结论：**实时性是系统级问题**——单点模型提速不能解决排队与分块造成的延迟，必须以框架为单位编排
- 与《工程改进》的边界：《工程改进》写我们针对延迟/稳定性做的具体优化（编码链路、会话回收等），本节只写通用架构与判定口径
- 素材：knowledge/《数字人基础》《5分钟认识数字人》《cyberverse-realtime-digital-human-agent》、CyberVerse README 的链路说明

### 三、`## CyberVerse 架构`
- `### 三服务`：Python inference gRPC :50051（进程内跑所有插件）/ Go orchestrator :8080 + TURN :8443 / Vue 前端 :5173；**必须附 mermaid `flowchart` 架构图**——画浏览器 / 服务器边界，标出三条链路（`/api`、`/ws` 代理，WebRTC 媒体，gRPC）
- `### 插件体系`：`inference/core`（config/registry/types）+ `inference/plugins/{asr,llm,tts,voice_llm,avatar}` + `proto/*.proto` 七个 gRPC 接口；配置驱动（`cyberverse_config.yaml` + `/settings` UI）
- `### Avatar 抽象`：`AvatarPlugin`（set_avatar/generate_stream/reset/get_fps/get_output_dimensions）与 `BidirectionalAvatarPlugin`（feed_user_audio/video，支持双向听说）；gRPC `AvatarService` 含 `SwitchAvatarBackend`（后端热切换）
- 论证/结论：插件化 + gRPC 边界是"可插拔"的实现基础
- **不含** `### Agent 与记忆`（PersonaAgent/SubAgent/RAG）：与框架骨架关系偏松，用户决定不写
- 素材：@4968280 `inference/`、`server/internal/`、`proto/`

### 四、`## 模型接入`
- 表达内容：五模型（AvatarForcing / Ditto / FlashHead / MuseTalk / SoulX-LiveAct）接入形态与插件路径（`inference/plugins/avatar/*.py`）；接入契约（输入音频流 / 输出 VideoChunk）
- 论证/结论：统一契约让模型可替换；各模型的差异被适配层吸收
- 引用：链论文笔记五篇深读

### 五、`## 部署形态`
- 表达内容：远程 GPU 服务器运行（本地无 GPU）；三服务绑定 127.0.0.1 + SSH 隧道（5173/8080/8443）；"本地只编辑、远端只部署"的纪律（引 AGENTS.md）；`.env` 必须先加载
- 论证/结论：这种纪律避免了远端工作树污染与密钥缺失类故障
- 素材：AGENTS.md

### 六、`## 我们的改造与扩展`
- 表达内容：按主题列落点（链《工程改进》）：silent-avatar 静默态、编码链路常驻 NVENC、会话回收；管理模块迁移（t3）；[shared] 脚手架协作（t10）；资产提取框架（t9）
- 论证/结论：改造集中在"实时性 + 稳定性 + 工程基建"三块
- 引用：链《工程改进》，不在此展开细节

### 七、`## 开放问题与改进方向`
- 表达内容：插件内存泄漏（AvatarForcing 每 load/unload 约 1.4GB 残留）；多模型并行/热切换；远端部署自动化；竞品框架能力补差
- 论证/结论：框架层下一阶段重点是资源回收与多模型共存

---

## 决策点（已定）

1. 竞品框架写多细 → **(A) 一表对照 + 结论**（不逐家展开）
2. 第三节 `### Agent 与记忆` → **删除**（PersonaAgent/SubAgent/RAG 不写进本文）

## 整理清单（动笔前必须完成）

| 来源 | 提取物 | 状态 |
|------|--------|------|
| README.zh-CN + AGENTS.md | 定位/特性/端口表/部署纪律 | ✅ 待整理成文 |
| `inference/`、`server/internal/`、`proto/` @4968280 | 插件体系、编排模块、gRPC 接口 | ✅ 待整理成文 |
| `models/` + avatar 插件 | 五模型接入形态 | ✅ 待整理成文 |
| knowledge/ 竞品三篇 + cyberverse-realtime | 框架版图对勘 | ✅ 待整理成文 |
| management/projects/cyberverse/tasks.json | t1–t25 改造归类 | ✅ 待整理成文 |

> 说明：以上素材已具备，但按闸门需先审本大纲；通过后在对话中提交整理结果供审核（不写入仓库），再动笔。

## Decisions

- **D1 架构以代码为准**：README 面向用户，架构部分以 @4968280 目录/接口确认
- **D2 竞品对勘用自然语言说明性质**：竞品信息来自博客笔记，正文不标出处，只说明"这是二手整理"；出处保留在本 change 的整理清单里
- **D3 只有正文进仓库**：素材在对话中审核；正文进 `management/docs/实习复盘/CyberVerse框架.md`

## Risks / Trade-offs

- [框架演进（t7/t11 active）] → 锚定 @4968280，标注快照时间
- [与《工程改进》重复] → 只列改造落点，细节链过去

## Open Questions

见"决策点"1、2。
