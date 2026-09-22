# Proposal: docs-intern-industry（数字人行业全景.md 单篇 change）

## Why

伞 change 登记表 #6。这一篇是**市场与实测视角**：模型实时性横评、硬件可行性、竞品与产品调研、选型结论、趋势判断。它与《数字人介绍与技术路线》分工——那边写原理与流派（教科书视角），这边写"我们测过什么、市场在做什么、我们为什么选它"。

## What Changes

- 整理证据：30+ 模型实时性对比（区分论文披露 / 仓库 / 我们实测三类来源）、硬件层级结论、竞品与产品调研要点、选型依据、未采纳与待复跑清单、趋势判断素材
- **第一手 15+ 模型 SpeedRun / Formal Eval 横评数据目前在仓库中缺失**（本仓库 `results/` 为空）；需确认数据位置后补入，否则该节按"待补"处理，不编数字
- 经确认后写正文 `management/docs/实习复盘/数字人行业全景.md`

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

## Impact
- 新增正文 1 个 md；不改代码
- 来源：knowledge/《digital-human-realtime-gpu-comparison》《digital-human-engineering-benchmark》《hardware-assessment》《voice-ai-digital-human-landscape》《模型探索与未采纳实验复盘》《digital-human-backend-agent-design》、papers 库（117 篇）+ 博客 arxiv-digest 时间线
- 待补：digital_human 平台的 SpeedRun / Formal Eval 原始结果（本机未找到）
