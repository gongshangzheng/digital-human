---
title: 知识库
author: 汤问
date: 2026-09-20
tags: [digital-human, knowledge]
summary: 从外部信息源复制的数字人知识库索引：52 篇单层平铺的专题与精读，附来源与外部代码源登记。
---

# 知识库（复制自外部信息源）

> 单层平铺，不嵌套。现共 52 个文件（InternWiki 复制 29 + 博客精选 22 + 本索引）。外部源登记见下方「来源」与「外部代码源」两节。
> 复制即声明本仓库为演进主体，上游冻结为历史源。

## 来源

| 前缀/特征 | 来源 | 快照 |
|-----------|------|------|
| 中文文件名（专题/精读/5分钟/工程等） | InternWiki `apps/web/content/interns/tangwen/docs/` 及 `projects/digital-human/`（tangwen，26 篇 + junjiawang voice-agent 系列 7 篇） | commit `91b683b`，2026-09-20 复制 |
| 英文 slug 文件名 | 博客 `src/pages/*.html` 精选 22 篇（survey/工程/框架竞品），html2text 转换，脚本 `scripts/copy_blog_knowledge.py` | commit `3e7da698`，2026-09-20 转换 |

## InternWiki（tangwen / junjiawang）

数字人基础 · 动作空间专题 · 数字人渲染器专题 · 5 分钟系列 ×4 ·
Avatar Forcing 模型精读 · Avatar Forcing Motion Latent AutoEncoder · Ditto 模型精读 · Talker-T2AV 模型精读 ·
CyberVerse 工程专题 · Ditto 实时化与 TensorRT 加速复盘 · 音画同步专题 · 数据集整理专题 · 评测指标专题 · 视频生成训练与推理加速专题 · 模型探索与未采纳实验复盘 · Talker-T2AV 接入与验证 ·
Ditto 改动实践 · Avatar Forcing 微调实践 · 微调策略专题 ·
3dgs-methods-research · hardware-assessment · project-README · project-tasks.json ·
junjiawang：voice-agent-web 系列 7 篇（架构/数字人/MCP-RAG/会话生命周期/鉴权/契约/badcase）

## 博客精选

digital-human-survey-map · digital-human-avatar-survey · realtime-digital-human-survey · gfvc-survey-2023 ·
digital-human-engineering-benchmark · digital-human-training-inference-benchmark · digital-human-realtime-gpu-comparison ·
digital-human-streaming-distillation · digital-human-identity-consistency ·
cyberverse-realtime-digital-human-agent · cyberverse-flashhead-lite-experiment ·
realtime-communication 系列 5 篇 · tool-augmented-digital-human · voice-ai-digital-human-landscape

（论文单篇精读不入知识库——已在 papers 库索引，带 blog_url）

## 外部代码源（未复制，独立 clone 锚定）

> 只登记与锚定，不 vendoring 代码。锚定 commit 保证外部源演进后引用仍可复现（`git -C <本机路径> show <hash>:<path>`）。

| 源 | 远端 | 本机路径 | 用途 | 引入方式 | 锚定 commit |
|----|------|----------|------|----------|-------------|
| CyberVerse | github.com/gongshangzheng/CyberVerse | `~/code/CyberVerse` | 实时数字人 Agent 框架优化 fork（avatarforcing / ditto / flash_head / MuseTalk / SoulX-LiveAct 模型插件、流式管线、设计文档） | 独立 clone | `4968280b109aa2e31d463bc7cfae1959d3dfa215`（2026-08-04） |
| ProjFlow | —（本地上游脚手架） | `~/code/ProjFlow` | 共享脚手架上游：management / papers / evaluation 三模块 + FastAPI + Vue3 | rsync 派生（本仓库即下游） | 拷贝时工作树快照 |

### CyberVerse 被索引的关键路径（锚定 `4968280`）

- `models/avatarforcing/`、`models/ditto/`、`models/flash_head/`、`models/MuseTalk/`、`models/SoulX-LiveAct/`
- `management/docs/`：avatarforcing-design、ditto-design、streaming-pipeline、paste-back-compositing、silent-avatar-feed-gate、avatar-rtf-latency-over-time
- `management/projects/digital-human/`：dh-eval 评测框架任务树
