---
title: 数字人
slug: digital-human
status: active
startDate: 2026-06-01
endDate: null
category: work
tags:
  - 数字人
  - 生成式AI
  - 实时推理
summary: 钉钉数字人方向。当前目标为会议面试官数字人，围绕实时数字人、音视频交互与生成式模型落地，参与算法方案调研、工程实现和效果优化。已完成 20+ 篇技术调研、评测框架设计与实现（含 speed run 快速验证、agent skill 封装），当前推进评测框架优化与模型部署测试。
timeline:
  - date: 2026-06-01
    title: 入职钉钉
    type: milestone
    description: 第一天入职，数字人方向实习生，完成环境配置与团队对接。
  - date: 2026-06-08
    title: 技术方案调研启动
    type: progress
    description: 开始调研实时数字人主流方案，覆盖 2D talking-head、3D Gaussian Splatting 头像、扩散式生成三条路线。
  - date: 2026-06-22
    title: 调研阶段完成
    type: milestone
    description: 完成技术选型报告，确定以 GAGAvatar / UIKA 系前馈式方案为主要探索方向。
  - date: 2026-06-22
    title: 评测框架设计与实现
    type: milestone
    description: 完成评测框架设计文档，11 步实现脚手架、核心接口、指标、Pipeline、CLI、HTML 报告，177 项单元测试通过。
  - date: 2026-06-24
    title: FlashHead 接入与推理管线
    type: progress
    description: 接入 FlashHead 适配器，TalkVid 数据格式适配，推理输出重构，GT 标准化。
  - date: 2026-07-06
    title: 当前任务梳理
    type: progress
    description: 整理出五大并行任务方向：卡通数字人、数字人产品调研、评测框架优化、模型部署测试、conversation 评测数据集制作。
  - date: 2026-07-09
    title: 评测框架能力扩展 + FlexAvatar 接入
    type: progress
    description: 新增 speed run 快速验证线路，支持端到端跑通并主观检验效果；将评测功能封装为 agent skill，便于快速调用；端到端跑通评测代码全流程，验证各环节可用；修复模型参数覆盖问题并重新下载。基于 UV 实现基准环境 + 微调环境双层管理策略。接入 FlexAvatar（CVPR 2026）模型适配器，支持 pixel3dmm 和 artalk 两种驱动模式；调研 FlexAvatar / HyperGaussians / MATCH / AniGS 四个 3DGS 方法。
  - date: 2026-07-13
    title: 下周重点：竞品调研 + 选型确认
    type: progress
    description: 启动主流数字人产品调研（实现原理/效果/实时通话/延迟），同步推进选型方案确认，要求自研方案在主观表现和客观指标上不低于竞品。
---

## 项目背景

钉钉 · 数字人方向（2026.06 — 至今）。

### 目标

**会议面试官数字人**：打造一个能够在视频会议场景中担任面试官角色的数字人，具备实时对话、表情/唇形同步、自然交互等能力。

该目标有可能进一步拓展至更多数字人应用场景（如客服、培训、演讲等），具体方向待团队讨论确定。

## 技术栈

- 生成式 AI：扩散模型、3D Gaussian Splatting、NeRF
- 音视频：实时推理 pipeline、流式生成
- 工程：PyTorch、ONNX/TensorRT、C++

## 已完成工作

### 1. 技术调研（20+ 篇系列文章）

完成数字人技术全景调研，覆盖 **6 条主流路线**，产出系列文章 20+ 篇：

| 路线 | 代表工作 | 文章 |
|------|---------|------|
| 换嘴与视频配音 | Wav2Lip、MuseTalk | 系列（二） |
| 运动空间 | SadTalker、VASA-1、Ditto | 系列（三） |
| 3DGS / NeRF Avatar | GAGAvatar、UIKA | 系列（四） |
| 扩散基模与整帧 | FlashHead、LivePortrait | 系列（五） |
| 整帧与全身生成 | OmniAvatar、LongCat-Video-Avatar | 系列（六） |
| 实时流式与蒸馏 | LiveAvatar、Self-Forcing | 系列（七） |

另有：
- **Avatar 类型总报告**（系列八）
- **评测指标 / 数据集 / 算力 Benchmark**（系列九）—— 5 大指标族深度拆解、28 个模型输入输出规格
- **产业图谱**（系列十）
- **Demo Gallery**（系列十一）
- **实时性全景对比**（系列十二）—— GPU 需求到交互延迟
- **卡通与风格化数字人**（系列十三）—— 跨域卡通重演、风格化共语音生成、细粒度表情数据集、3D 动画质量评估与 RGB 驱动肖像动画，含 ToonTalker / Co-Speech NPR / GenEAva / 4DHumanQA / CapTalk / X-Portrait 等 6 篇论文精读
- **工程解读**：CyberVerse 实时数字人 Agent、FlashHead Lite 实验、Ultralight-Digital-Human 源码解读、推理 Benchmark 汇总

### 2. 评测框架（~/code/digital_human）

从零设计并实现了一套**数字人模型验证框架**，59 次 commit，177 项单元测试通过。

**框架架构**：
```
src/
├── cli.py                    # CLI 命令行入口
├── datasets/                 # 数据集适配器（base/talkvid/conversation/long）
├── defs/                     # 核心类型、接口定义、注册表
├── logics/                   # 观察层（漂移检测、效率分析、延迟拆解、压测）
├── metrics/                  # 指标实现
│   ├── quality/              #   PSNR、SSIM、LPIPS、TOPIQ-FR
│   ├── identity/             #   CSIM（余弦相似度）
│   ├── lip_sync/             #   SyncNet（Sync-C、Sync-D）
│   ├── drift/                #   Dino-S、CSIM 漂移、LPIPS 漂移
│   └── efficiency/           #   FPS、延迟、显存、GPU 利用率、吞吐量
├── models/                   # 模型适配器（flash_head/mock/_template）
├── pipeline/                 # 编排（推理、压力测试、轨道管理）
├── renderers/                # 视频标准化器
└── reporting/                # HTML 报告生成 + 聚合器
```

**已实现指标**：
| 类别 | 指标 |
|------|------|
| 画质 | PSNR、SSIM、LPIPS、TOPIQ-FR（有参/无参） |
| 身份保持 | CSIM（Cosine Similarity） |
| 唇同步 | SyncNet（Sync-C / Sync-D） |
| 长时漂移 | Dino-S、CSIM Drift、LPIPS Drift |
| 效率 | FPS、Latency、VRAM、GPU Util、Throughput、Max Concurrent、RTF |

**模型适配器**：
- FlashHead（已接入）
- FlexAvatar（已接入，CVPR 2026，单图→完整 3D 头部 Avatar）
- Mock（用于测试）
- Template（供新模型参考）

**数据集适配器**：
- TalkVid、Conversation、Long、Base

**Speed Run 模式**：
- 快速跑通全流程，获取输出结果用于主观效果检验
- 不追求指标精度，重点加速迭代调试

**Agent Skill 封装**：
- 将部分评测功能封装为 skill，agents 可快速调用评测模型

**UV 环境管理**：
- 基准环境（`.venv`）：通过 `pyproject.toml` + `uv.lock` 管理，覆盖大多数模型
- 微调环境（`.envs/{model}`）：依赖冲突的模型创建增量环境，UV 全局缓存通过 hardlink 共享包
- 四步决策流程：基准测试 → 调整基准 → git 回退 → 创建微调
- subprocess wrapper 按优先级解析：`venv_path` > `conda_env` > venv 回退

## 当前任务

### 1. 卡通数字人

- [ ] 相关算法调研与实现
- [ ] 主观测试（人眼感知质量评估）
- [ ] 客观指标测试（PSNR、SSIM、LPIPS 等）

### 2. 数字人产品调研

- [ ] 数字人后端 Agent 的设计理念调研
- [ ] 主流数字人产品实现原理调研：调研 HeyGen、D-ID、Synthesia、硅基智能、腾讯智影、阿里通义等产品的技术路线（2D整图生成/换唇/3D数字人模型）
- [ ] 竞品效果与实时通话能力评估：主观效果（画质/唇同步/表情自然度）、是否支持实时通话、端到端延迟，输出竞品对比表

### 2b. 数字人选型方案确认

- [ ] 自研方案与竞品效果对标：将 FlashHead/FlexAvatar 等自研模型与竞品在主观效果和客观指标上对标
- [ ] 选型决策报告：综合调研和对标数据，输出方案对比矩阵、推荐结论、A10部署可行性和风险分析

### 3. 评测框架优化

- [x] 新增 speed run 线路：快速跑通项目并获取输出结果，进行主观效果检验
- [x] 评测功能封装为 agent skill，便于快速调用
- [x] 跑通评测代码全流程：端到端跑通评测代码的完整流程，验证各环节可用
- [x] 模型参数重新下载：修复误覆盖的模型参数，恢复正常使用
- [x] UV 环境管理机制：基准环境 + 微调环境双层策略，env-manager skill + 四步决策流程 + 依赖冲突分析
- [ ] 人脸 matting 前置处理：PSNR 等指标需先做人脸 matting 再测，否则对 3DGS 等无背景算法不公平
- [ ] Wave2Lip 唇同步指标异常排查：之前测试 Wave2Lip 唇同步分数最高，结果可疑，需复验
- [ ] 无参视频质量评测模型调研：除 TOPIQ 外，调研更多无参考（no-reference）视频质量评测模型，补充 TOPIQ-FR 等有参方案的对照
- [ ] 优化后输出一版当前所有模型的评测结果

### 4. 近实时/非实时数字人模型部署与测试

- [ ] 近实时模型部署与效果测试
- [ ] 非实时模型部署与效果测试

### 5. Conversation 评测数据集制作

- [ ] 设计对话场景与评测维度
- [ ] 数据集采集与标注
