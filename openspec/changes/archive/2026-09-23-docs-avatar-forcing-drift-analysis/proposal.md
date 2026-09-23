## Why

现有《Avatar Forcing 模型笔记》已在“局限与启发”中用一条项目符号概括身份漂移诊断，但没有完整说明漂移为何会在流式生成中累积、实验如何区分模长与方向假说，以及静音缺少强条件约束时为何更严重。该问题是我们对论文 exposure bias 局限所做的核心实测，需要形成可追溯、边界清楚的独立小节。

## What Changes

- 在 `management/docs/论文笔记/avatar-forcing.md` 的“局限与启发”内新增“长时身份漂移：历史递归、方向游走与静音放大”三级小节。
- 将现有笼统的“漂移诊断/治理裁决”项目符号拆分为：机制链路、模长与方向的可检验假说、当前 c1 单身份 300 秒实验结果、静音段的条件缺失解释、以及已验证治理结果与跨身份边界。
- 使用明确措辞区分：论文直接结论、我们的实测、机制解释和仍待验证的泛化结论；不改变论文原始实验结论。
- 同步更新文章的“可操作启发”和相关文档指向，避免与新小节重复或互相矛盾。

## Capabilities

### New Capabilities

无（纯文档结构与内容整理）。

### Modified Capabilities

无（不涉及系统行为需求变更）。

## Impact

- 影响文档：`management/docs/论文笔记/avatar-forcing.md`。
- 依据资料：`management/docs/knowledge/Avatar Forcing 微调实践.md`、`management/docs/knowledge/Avatar Forcing 模型精读.md`、Avatar Forcing 论文方法与局限章节。
- 不涉及代码、API、数据表或模型权重改动。
