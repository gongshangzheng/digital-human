# Proposal: docs-note-avatar-forcing（AvatarForcing 论文笔记单篇 change）

## Why

论文笔记登记表首篇（`docs-note-*` 系列的第一篇）。AvatarForcing 是我们**深度接入过**的模型：既要做论文层精读（架构与同类差异），也要写工程层（接入状态、我们的改动、否证与失败），因此它是"论文层 + 工程层"模板的样板。

按体系规则：**论文笔记同样先建单篇 change（含大纲），审核通过后才写正文。**

## What Changes

- 整理论文层素材：论文信息（arXiv 条目）、三模块架构（运动潜空间编码 / 双路条件编码 / 因果流式生成）、与同类工作的差异
- 整理工程层素材：接入形态与插件路径、流式改造、微调（桥系列 / 注入点）、漂移诊断与治理裁决、失败结论
- 整理结果在对话中提交审核（不写入仓库），审核通过后写正文 `management/docs/论文笔记/avatar-forcing.md`

## Capabilities

### New Capabilities
（无——纯文档 change，`skip_specs: true`）

## Impact
- 新增笔记 1 篇；不改代码
- 来源：papers 库 `arxiv-2603.14331` · knowledge/《Avatar Forcing 模型精读》《Avatar Forcing Motion Latent AutoEncoder》《Avatar Forcing 微调实践》· CyberVerse `models/avatarforcing/`（核对基准 @4968280）
