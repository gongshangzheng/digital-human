## Why

OmniMate 是目前少见的「**开放时长**实时音视频交互头像」方案：把「这次回复还要说多久」显式建模成连续进度条件（GPC），并用多参考条件模块（MRCM）对抗长时跨模态身份漂移。《数字人概述/数字人领域问题》已把它作为「因果统一模型如何表示开放回应」的代表点名（250 行），但笔记库没有这一篇；它也是「五篇深读」清单里尚未完成的两篇之一。

## What Changes

- 新增 `management/docs/论文笔记/omnimate.md`：按 10 节骨架成文，含 5 张论文原图（矢量图栅格化）、公式与术语符号表
- 新增 sidecar `management/docs/论文笔记/omnimate.json`
- 发布采用图到 `management/docs/_assets/omnimate/`（WebP，单图 ≤500KB、单篇 ≤5MB；按 tex 的 `trim` 参数等效裁白边）
- 链接回补：《数字人领域问题》250 行的点名处加文档链接
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- 《数字人领域问题》新增站内链接
- 不涉及渲染器、构建与后端接口
