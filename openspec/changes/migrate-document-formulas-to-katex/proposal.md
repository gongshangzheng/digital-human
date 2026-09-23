## Why

KaTeX 已成为文档渲染器的正式能力，但现有文档仍混用纯文本公式、旧的 `\(...\)` / `\[...\]` 定界符和少量已可渲染的 `$...$` / `$$...$$`。这会使同一技术说明的符号层级、可读性和页面呈现不一致；DPO 技术介绍与 Avatar Forcing 笔记尤其包含核心目标函数，应优先迁移。

## What Changes

- 仅审核长期保留、面向阅读的 DPO 技术介绍与 Avatar Forcing 论文笔记中的数学表达，区分真正的数学关系、代码/命令/货币等必须保持字面文本的内容。
- 将应排版的数学表达统一为渲染器支持的 `$...$` 行内公式或 `$$...$$` 块级公式；迁移旧 `\(...\)`、`\[...\]` 与纯文本多行公式。
- 优先完整迁移 `技术介绍/dpo-直接偏好优化.md` 与 `论文笔记/avatar-forcing.md` 的 DPO、扩散/流匹配、因果掩码与训练配置相关公式，并补齐公式附近缺失的符号解释。
- 不将产品型号、代码变量、URL、Shell、金额和普通数值伪装成公式。`management/docs/knowledge/` 是后续将清理的临时归档区，本次不审计、不迁移其中内容。
- 保留正文事实、引用、章节职责与站内链接语义；不更改公式所表达的数学含义或未披露的论文细节。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- None; 公式定界符、渲染与失败降级行为已经由 `docs-math` capability 定义，本 change 仅迁移现有内容以符合该契约。

## Impact

- `management/docs/技术介绍/dpo-直接偏好优化.md` 与 `management/docs/论文笔记/avatar-forcing.md`。
- 不改动 `management/docs/knowledge/`、渲染器、依赖、后端接口、sidecar 数据或 archived OpenSpec 历史。