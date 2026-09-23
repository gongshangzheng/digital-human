## Why

FLOAT 是 Avatar Forcing 的基座之一——Avatar Forcing 直接沿用它定义的 **motion latent**（显式身份/运动分解、512D appearance `s` + 512D motion 接口 `r = Bα`），我们接入的 AvatarForcing 模型就是在该空间上重训并加因果流式与 DPO 的版本。它在《数字人身份》《数字人动作》《数字人介绍与技术路线》里被点名 6 处以上，但笔记库没有这一篇，读者无法从概述跳到方法本身；而它"正交 motion latent + 流匹配 + test-time 线性编辑"的设计，正是我们这条"低维运动空间生成"路线的源头之一。

## What Changes

- 新增 `management/docs/论文笔记/float.md`：按 10 节骨架成文，含论文原图（6 张矢量图栅格化后发布）与公式、术语与符号表
- 新增 sidecar `management/docs/论文笔记/float.json`
- 发布采用图到 `management/docs/_assets/float/`（WebP，单图 ≤500KB、单篇 ≤5MB）
- 链接回补：把概述中的点名换成文档链接（《数字人动作》42/63、《数字人身份》88、《数字人介绍与技术路线》91；仅替换链接）
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- 三篇概述文档新增站内链接
- 不涉及渲染器、构建与后端接口
