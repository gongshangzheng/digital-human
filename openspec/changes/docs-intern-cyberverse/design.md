# Design: docs-intern-cyberverse（含待审核大纲）

## Context

- 伞 change 登记表 #2；统一骨架（为什么重要 → 现行做法 → 我们的工作 → 改进方向）。
- 目标读者：**自己**（回顾 + 后续框架层推进 + 发文素材）。
- 依赖 #1《数字人介绍与技术路线》；被《工程改进》《数字人行业全景》《总结》引用。
- 定位：**框架介绍**（系统视角）；单个模型算法细节留给论文笔记五篇。
- 正文目标路径：`management/docs/实习复盘/CyberVerse框架.md`

## Goals / Non-Goals

**Goals：** 说清"为什么需要统一框架、现有哪些框架、CyberVerse 长什么样（架构/插件/模型/部署）、我们改了哪里、还能往哪走"。
**Non-Goals：** 不写模型算法（链论文笔记）；不重复《工程改进》优化细节（只列落点+链接）；不写部署教程。

---

## 【待审核】正文大纲（到二级标题）

### 一、`## 为什么需要统一框架`
- 表达内容：模型碎片化（每个 avatar 模型接口/依赖/env 各不同）；实时 Agent 需要 ASR/LLM/TTS/Avatar 全链路编排；会话/媒体/记忆需要统一管理
- 论证/结论：没有统一框架，每换一个模型就要重搭一遍链路
- 素材：CyberVerse README 功能特性、`models/` 五模型接口差异

### 二、`## 现行做法（框架版图）`
- 表达内容：开源框架对照——OpenAvatarChat（模块化对话式）、LiteAvatar（轻量 2D 数字人）、Ultralight（源码阅读类）；各自架构与取舍
- 论证/结论：现有框架多在"轻量 2D / 纯对话"或"重型离线"，实时 + 可插拔 3D/扩散模型是缺口
- 素材：knowledge/《open-avatar-chat-liteavatar》《lite-avatar-source-code-analysis》《ultralight-digital-human-source-read》《cyberverse-realtime-digital-human-agent》
- 注意：竞品信息来自博客笔记（二手），**正文里用自然语言说明其性质**，不标出处、不写成定论

### 三、`## CyberVerse 架构`
- `### 三服务`：Python inference gRPC :50051（进程内跑所有插件）/ Go orchestrator :8080 + TURN :8443 / Vue 前端 :5173；附架构图
- `### 插件体系`：`inference/core`（config/registry/types）+ `inference/plugins/{asr,llm,tts,voice_llm,avatar}` + `proto/*.proto` 七个 gRPC 接口；配置驱动（`cyberverse_config.yaml` + `/settings` UI）
- `### Avatar 抽象`：`AvatarPlugin`（set_avatar/generate_stream/reset/get_fps/get_output_dimensions）与 `BidirectionalAvatarPlugin`（feed_user_audio/video，支持双向听说）
- `### Agent 与记忆`：PersonaAgent 前台 + SubAgent 后台异步；角色记忆持久化 + RAG
- 论证/结论：插件化 + gRPC 边界是"可插拔"的实现基础
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

## 【待审核】决策点

1. 竞品框架写多细？(A) 只做一表对照 + 结论【建议】 / (B) 每家一小节展开 / (C) 删除该节，只写"为什么需要框架"
2. 第三节 `### Agent 与记忆` 是否保留（PersonaAgent/SubAgent/RAG 与框架介绍关系偏松）

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
