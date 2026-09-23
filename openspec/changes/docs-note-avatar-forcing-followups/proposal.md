## Why

`论文笔记/avatar-forcing.md` 的「相关工作与定位」只列了四篇**前置**工作（DIM / INFP / ARIG / 本篇），完全没有记录**后续工作**。而 Semantic Scholar 显示 Avatar Forcing（`2601.00664`）已有 **16 篇引用**（influential 4），这些引用恰好回答了一个关键问题：它那三个优点（低维运动隐变量换来的实时、块因果流式、DPO 换来的表达力）分别被谁继承、有没有做得更好。

同时我们的论文待读清单（`论文笔记/README.md` 的「现有清单」表）需要补入这次调研中价值最高的两篇：**Causal Forcing**（该篇被引最高的继承者，134 次）与 **Wan-Streamer**（实时交互基座）。

## What Changes

- 在 `management/docs/论文笔记/avatar-forcing.md` 的「相关工作与定位」中新增「后续工作」小节：按"继承哪个优点"分组的引用表，并明确**仍然空着的两点**（低维运动隐变量的显式控制接口、低维运动子空间上的偏好优化）。
- 在同一篇的「局限与启发」补一段**对照性说明**：DynaForcing 把这类"自条件反馈环导致的运动塌陷"形式化为 dynamic collapse；需写明它研究的是 DMD 蒸馏、与本篇的 diffusion forcing **不是同一设定**，因此只作机制对照、不作等价结论。
- 修正「论文信息」两处事实：arXiv 版本日期（v1 2026-01-02 / v2 2026-05-30，现写作"v2，2026-01-02"）与"代码仓库未公开"（现有 `AVTR-1` 开放栈作为替代参考）；并补一行被引数。
- 在 `management/docs/论文笔记/README.md` 的「现有清单」追加 `causal-forcing.md`、`wan-streamer.md` 两条待读条目，状态 `待写`，附 arXiv 链接与标题。
- 更新 `avatar-forcing.json` 的 `changelog`。

## Capabilities

### New Capabilities

无。纯文档更新。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 修改文档：`management/docs/论文笔记/avatar-forcing.md`、`management/docs/论文笔记/README.md`、`management/docs/论文笔记/avatar-forcing.json`。
- 依据：Semantic Scholar 的 `/paper/arXiv:2601.00664/citations`（16 篇）与 `/paper/arXiv:2603.14331/citations`（7 篇），以及对其中 6 篇的 arXiv 摘要原文核对。
- 不修改 `## 方法精析`、实验数据、配图与工程层实测结论；不新增论文笔记正文文件（待读条目只登记队列）。
