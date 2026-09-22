## MODIFIED Requirements

### Requirement: 用 `order` 字段显式表达阅读顺序

文档 frontmatter SHALL 支持 `order` 字段（数字）。列表排序中 `order` 的优先级 SHALL 高于 `id`：`order` 越小越靠前。未写 `order` 的文档 SHALL 继续按 `id` 排序，行为与改动前一致。

`order` 的取值 SHALL 以 **10 为步长递增**（如 `10, 20, 30`），使相邻文档之间保留插入空间；在同一文档目录内新增或重排文档时，SHALL 优先使用中间空位，而 SHALL NOT 为插入一篇而重排既有文档的编号。

#### Scenario: 两篇都写了 order
- **WHEN** `A.md` 写 `order: 10`、`B.md` 写 `order: 20`（其余字段相同）
- **THEN** 列表中 A 排在 B 之前

#### Scenario: 在两篇之间插入新文档
- **WHEN** 文档目录内已有 `order: 10` 与 `order: 30` 两篇，新增一篇要求排在两者之间
- **THEN** 新文档写 `order: 20` 即可，既有文档的 `order` 均不变

#### Scenario: 未写 order 时不改变现状
- **WHEN** 某文档没有 `order` 字段
- **THEN** 它仍按 `id` 升序参与排序（知识库 22 篇的顺序不变）

#### Scenario: order 非数字
- **WHEN** `order` 的值不是数字
- **THEN** 该字段被忽略，回退到 `id` → `date` 排序，不报错
