---
title: CyberVerse框架
author: 汤问
date: 2026-09-20
tags: [数字人, CyberVerse, 实时框架, 插件化, WebRTC, 部署]
order: 2
summary: 为什么需要统一框架、开源框架版图、系统架构与实时性、CyberVerse 三服务与插件体系、模型接入、部署形态、我们的改造与开放问题
---

# CyberVerse框架

## 为什么需要统一框架

数字人落地的第一个障碍不是模型不够好，而是**模型太碎**：

- **接口各不相同**：Ditto、Avatar Forcing、MuseTalk、FlashHead、SoulX-LiveAct 的输入输出、依赖库、conda 环境、权重组织方式都不一样
- **链路必须完整**：一次实时对话要串起 ASR（听）→ LLM（想）→ TTS（说）→ Avatar（看），任何一环都要有流式接口
- **会话与媒体要管**：会话生命周期、音视频通道、打断与恢复、状态机，这些和模型无关，却决定了能不能真的用起来

如果每换一个模型就重搭一遍链路，所有精力都会花在胶水上。**框架的作用就是把模型变成插件**：链路、会话、媒体由框架负责，模型只实现一个固定契约。

## 现行做法

### 开源框架版图

| 项目 | 定位 | 架构形态 | 支持模型 | 实时性 | 与我们的差距 |
|------|------|---------|---------|--------|-------------|
| OpenAvatarChat | 模块化对话式数字人 | Handler Pipeline + WebRTC / coturn TURN | LiteAvatar 系 2D | 纯 CPU 可跑实时 | 以 2D 与对话为主，3D / 扩散模型未插件化 |
| LiteAvatar | 纯 CPU 实时 2D 驱动引擎 | Paraformer 特征 + ONNX 口型预测 + 轻量生成器 | 自带单一模型 | CPU 30fps | 是模型库而不是框架，无多模型抽象 |
| Ultralight-Digital-Human | 超轻量端侧数字人 | 6 通道 masked 重建 + MobileNet 风格 UNet + wenet 流式 | 自带单一模型 | 可塞进手机 | 能力范围最窄，用于端侧场景 |

**结论**：现有开源工作要么是"轻量 2D / 纯对话"，要么是"重型离线"；**实时 + 可插拔 3D 与扩散模型**是缺口。CyberVerse 的目标正是这块。

（三家信息来自二手整理，细节未见官方数据支撑，这里只作定位对照。）

### 系统架构与实时性

级联四组件：**ASR → LLM → TTS → Avatar 渲染**。三种架构形态：

| 架构 | 特点 |
|------|------|
| 级联 | 组件独立、可控、可替换，但链路各段排队，端到端延迟高 |
| 端到端 | 单模型吃完整链路，延迟低但可控性差、难替换组件 |
| 混合 | 级联框架 + 端到端局部模块 |

延迟的差距主要来自**分块等待与组件间排队**，不是单纯模型算得慢。同样的模型，放在不同编排里，用户感受到的等待可以差一个数量级。

由此形成两条工程战线：

- **传输层**：实时交互基本必选 WebRTC——自带 jitter buffer、丢包隐藏与抗弱网；WebSocket 结构简单，但平滑、抖动与丢包都要自己做
- **推理层**：流式 TTS 分块 + Avatar 异步渲染，把首帧等待摊薄；轻量技巧包括滑动窗口重叠融合、静音回退中性口型、说话与静音状态机

**实时性是系统级问题**：单点模型提速解决不了排队与分块造成的延迟，必须以框架为单位做编排。

## CyberVerse 架构

### 三服务

| 服务 | 语言 / 协议 | 端口 | 职责 |
|------|------------|------|------|
| Inference | Python / gRPC | 50051 | 一个进程内加载所有插件（ASR / LLM / TTS / Voice-LLM / Avatar） |
| Orchestrator | Go / HTTP | 8080 | 会话编排、角色配置、媒体协商；同进程还带 TURN 服务 |
| TURN | Go / TCP | 8443 | WebRTC 直连模式下的媒体中继 |
| Frontend | Vue 3 / vite | 5173 | 浏览器 UI，仅绑 `127.0.0.1`，把 `/api` 与 `/ws` 代理到 8080 |

拆成"Python 跑模型 + Go 管会话"是有意的：模型侧要什么库就给什么库，编排侧只认 gRPC 契约，两边互不污染。

### 插件体系

- **核心层** `inference/core/`：`config`（配置加载）、`registry`（插件注册与查找）、`types`（公共数据结构）
- **插件目录** `inference/plugins/`：按能力分五类——`asr`、`llm`、`tts`、`voice_llm`、`avatar`
- **服务层** `inference/services/`：把插件包成 gRPC 服务（asr / llm / tts / voice_llm / avatar / rag）
- **接口定义** `proto/`：七个 proto——`asr`、`llm`、`tts`、`voice_llm`、`avatar`、`rag`、`common`
- **配置驱动**：`cyberverse_config.yaml` 决定每个能力启用哪个插件（仓库内提供 `infra/cyberverse_config.example.yaml` 作模板，实际生效的那份不入库）

换模型不需要动链路代码：写一个插件实现对应 proto 的接口，在配置里指向它即可。

### Avatar 抽象

Avatar 是最重也最碎的一环，CyberVerse 给它单独定了契约：

- **`AvatarPlugin`**：`set_avatar`（设置形象）、`generate_stream`（吃音频流吐视频流）、`reset`、`get_fps`、`get_output_dimensions`
- **`BidirectionalAvatarPlugin`**：在基础契约上增加 `feed_user_audio` 与 `feed_user_video`，支持"能听能看"的双向会话
- **gRPC `AvatarService`**：`SetAvatar`、`GenerateStream`（`stream AudioChunk` → `stream VideoChunk`）、`FeedUserMedia`、`Reset`、`GetInfo`、**`SwitchAvatarBackend`**（后端热切换）

`GenerateStream` 是整条链路的咽喉：它把"音频流进、视频流出"固定成唯一的交互形态，模型内部的自由度全部被适配层吸收。

## 模型接入

`inference/plugins/avatar/` 下已接入四个 Avatar 插件：

| 插件 | 模型 | 我们体系中的角色 |
|------|------|-----------------|
| `avatarforcing_plugin` | Avatar Forcing | 交互头像主线之一，双向听说能力 |
| `ditto_plugin` | Ditto | 实时化主线之一，TensorRT 加速 |
| `flash_head_plugin` | FlashHead | 整帧视频生成路线对照 |
| `live_act_plugin` | SoulX-LiveAct | 双向交互对照 |

**接入契约是统一的**：输入音频流，输出 `VideoChunk` 流；形象通过 `set_avatar` 设置；帧率与输出尺寸通过 `get_fps` / `get_output_dimensions` 暴露给编排层。各模型在音频分块、采样步数、缓冲策略上的差异，都在插件内部消化——编排层看到的只有一条统一的音视频流。

各模型的算法细节与实测数据分别写在论文笔记与《数字人行业全景》，这里不展开。

## 部署形态

我们的部署方式有自己的纪律，值得写清楚：

- **远端 GPU 服务器**：模型与推理都在远端跑，本地机器没有 GPU
- **三服务全部绑 `127.0.0.1`**：因此从本地访问必须建 **SSH 隧道**（5173 前端 / 8080 编排 / 8443 TURN），三条缺一不可——前端能打开但音视频连不上，通常就是漏了 8443
- **重启只走一条路**：`scripts/restart_remote.sh`，它负责加载 `.env`（不加载会导致 API key 缺失、ASR/LLM 报 401）、等服务就绪、再校验三条隧道
- **远端工作树只部署不编辑**：`/root/CyberVerse` 是部署目标，编辑一律在本地做完再同步；这条纪律避免了远端改动被覆盖、以及"改了没生效"的假象

## 我们的改造与扩展

我们的工作集中在**实时性、稳定性、工程基建**三块（细节见《工程改进》，这里只列落点）：

- **流式与静默态**：AvatarForcing 连续流式接入；修复 Ditto 静默运行时卡死
- **实时性测量**：Ditto 与 AvatarForcing 的 RTF 及其波动曲线；RTF/延迟随运行时间的漂移测量（含 WebRTC 段）
- **延迟压缩**：全链路首响应 3.5s → 约 2.9s；开口前排空待机缓冲；段聚合粒度压到 200ms；编码链路耗时 679ms → 100ms 以内
- **编码链路**：H.264 换用 NVENC 硬编、编码器常驻、缓冲档位配置化
- **交互体验**：插话打断自然收声、打断立即止声、消除开口前的冻帧与雪花帧、修复待机呼吸音
- **画面质量**：流式漂移（头部放大）修复、输出分辨率档位与编码质量权衡、anchor guidance 移植到流式路径
- **资源回收**：会话回收验证（终止后约 30s 进入 terminal、约 35s 会话归零、idle 3 分钟卸载 avatar 后端）
- **配套基建**：管理模块迁移到本平台；共享脚手架变更同步；统一资产提取框架

## 开放问题与改进方向

- **插件显存泄漏**：会话回收本身有效，但 AvatarForcing 插件每个 load/unload 周期仍残留约 1.4GB 活跃分配——这是插件层的问题，与会话回收是两件事，需要单独立项
- **多模型并行与热切换**：`SwitchAvatarBackend` 已提供接口，但多模型同时驻留的显存与调度策略还没有答案
- **远端部署自动化**：目前依赖脚本 + 人工隧道检查，容易漏步
- **实时性的可观测性**：GPU 侧合计约 38.5ms/帧，而 25fps 的预算是 40ms——余量只有几毫秒，任何排队都会变成卡顿；这类问题需要跨端（GPU、发布端、浏览器）串起来的观测，而不是按症状猜模块
- **竞品能力补差**：轻量 2D 与端侧方案在 CPU/端侧推理上比我们更省，是否需要在"轻量档位"上补一条路线，尚未定论
