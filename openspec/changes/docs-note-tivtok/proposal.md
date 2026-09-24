## Why

`docs-note-adaptok` 已完成。按约定继续第二篇素材：**TivTok**（arXiv:2606.17590），它是 `数字人领域问题` 第七章首条目（1D 视觉分词器 → 从视频提身份）的另一半。

它与 AdapTok 恰好互补，这也是必须先读它的理由：

- AdapTok 给的是**因果性与自适应预算**（块级因果、按内容密度分配），但没有身份—运动解耦；
- TivTok 给的正是**解耦**——把 clip 拆成 TIV（跨帧共享）与 TV（逐帧残差），而且论文 §4.5 明确写了一句对我们极其关键的话：**运动物体只要身份与外观稳定，也可以进 TIV，TV 只负责姿态、位置等瞬变量**。这是"从视频提身份"想要的机制，且是**架构涌现**而非显式监督。

同时它有一个必须写清的硬伤：**TivTok 的编码不是时间因果的**（TV 单帧可见、TIV 全 clip 可见），这与 AdapTok 的块级因果形成正面取舍。

## What Changes

- 新建 `management/docs/论文笔记/tivtok.md`（10 节骨架）+ 同名 sidecar。
- 第 3 节讲清三段机制：**TIV/TV 分解**（含信息论动机 $H_{\text{indep}}-H_{\text{shared}}\approx(T-1)H(C)>0$）、**SIF**（靠非对称注意力范围而非显式监督实现分解）、**IB 与跨块 TIV 复用**（解码广播 + TIV 平均合并）。
- 第 6 节登记四组数字：重建（T512 = rFVD 12.65）、长视频（128 帧压缩效率 2.91×、TivTok-T128 = 160 token / 0.20 s）、生成（16 帧 T1024 = FVD 99）、以及 TIV 容量与 TIV:TV 分配的两组权衡表。
- 第 8 节写**与数字人的关系**（本篇增值）：§4.5 的"运动物体身份稳定时可进 TIV"是关键机制，但必须同时写三点限定——① 论文只给**定性示例**（滑冰者、台球），没有身份判别指标；② TIV 语义同时含**场景几何与背景**，身份只是其中一部分；③ **编码非时间因果**，与 AdapTok 正好互补（TivTok 给解耦、AdapTok 给因果与预算）。
- 发布 5 张原图到 `management/docs/_assets/tivtok/`。
- 更新 `论文笔记/README.md` 中 `tivtok.md` 状态为「已完成」。

## Capabilities

### New Capabilities

无。纯文档变更。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 新增：`management/docs/论文笔记/tivtok.md`、`tivtok.json`、`_assets/tivtok/*.webp`。
- 修改：`management/docs/论文笔记/README.md`（一行状态）。
- 素材：`.cache/article-note/tivtok/`（HTML 正文 259 KB、PDF、5 张已下原图）。
- **不修改** `数字人概述/数字人领域问题` 第七章（属 `docs-dh-field-tech-applicability`，待本篇完成后写）。
- 不改前后端代码、API、依赖或排序常量。
