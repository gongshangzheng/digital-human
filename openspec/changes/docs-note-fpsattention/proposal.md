## Why

`论文笔记/README.md` 登记了「生成侧加速十篇」（清单最后十行），`fpsattention` 是其中第一篇。这批笔记的素材已经存在——知识库《视频生成训练与推理加速专题》与博客 `video-gen-acceleration` 都覆盖了它们——但**都还没有笔记正文**，而《数字人加速》正文已点名这十个工作、只差链接（伞 change 的 3.1 依赖这一点）。

FPSAttention 还有一层与我们直接相关的意义：它的加速收益建立在 **Hopper 的 FP8** 上，而我们在 `liveact` 篇记录的正是「**A10 没有 FP8 硬件 ⇒ FP8 路线作废**」。这篇能把那条一手经验放进论文级语境里对照。

素材已就绪：arXiv `2506.04648v2`（NeurIPS 2025 Spotlight，ZIP Lab；HTML + 26 页 PDF + 3 张正文图），4 个委派 lane 已完成并通过 `validate-analysis.py`；其中**本地素材交叉核对 lane 抓到博客页两处实质错误**（见 design 待决项）。

## What Changes

- 新建 `management/docs/论文笔记/fpsattention.md`（10 节骨架 + 同名 sidecar），含 3 张论文正文图。
- 如实登记六处口径纪律：kernel 与 E2E 是两套加速比；SageAttention 在本论文里是 INT8 PTQ（**1.26× 属于 FP8 行**）；「VBench 未降」应写为 **+1.8% 且列出下降维度**；附录 E 讲的是**跨论文可比性**而非「VBench 指标失效」；**不能写成「老卡跑不了」**（论文 Limitations 的原话是老硬件仍受益但 FP8 加速打折）；Figure 7 图内**基线最低损失反而更低**。
- 第 8 节接住我们的一手经验（`liveact` 篇的 A10 无 FP8 结论），把「硬件依赖」写成可判定的选型条件。
- 更新 `论文笔记/README.md` 清单：`fpsattention.md` 状态改为已完成。

## Capabilities

### New Capabilities

无（纯文档变更，`skip_specs: true`）。

### Modified Capabilities

无。

## Impact

- 新增 `management/docs/论文笔记/fpsattention.md` 与 `fpsattention.json`；新增 `management/docs/_assets/fpsattention/`（3 张 WebP）。
- 修改 `management/docs/论文笔记/README.md` 一行。
- 来源：`.cache/article-note/fpsattention/`（raw + 5 lane）、`knowledge/视频生成训练与推理加速专题.md`、`数字人概述/数字人加速.md`、博客 `video-gen-acceleration`（用于交叉核对，不作为数字来源）。
- **不在本 change 内修博客**：博客页的两处错误位于另一个仓库（`~/gongshangzheng.github.io`），需要单独确认。
- 不改代码、API、依赖与既有 OpenSpec 产品规格。
