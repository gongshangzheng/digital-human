## Why

Causal Forcing 是自查 `Avatar Forcing`（`2601.00664`）被引列表时发现的**最高被引后续工作**（Semantic Scholar：`2602.02214` 被引 134），已登记进 `论文笔记/README.md` 的待读清单。它值得先读的理由是它在**理论层面**改写了我们既有的流式认知：

- 它指出把预训练**双向**视频扩散蒸馏成 **few-step 自回归**学生时，除"少步采样"之外还有一个 **architectural gap**（全注意力 → 因果注意力），而现有 SOTA（Self Forcing）的 ODE 初始化**在理论上就错**：MSE 回归式 ODE 蒸馏要求配对数据单射，双向教师只在 **video level** 单射、不满足 AR 学生需要的 **frame level** 单射，最优解因此塌成条件期望（模糊）。
- 它的修法是换教师：用 **teacher forcing 训出的自回归扩散模型**当 ODE 蒸馏的教师，再加 asymmetric DMD。顺带给出一个反直觉结论——**teacher forcing 比 diffusion forcing 更适合训 AR 扩散模型**。
- 这条结论与我们 `avatar-forcing` 笔记直接张力：Avatar Forcing 用的正是 diffusion forcing，且在我们复现的消融里比普通自回归扩散稳定得多。这个对照必须写清楚，是本篇笔记的最大增量。

本篇**没有我们的接入实测**，也没有 CyberVerse 对应模型目录，属于**纯论文层笔记 + 与既有路线对照**。

## What Changes

- 新建 `management/docs/论文笔记/causal-forcing.md`（10 节骨架）+ 同名 sidecar `causal-forcing.json`。
- 第 3 节承载理论主线：frame-level injectivity 的定义、违反后的条件期望塌陷、双向教师为何必然违反、以及三阶段方法（TF 训 AR 扩散 → causal ODE 蒸馏 → asymmetric DMD），并附 causal CD 扩展。
- 第 6 节如实登记评测口径两处陷阱：基线的吞吐/延迟**取自 Self Forcing 论文**而非本文实测；Dynamic Degree / VisionReward / Instruction Following 用的是自建 100-prompt 运动集，而 VBench 的 Total/Quality/Semantic 仍走官方 prompt。
- 第 8 节写「与 `avatar-forcing` 的 diffusion forcing 张力」：本文预言 DF 会因训练-推理分布失配而塌陷，而 Avatar Forcing 在运动隐空间用 DF 稳定工作；只作机制对照并**显式标注为我们的推断、未验证**。
- 发布 5–6 张原图到 `management/docs/_assets/causal-forcing/`。
- 更新 `论文笔记/README.md` 清单中 `causal-forcing.md` 的状态为「已完成」。

## Capabilities

### New Capabilities

无。纯文档变更。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 新增：`management/docs/论文笔记/causal-forcing.md`、`management/docs/论文笔记/causal-forcing.json`、`management/docs/_assets/causal-forcing/*.webp`。
- 修改：`management/docs/论文笔记/README.md`（一行状态）。
- 素材：`.cache/article-note/causal-forcing/`（`example_paper.tex` 834 行 LaTeX 源、HTML 派生正文、17 张候选图 PDF、`synthesis.md`）。
- 不修改 `avatar-forcing.md` 正文（其「后续工作」表已含本篇），不改前后端代码、API、依赖或排序常量。
