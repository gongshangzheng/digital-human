## Why

Face Vid2vid（CVPR 2021 oral）是 **LivePortrait 的基座**，也是整条「隐式关键点 + warping」路线的转折点：它首次引入 **3D 隐式关键点**，把运动显式分解成「身份 canonical 关键点 + 头姿 + 表情形变」三项，从而同时拿到**局部自由视角**与**低带宽传输**（每帧只传关键点扰动）。LivePortrait 的 Eq. 1、等变/先验损失、外观特征体与 warp 解码全出自这篇，Ditto 的运动空间血统也在这条线上。它目前只在我们新写的 `liveportrait.md` 里被提及（作为前置），笔记库没有独立一篇，读者无法顺着"前置"继续读。

## What Changes

- 新增 `management/docs/论文笔记/face-vid2vid.md`：按 10 节骨架成文，含论文原图（6 张）与公式、术语与符号表
- 新增 sidecar `management/docs/论文笔记/face-vid2vid.json`
- 发布采用图到 `management/docs/_assets/face-vid2vid/`（WebP，单图 ≤500KB、单篇 ≤5MB）
- 链接回补：把 `liveportrait.md` 中提到 Face Vid2vid 的首现处（第 28 行）换成文档链接
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- `liveportrait.md` 与 `face-vid2vid.md` 形成「前置 ↔ 下游升级」双向互链
- 不涉及渲染器、构建与后端接口
