## Why

当前库没有任何一篇解释"人脸身份验证（人脸识别）模型"的技术介绍：`ArcFace`、`CosFace`、`AdaFace` 这些词只以"评测尺子"或"训练损失"的身份出现在 `数字人概述/数字人身份` 与 `knowledge/digital-human-identity-consistency` 里，读者无法从库内理解它们各自解决什么问题、如何演进、以及为什么把它们挪用到生成侧当裁判时要打折扣。

外部站点 `~/gongshangzheng.github.io` 也没有这个总结，已核查：只有 `src/pages/arcface-2018.html` 一篇 ArcFace 单篇深读（问题形式化、测地线距离、additive angular margin、sub-center ArcFace、ArcFace 反演），以及 `digital-human-identity-consistency` 第 2.4 节对人脸识别编码器谱系（VGG-Face → FaceNet → ArcFace → CurricularFace / AdaFace → SFace / GhostFaceNet）的几百字梳理——两者都是"生成评测借来的尺子"视角，前者只讲一篇论文，后者只为一章度量批判服务。身份验证模型本身的任务定义、损失谱系、数据与骨干工程、自适应改进与选型，在库内外都缺一篇可复用的技术介绍。

## What Changes

- 在 `management/docs/技术介绍/` 新增一篇通用技术介绍 `face-verification-models.md`（暂定 slug），覆盖：任务定义与协议 / 指标、从 softmax 到度量学习的损失谱系（含 ArcFace 公式与几何直觉）、决定上限的数据与骨干工程、自适应 margin 与鲁棒性改进、作为数字人度量与损失时的接口与失效边界、场景到模型的选型对照、术语表。
- 该篇只讲**通用机制与谱系**，不写任何具体数字人模型的实验细节；项目自身的实测（方向游走、锚点引导、CSIM 当 loss 放弃等）保留在 `数字人概述/数字人身份`，两篇用站内链接相连。
- 更新 `数字人概述/数字人身份` 的度量段落，把可复用的人脸识别原理改为链接到新文档，避免两处重复解释 ArcFace 及其后继者。
- 为新文档补齐 frontmatter（`title` / `author` / `date` / `tags` / `summary` / `order`）与同名 sidecar JSON。

## Capabilities

### New Capabilities

无。本变更只新增和调整说明性文档，不改变产品或接口行为。

### Modified Capabilities

无。变更声明 `skip_specs: true`（纯文档变更，无 spec 级行为改变）。

## Impact

- 新增 `management/docs/技术介绍/` 下的身份验证模型说明文档及同名 sidecar JSON。
- 修改 `management/docs/数字人概述/数字人身份.md` 的度量相关措辞与跨文档链接（可能同步其 sidecar 的 `related`）。
- 依据资料：`management/docs/knowledge/digital-human-identity-consistency.md`、`management/docs/数字人概述/数字人身份.md`、博客 `arcface-2018` 页，以及 ArcFace / CosFace / SphereFace / FaceNet / AdaFace / MagFace / CurricularFace / ElasticFace / sub-center ArcFace / Partial FC 等一手论文（书目与公式在素材阶段逐篇核实）。
- 不修改前后端代码、API、依赖、排序常量或既有 OpenSpec 产品规格。
