# Proposal: docs-intern-engineering（工程改进.md 单篇 change）

## Why

伞 change 登记表 #5。工程改进是实习中工作量最大、汇报价值最高的一条线：瓶颈定位、音频缺口、僵尸会话、Ditto 实时化、编码链路、PasteBack 贴回、实时性改进（t1–t25），且串起"C 位证据"（跨端时间线定位、局部变快≠用户变快、未采纳方案的负结论）。

## What Changes

- 整理证据与数据表（瓶颈基线、音频缺口前后对照、会话回收时间线、TRT 模块级事实、编码链路耗时、贴回 p95/RTF/TTFF、t1–t25 归类），在对话中提交审核，不写入仓库
- 经确认后写正文 `management/docs/实习复盘/工程改进.md`
- **边界**：本篇写"我们改了什么、怎么定位、结论"；系统架构与实时性通论归《CyberVerse框架》；模型算法与动作/身份侧归《数字人动作》《数字人身份》

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

## Impact
- 新增正文 1 个 md；不改代码
- 来源：knowledge/《CyberVerse 工程专题》《Ditto 实时化与 TensorRT 加速复盘》《Ditto 改动实践》《视频生成训练与推理加速专题》、CyberVerse `management/projects/cyberverse/tasks.json`（t1–t25，核对基准 @4968280）
