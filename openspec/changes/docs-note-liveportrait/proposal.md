## Why

LivePortrait 是「隐式关键点 + warping」这条非扩散路线的代表，也是我们主线的血统来源（Ditto 的 21×3 位移表与逐维扰动控制映射与它同源）。它在《数字人身份》《数字人动作》《数字人加速》中被反复引用（3 / 5 / 3 处），但笔记库中该篇仍未撰写，引用只能停留在文字点名，读者无法顺着链接读到方法本身。

## What Changes

- 新增 `management/docs/论文笔记/liveportrait.md`：按 10 节骨架成文，含论文原图（5 张）、公式（2–3 个）、术语与符号表
- 新增 sidecar `management/docs/论文笔记/liveportrait.json`
- 发布采用图到 `management/docs/_assets/liveportrait/`（WebP，单图 ≤500KB、单篇 ≤5MB）
- 链接回补：把概述中的点名叫法换成文档链接（《数字人身份》82、《数字人动作》41、《数字人加速》159/177；仅替换链接，不改数字与结论）
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- 上述三篇概述文档新增站内链接
- 不涉及渲染器、构建与后端接口
