# Design: docs-intern-cyberverse

## Context

- 伞 change 登记表 #2（结构契约见其 design）；统一写作骨架（为什么重要 → 现行做法 → 我们的工作 → 改进方向）。
- 依赖 #1《数字人介绍与技术路线》；被《工程改进》《数字人行业全景》《总结》引用。
- 定位：**框架介绍**（系统视角）；单个模型的算法细节留给论文笔记五篇，不在此展开。

## Goals / Non-Goals

**Goals:**
- 整理产物：架构图（三服务 + 插件体系 + 媒体链路）、插件与模型清单、端口与部署纪律、我们改造点清单（链工程改进任务号）
- 正文：能让读者（自己）快速重建"CyberVerse 长什么样、我们的改动落在哪"

**Non-Goals:**
- 不写模型算法（链论文笔记）
- 不重复《工程改进》的优化细节（只列落点、链过去）
- 不写部署教程（README 已有）

## 整理清单（动笔前必须完成）

| 来源 | 提取物 |
|------|--------|
| CyberVerse README.zh-CN.md | 定位、功能特性（实时语音/WebRTC/PersonaAgent+SubAgent/记忆 RAG/可选 avatar/插件化）、前置条件与三终端启动 |
| CyberVerse AGENTS.md | 三服务端口表（50051/8080/8443/5173）、远程 GPU 部署与 SSH 隧道、本地编辑/远端部署纪律 |
| `inference/` 结构 @4968280 | core（config/registry/types）、plugins（asr/llm/tts/voice_llm/avatar + base）、services、rag、generated（gRPC stubs） |
| `server/internal/` @4968280 | orchestrator / mediapeer / ws / inference / character / rag / agenttask / livekit / direct / recording / management 各模块职责 |
| `proto/*.proto` | 七个 gRPC 接口（asr/avatar/common/llm/rag/tts/voice_llm） |
| `models/` @4968280 | 五模型接入形态（avatarforcing/ditto/flash_head/MuseTalk/SoulX-LiveAct），插件路径 inference/plugins/avatar/* |
| Avatar 抽象 | AvatarPlugin / BidirectionalAvatarPlugin 接口方法（set_avatar/generate_stream/reset/get_fps/feed_user_*） |
| knowledge/《cyberverse-realtime-digital-human-agent》 | 博客视角的系统架构叙述（可对勘代码） |
| knowledge/《open-avatar-chat-liteavatar》《lite-avatar-source-code-analysis》《ultralight-digital-human-source-read》 | 竞品框架（OpenAvatarChat/LiteAvatar/Ultralight）架构与取舍，用于"现行做法" |
| management/projects/cyberverse/tasks.json | t1–t25 改造任务 → "我们的改造"素材（含 t3 管理模块迁移、t10 [shared]） |

## Decisions

- **D1 架构描述以代码为准**：README 是面向用户的，正文架构部分以 @4968280 的目录/接口为准确认
- **D2 竞品对勘**：竞品框架信息来自博客笔记（二手），标注来源与时间，不写成定论
- **D3 整理产物放 change 目录**，正文写完后作为附件保留

## Risks / Trade-offs

- [框架仍在演进（t7/t11 active）] → 锚定 @4968280，标注快照时间
- [竞品笔记可能过时] → 引用时写明来源与日期，标【待验证】而非【已验证】

## Open Questions

（无）
