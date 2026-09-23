## Why

`management/docs/论文笔记/README.md` 的现有清单登记了 16 篇待写论文笔记，`ditto.md` 是其中第一篇（深读 + 工程层）。它是已完成的 `avatar-forcing.md` 的天然对照篇：两篇同属「运动空间 + 流式」路线，但 Ditto 走 LivePortrait 参考锚定渲染、Avatar Forcing 走块因果递归 latent，我们的长时漂移实验只有配上 Ditto 侧证据才能形成完整判断。素材已就绪（arXiv HTML v3 + PDF + 6 张原图 + CyberVerse `models/ditto/` 代码 + 7 篇知识库文档），6 个分析 lane 已完成并通过 `validate-analysis.py`。

## What Changes

- 新建 `management/docs/论文笔记/ditto.md`（10 节骨架 + 同名 sidecar），覆盖论文机制、训练/实现、流式推理、实验数字、相关工作定位、局限与我们的实测。
- 发布 4–6 张论文原图到 `management/docs/_assets/ditto/`（WebP，最长边 ≤1600px、单图 ≤500KB）。
- 更新 `management/docs/论文笔记/README.md` 现有清单：`ditto.md` 状态改为已完成。
- 在笔记中登记两条**代码级澄清**（论文未写、知识库也没写清）：265 维的真实构成与「66 是 bin 不是自由度」。
- 把三项口径边界写进正文：三层 RTF 不可合并、「头部放大漂移」不属 Ditto、前 3.2 秒音画错位仍未定因。

## Capabilities

### New Capabilities

无（纯文档变更，`skip_specs: true`）。

### Modified Capabilities

无（不改变产品或接口行为）。

## Impact

- 新增 `management/docs/论文笔记/ditto.md` 与 `ditto.json`；新增 `management/docs/_assets/ditto/`（4–6 张 WebP）。
- 修改 `management/docs/论文笔记/README.md` 清单一行。
- 来源：`papers/arxiv-2411.19509`、`.cache/article-note/ditto/`（raw + 6 lane）、`knowledge/` 七篇（Ditto 模型精读、Ditto 改动实践、Ditto 实时化与 TensorRT 加速复盘、动作空间专题、音画同步专题、数据集整理专题、评测指标专题、digital-human-realtime-gpu-comparison）、CyberVerse `models/ditto/` 与 `management/docs/ditto-design.md`、`avatar-rtf-latency-over-time.md`（锚定 @4968280）。
- 不修改前后端代码、API、依赖与既有 OpenSpec 产品规格。
