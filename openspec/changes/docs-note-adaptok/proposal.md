## Why

用户决定：先把 **AdapTok** 与 **TivTok** 两篇笔记做完，再写 `数字人领域问题` 第七章「技术适用性」的首条目——因为该条目最关键的判断（AdapTok 的"时间因果"是否真能用于流式、TivTok 的 TIV 里身份占多少）依赖正文细节，只看摘要只能写"未验证"。

本篇是这两篇中的第一篇。AdapTok（arXiv:2505.17011）是"**自适应 token 分配 + 时间因果**的 1D 视频分词器"，它对我们判断的价值有两处别的论文给不了：

- 它的 token 分配依据是**重建质量**（感知损失），不是任何判别性——这直接决定"它按什么分配预算"，以及"身份信息量"是否与它的分配策略相关；
- 它的因果性是 **block-causal**（分块，每块 4 帧）而非帧级因果——这决定把它接进流式管线时的最小延迟粒度。

我们有现成的二手素材：博客 `drafts/adaptok.md`（快读草稿，含 6 张配图）与本仓库外部无重复，可作交叉核对源。

## What Changes

- 新建 `management/docs/论文笔记/adaptok.md`（10 节骨架）+ 同名 sidecar。
- 第 3 节讲清三块：**自适应 tokenizer**（3D patchification + block causal transformer + 训练期 block-wise mask sampler）、**adaptive scorer**（block-causal 打分器，预测不同 token 数下的重建质量）、**IPAL 推理期分配**（整数线性规划，在全局预算下最小化预测感知损失），并说明 block 粒度（K=4 块 × M=512，每块 4 帧）。
- 第 6 节如实登记：重建 rFVD、生成 gFVD、模型规模、两处消融（自适应机制 / 分配策略 / 打分指标）与**延迟 50.9 ms vs ElasticTok 571.7 ms**；标注"我们复现的 CausalTok 基线"这类自建对照的性质。
- 第 8 节写**与数字人的关系**（本篇笔记的主要增值）：AdapTok 的两个特性分别对上我们的流式与算力约束，但它的优化目标是重建保真、**没有身份—运动解耦机制**；因 block-causal 是**块级因果**，接入流式的最小延迟是 4 帧量级；并给出"用它做身份表示"时必须先验证的两条判据（token 分配是否与身份信息量相关；跨条件身份 token 的可比性）。
- 发布 5–6 张原图到 `management/docs/_assets/adaptok/`。
- 更新 `论文笔记/README.md` 中 `adaptok.md` 的状态为「已完成」。

## Capabilities

### New Capabilities

无。纯文档变更。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 新增：`management/docs/论文笔记/adaptok.md`、`adaptok.json`、`_assets/adaptok/*.webp`。
- 修改：`management/docs/论文笔记/README.md`（一行状态）。
- 素材：`.cache/article-note/adaptok/`（HTML 正文 284 KB、PDF 22 页、5 张已下原图）、博客 `drafts/adaptok.md`（二手核对源）。
- **不修改** `数字人概述/数字人领域问题` 第七章（属另一个 change `docs-dh-field-tech-applicability`，待两篇笔记完成后写）。
- 不改前后端代码、API、依赖或排序常量。
