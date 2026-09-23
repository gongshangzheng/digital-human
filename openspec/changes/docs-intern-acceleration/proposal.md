# Proposal: docs-intern-acceleration（数字人加速.md 单篇 change）

## Why

伞 change 登记表 #6（本次新增）。实时性此前被拆在三篇里（《CyberVerse框架》通论、《工程设计》我们的改进、《数字人行业全景》指标与横评），读者要跳三篇才能追完；而且"**视频推理加速**"这一层（模型侧的量化 / 稀疏 / 步数蒸馏 / 缓存 / 并行）此前完全没有归宿。本篇把"**快**"这条线集中成一篇：从指标口径与延迟链，到模型侧与系统侧两条加速路径，再到横评、硬件档位与未采纳方案。

## What Changes

- 新建正文 `management/docs/数字人概述/数字人加速.md`
- 从《数字人行业全景》迁入：实时性三个指标与延迟链、生成侧加速、模型实时性横评、硬件档位与可行性（**原篇同步删除并留链接**）
- 从《工程设计》迁入：实时链路瓶颈基线、Ditto 实时化、编码与传输链路、首帧与开口（**原篇保留"稳与对"的部分**：音频缺口、僵尸会话、会话与内存、PasteBack、体验类缺陷）
- 整理证据并在对话中提交审核（不写入仓库），审核通过后动笔

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

## Impact
- 新增正文 1 个 md；另需修改《工程设计》《数字人行业全景》两篇正文（搬迁，属内容级调整）
- 来源：knowledge/《视频生成训练与推理加速专题》《digital-human-realtime-gpu-comparison》《digital-human-engineering-benchmark》《hardware-assessment》《CyberVerse 工程专题》《Ditto 实时化与 TensorRT 加速复盘》、博客成稿 `video-gen-acceleration`、CyberVerse `tasks.json`（首帧与开口 t15/t16/t20/t25）
- 待补：15+ 模型第一手 SpeedRun / Formal Eval 数据（本机未找到）
