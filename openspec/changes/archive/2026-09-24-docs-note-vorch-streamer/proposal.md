## Why

`vorch-streamer` 是本轮新增登记（见 `论文笔记/README.md`），也是与我们既有三条笔记最直接对撞的一篇：它把「自回归复用生成块作上下文 ⇒ exposure bias ⇒ 长时误差与视觉漂移累积」写成首要困境，并给出一个**后训练**解法（长时自强制 + DMD 蒸馏）。我们这边已经有 `avatar-forcing` 的漂移诊断（方向游走 + 静音放大）、`liveact` 的 ARPP/ConvKV、`ditto` 的参考锚定——这篇能补齐「同一问题在 T2AV 全双工设定下的第四条路线」，且它自带 Drift / Identity 等时序指标的量化结果。

素材已就绪：论文 `arXiv:2608.05663v2`（4 张正文图，其中 Figure 2 为 SVG）、4 个分析 lane 已完成并通过 `validate-analysis.py`。该论文**没有**我们的接入实测（知识库中无任何 Vorch 相关素材），因此本篇是纯论文层笔记，工程层只写「与我们既有路线的对照」。

## What Changes

- 新建 `management/docs/论文笔记/vorch-streamer.md`（10 节骨架 + 同名 sidecar），含 4 张论文原图。
- 第 8 节写三件必须如实登记的事：① 合成数据只用「model-consistent」一条理由（无真人数据配比/清洗/许可说明）；② Table 1 的加粗/下划线**跨 T2AV 与 TIA2V 两组统一比较**，与图注「不可直接比较」的警告并存；③「支持打断/切换语音」没有量化协议。
- 明确写清 **T2AV 与 TIA2V 不是同一任务**（后者的 WER 由外部 TTS 决定，不衡量 avatar 生成器）。
- 更新 `论文笔记/README.md` 清单：`vorch-streamer.md` 状态改为已完成。

## Capabilities

### New Capabilities

无（纯文档变更，`skip_specs: true`）。

### Modified Capabilities

无。

## Impact

- 新增 `management/docs/论文笔记/vorch-streamer.md` 与 `vorch-streamer.json`；新增 `management/docs/_assets/vorch-streamer/`（4 张 WebP，其中 Figure 2 需先从 SVG 栅格化）。
- 修改 `management/docs/论文笔记/README.md` 一行。
- 来源：`papers/` 无此条目（arXiv:2608.05663 尚未入库，frontmatter 只写 `arxiv_id`）、`.cache/article-note/vorch-streamer/`（raw + 5 lane）。
- 不改前/后端代码、API、依赖与既有 OpenSpec 产品规格。
