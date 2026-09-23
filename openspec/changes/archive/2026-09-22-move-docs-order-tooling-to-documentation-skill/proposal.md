## Why

文档排序工具目前位于仓库根 `scripts/`，而排序规则、frontmatter 约定和文档写作流程已经由项目级 `documentation` skill 负责。将工具及其使用契约纳入该 skill，可让需要新增或重排文档的 Agent 在同一入口发现规则和可执行工具，避免依赖仓库外的隐含知识。

## What Changes

- 将标准库实现的 `docs_order.py` 从仓库根 `scripts/` 迁入 `.agents/skills/documentation/scripts/`，使其成为 `documentation` skill 的随附工具。
- 在 `documentation/SKILL.md` 中定义排序工具的用途、默认 dry-run、安全校验，以及 `list`、`insert`、`insert --shift`、`renumber` 的调用方式。
- 更新仓库内当前的文档排序调用与说明，统一使用 skill 内路径；移除根目录旧入口，避免形成两个事实来源。
- 明确插入时优先使用现有整数空位；明确要求连续十步编号时，`--shift` 重排插入点及其后的编号而保留前缀不变。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `repository-agent-skills`: 项目级 `documentation` skill 需要随 skill 一起提供文档排序工具与可发现的操作说明。
- `docs-page-content`: 文档 order 的维护规则需要定义正常插入与显式后缀顺延两种行为。

## Impact

- `.agents/skills/documentation/` 的 `SKILL.md`、新增 `scripts/docs_order.py`。
- 删除 `scripts/docs_order.py`，并更新其在 active 文档、OpenSpec artifacts 和运行说明中的路径引用。
- 不引入第三方 Python 依赖，不改变服务端读取 `order` 的排序语义。