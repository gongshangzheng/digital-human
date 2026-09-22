## Purpose

定义文档页（`/management/docs`）列表的顺序如何被显式控制：新 `order` 字段表达阅读顺序，`id` 保留编号语义，文件夹先后可控，且未使用新字段时与现状兼容。

## ADDED Requirements

### Requirement: 用 `order` 字段显式表达阅读顺序

文档 frontmatter SHALL 支持 `order` 字段（数字）。列表排序中 `order` 的优先级 SHALL 高于 `id`：`order` 越小越靠前。未写 `order` 的文档 SHALL 继续按 `id` 排序，行为与改动前一致。

#### Scenario: 两篇都写了 order
- **WHEN** `A.md` 写 `order: 1`、`B.md` 写 `order: 2`（其余字段相同）
- **THEN** 列表中 A 排在 B 之前

#### Scenario: 未写 order 时不改变现状
- **WHEN** 某文档没有 `order` 字段
- **THEN** 它仍按 `id` 升序参与排序（知识库 22 篇的顺序不变）

#### Scenario: order 非数字
- **WHEN** `order` 的值不是数字
- **THEN** 该字段被忽略，回退到 `id` → `date` 排序，不报错

### Requirement: 排序链最终必须确定（不得落到文件系统顺序）

当 `order`、`id`、`date` 都无法区分两篇文档时，系统 SHALL 以稳定且与文件系统无关的附加键（如 slug 字典序）作为最后一级，保证列表顺序确定、可复现。

#### Scenario: 全部排序键相同
- **WHEN** 两篇文档同 `date`、同 `id`、都无 `order`
- **THEN** 它们的先后由 slug 字典序决定，且重复请求结果一致

### Requirement: 文件夹在列表中的先后可配置

文档列表树中文件夹的先后 SHALL 由服务端配置的顺序决定（默认 `实习复盘 → 论文笔记 → knowledge`）；未列入配置的文件夹 SHALL 排在已配置的之后，并在其后按 `order` → `id` → `date` 排序。

#### Scenario: 默认顺序
- **WHEN** 文档树包含 `实习复盘/`、`论文笔记/`、`knowledge/` 三个文件夹
- **THEN** 列表中依次出现 实习复盘 → 论文笔记 → knowledge

#### Scenario: 未配置的文件夹
- **WHEN** 新增一个未列入配置的文件夹（如 `temp/`）
- **THEN** 它排在已配置文件夹之后，不报错
