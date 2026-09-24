## Why

Talker-T2AV 是「**联合文本→音视频生成**」这条线里把「两级解耦 + 自回归」讲得最清楚的一篇：高层跨模态规划交给共享因果 LM，低层渲染交给两个模态专属的轻量 DiT 头；并且它用**冻结的同帧率 1-D 编码器**（视频侧正是 **LIA-X 的 40 维 motion code @25Hz**，音频侧 WhisperX-VAE 32 维 @25Hz）让跨模态对齐「免费」。我们的《Talker-T2AV 模型精读》《Talker-T2AV 接入与验证》是知识库里的固定上游副本，但笔记库没有一篇正式笔记；它也是「五篇深读」清单里尚未完成的两篇之一。

## What Changes

- 新增 `management/docs/论文笔记/talker-t2av.md`：按 10 节骨架成文，含论文唯一的原图（Figure 1）+ **2 张 Mermaid**（补足结构表达）+ 公式与术语符号表
- 新增 sidecar `management/docs/论文笔记/talker-t2av.json`
- 发布原图到 `management/docs/_assets/talker-t2av/`（WebP）
- 链接回补：`knowledge/Talker-T2AV 模型精读.md` 与 `knowledge/Talker-T2AV 接入与验证.md` 各加一处前向链接
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- 两篇 knowledge 文档新增站内链接
- 不涉及渲染器、构建与后端接口
