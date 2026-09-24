## Why

`论文笔记/` 已有 `liveportrait`（隐式关键点 + stitching/retargeting）与 `face-vid2vid`（可分解 3D 隐式关键点）两篇，它们是我们「隐式关键点」主线的前置；`ditto`、`avatar-forcing` 等下游笔记都以 LivePortrait 的 265D 运动空间为输入。**PerformRecast 正好改的就是这条链的表示层核心——关键点变换公式**：它指出 LivePortrait 的 `x = s·(x_c·R + δ) + t`（先乘 R 再加 δ）会让表情形变混入头姿信息，从而无法真正做到「只改表情、头不动」；改成与 FLAME 前向一致的 `x = s·((x_c+δ)·R) + t` 后即可继承 3DMM 的自然解耦。

这篇对我们有双重价值：① 它是「公式一致性 > 损失堆叠」的直接证据——用一个公式改动 + 49 个显式 3D 关键点监督，替掉了 LivePortrait 的 4 项辅助损失与第二训练阶段；② 它的失败案例（源闭嘴/驱动张嘴时牙齿模糊）正好标示了 GAN-warping 路线与扩散路线的能力边界，与我们已有笔记里的能力—代价讨论互补。

`论文笔记/performrecast.md` 目前不存在，博客 `paper-performrecast` 已有精读但仅覆盖 Replacement 模式，且未登记 Enhancement 列与附录训练配置。本次产出库内正式笔记。

## What Changes

- 新建 `management/docs/论文笔记/performrecast.md`：10 节骨架，含 6 张原图、≥7 个公式、1 张 Mermaid、训练配置披露表、Table 1（Replacement + Enhancement 两列）/ Table 2 / Table 3 的实验表。
- 新建同名 sidecar `management/docs/论文笔记/performrecast.json`（changelog / related）。
- 发布 6 张论文原图到 `management/docs/_assets/performrecast/`（WebP，≤1600px、≤500KB）。
- 更新 `论文笔记/README.md` 的篇目清单，登记本篇。
- 不修改任何笔记正文以外的代码、sidecar 结构或既有文档。

## Capabilities

### New Capabilities

无（纯文档变更，`.openspec.yaml` 声明 `skip_specs: true`）。

### Modified Capabilities

无。

## Impact

- 新增：`management/docs/论文笔记/performrecast.md`、`.json`、`management/docs/_assets/performrecast/*.webp`。
- 修改：`management/docs/论文笔记/README.md`（清单补一行）。
- 素材：`.cache/article-note/performrecast/`（`paper.txt` 派生自 arXiv HTML `2603.19731v1`、`blog.txt`、`raw/facts.md`、`raw/figures/` 9 张原图）。
- 不改代码、API、依赖与既有 OpenSpec 产品规格。
