## Why

`论文笔记/README.md` 已把 `pixel3dmm` 登记为待读（本轮新增）。它是本轮调研里**最不像"生成模型"的一篇**，但对我们有两处直接用途，值得单独成篇：

1. **它是 tracking / 显式监督信号的提供者**：[[论文笔记/performrecast|PerformRecast]] 靠它从视频跟踪 FLAME 参数、取 49 个显式 3D 关键点做 FLAME Loss，从而丢掉 LivePortrait 的四项辅助损失与第二阶段；FlexAvatar 用它给野外单图估 FLAME。
2. **它的成本极低且数据全公开**：2×A6000 / 3 天收敛（batch 40），论文明确把这当作卖点——对我们"能不能自己复现一个可用跟踪器"是正面证据。

另外它有一条局限正好压在我们的判据线上：论文 §6 明确写"基于优化的方法**无法完美区分 identity 与 expression 参数**，因此需要专门设计的先验"——这与本项目关心的身份/运动解耦是同一轴。

本篇**没有我们的接入实测**（但评测框架里已有 `driving_mode: pixel3dmm`），属**纯论文层笔记 + 与既有路线的接口说明**。

## What Changes

- 新建 `management/docs/论文笔记/pixel3dmm.md`（10 节骨架）+ 同名 sidecar。
- 讲清**两段式**方法：先用两个 ViT 预测**逐像素几何线索**（surface normal 与 **uv-coordinate**），再用这些线索**约束 FLAME 参数的优化**；含单图拟合与单目视频跟踪两条用法。
- 如实登记关键设计事实与**容易写错的三点**：骨干是 **DINOv2**（不是 DINOv3）、主干**未冻结**（学习率降 10×）、**DPT 头被实验否掉**（只增耗时、不提升下游重建）。
- 登记成本与数据：**976K 图像 / 1000+ 身份**（NPHM + FaceScape + Ava256 对齐到 FLAME 拓扑）、用 **IC-Light** 做光照增广、**2×A6000 × 3 天**收敛、拟合 500 步约 **30 秒**（未优化）。
- 第 6 节写自建基准（**posed 与 neutral 双任务**，首个同时评测两者）与协议（单向 Chamfer / 法向余弦 NC / **R2.5**）。
- 第 8 节写**与数字人的关系**：它不是生成模型而是监督来源；成本门槛对我们有利；它的第三条局限接进第七章判据；并说明我们评测框架已有 `driving_mode: pixel3dmm`。
- 发布 5 张原图到 `management/docs/_assets/pixel3dmm/`。
- 更新 `论文笔记/README.md` 中 `pixel3dmm.md` 状态为「已完成」。

## Capabilities

### New Capabilities

无。纯文档变更。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 新增：`management/docs/论文笔记/pixel3dmm.md`、`pixel3dmm.json`、`_assets/pixel3dmm/*.webp`。
- 修改：`management/docs/论文笔记/README.md`（一行状态）。
- 素材：`.cache/article-note/pixel3dmm/`（HTML 正文 254 KB、PDF、6 张已下原图、三 lane 分析）。
- 不改前后端代码、API、依赖或排序常量；不修改第七章正文（属 `docs-dh-field-tech-applicability`）。
