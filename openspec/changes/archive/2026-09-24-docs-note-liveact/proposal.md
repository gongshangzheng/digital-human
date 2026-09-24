## Why

`management/docs/论文笔记/README.md` 的待写清单有 15 篇，`liveact.md` 是其中第一篇（深读 + 工程层「SoulX-LiveAct 接入」）。它是当前素材最齐全的一篇：有 arXiv 论文（`2603.11746v2`，7 张原图）、有 CyberVerse `models/SoulX-LiveAct/` 代码、还有我们的**第一手单卡 A10 冒烟数据**（两组完整跑通记录）——三者齐备，能同时把「论文机制」和「我们的接入边界」写实。

机制上也值得单篇：这篇把争论点从「是否 AR」移到「AR 链上传播什么」（ARPP），与已完成的 [[论文笔记/avatar-forcing|Avatar Forcing]]（块因果 + 历史 offset）和 [[论文笔记/ditto|Ditto]]（参考锚定）构成同一问题的第三条路线。

## What Changes

- 新建 `management/docs/论文笔记/liveact.md`（10 节骨架 + 同名 sidecar），含 7 张论文原图。
- 如实登记论文自身的三处内部不一致：EMTD 段引用错数字、EMTD 的 FID/FVD 为全文最差且正文回避、蒸馏步数 400 vs 300。
- 工程层区分**两条接入路径**：官方 `generate.py` 单卡路线（我们实际跑通）与 CyberVerse `avatar.live_act` 插件路线（多卡硬门槛，未在 A10 跑通），不把两者混写成「LiveAct 接入完成」。
- 更新 `论文笔记/README.md` 清单：`liveact.md` 状态改为已完成。

## Capabilities

### New Capabilities

无（纯文档变更，`skip_specs: true`）。

### Modified Capabilities

无。

## Impact

- 新增 `management/docs/论文笔记/liveact.md` 与 `liveact.json`；新增 `management/docs/_assets/liveact/`（7 张 WebP）。
- 修改 `management/docs/论文笔记/README.md` 一行。
- 来源：`papers/arxiv-2603.11746`、`.cache/article-note/liveact/`（raw + 6 lane）、`knowledge/` 六篇（cyberverse-realtime-digital-human-agent、digital-human-realtime-gpu-comparison、digital-human-engineering-benchmark、模型探索与未采纳实验复盘、视频生成训练与推理加速专题、hardware-assessment）、`数字人概述/` 三篇（数字人领域问题、数字人加速、数字人行业全景）、CyberVerse `models/SoulX-LiveAct/`（锚定 `4968280`）。
- 不改前/后端代码、API、依赖与既有 OpenSpec 产品规格。
