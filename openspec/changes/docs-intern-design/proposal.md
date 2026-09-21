# Proposal: docs-intern-design（工程设计.md 单篇 change）

## Why

伞 change 登记表 #5（本篇由《工程改进》重构为《工程设计》）。工程是实习中工作量最大的一条线，但此前的写法是"排障流水账"。本篇改为**按设计叙事**：整体链路怎么划分、贴回与传输管线怎么引入、音频链路与会话生命周期怎么设计、稳定性怎么保证——用演进过程（三轮贴回、4 版推翻）作证据，而不是主线。

## What Changes

- 整理证据与数据表（瓶颈基线、音频缺口前后对照、会话回收时间线、TRT 模块级事实、编码链路耗时、贴回 p95/RTF/TTFF、t1–t25 归类），在对话中提交审核，不写入仓库
- 经确认后写正文 `management/docs/实习复盘/工程设计.md`
- **边界**：本篇写"我们的工程怎么设计的"；速度与吞吐归《数字人加速》；架构与实时性通论归《CyberVerse框架》；模型算法与动作/身份侧归《数字人动作》《数字人身份》

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

## Impact
- 新增正文 1 个 md；不改代码
- 来源：knowledge/《CyberVerse 工程专题》《Ditto 实时化与 TensorRT 加速复盘》《Ditto 改动实践》《视频生成训练与推理加速专题》、CyberVerse `management/projects/cyberverse/tasks.json`（t1–t25，核对基准 @4968280）
