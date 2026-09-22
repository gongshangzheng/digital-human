## Why

`论文笔记/avatar-forcing.md` 用 DPO 概括其表达力微调，却没有解释偏好优化的基本机制、扩散模型中目标如何落地，或该论文为何能在没有人工偏好标签的条件下构造运动隐变量偏好对。项目 wiki 中也没有一篇可复用的 DPO 说明，其他文档遇到同一术语时无处可链。

## What Changes

- 在 `management/docs/` 新增一个技术介绍子文件夹，放置一篇**通用** DPO 技术介绍：从 RLHF / InstructGPT 背景讲到通用 DPO 目标、免奖励模型的推导直觉与适用边界，再介绍 DPO 在扩散模型上的通用扩展（DiffusionDPO），并以简短的延展阅读标记 IPO、KTO、ORPO、SimPO 所处理的问题。该篇不写任何具体论文的应用细节。
- 为技术介绍添加文档页所需的 frontmatter、阅读顺序和相关文档元数据，使其可作为可链接的知识节点。
- 扩写 `论文笔记/avatar-forcing.md` 中该论文专属的 DPO 内容：两阶段训练与 `v_ref`、偏好判别来源（含“丢弃用户条件”发生在何处）、逐帧向量场比较、`L_ft` 联合目标、配置，以及消融中的收益与 CSIM / LSE-C 小幅取舍；通用 DPO 推导改为链接到技术介绍，不在两篇中重复。


## Capabilities

### New Capabilities

无。本变更仅新增和重组说明性文档，不改变产品或接口行为。

### Modified Capabilities

无。

## Impact

- 新增 `management/docs/技术介绍/` 下的 DPO 说明文档及同名 sidecar JSON。
- 修改 `management/docs/论文笔记/avatar-forcing.md` 的 DPO 相关措辞和跨文档链接，可能同步更新其 sidecar 的相关文档条目。
- 不修改前后端代码、API、依赖或既有 OpenSpec 产品规格。
