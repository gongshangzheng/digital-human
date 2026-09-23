## MODIFIED Requirements

### Requirement: Documentation skill states explicit ordering conventions per folder

`documentation` skill SHALL 规定**第一方内容文件夹**使用**显式排序键**，并说明外部复制件文件夹的豁免范围、缺省行为、索引文件要求与交付校验，使新建第一方文档的顺序不依赖文件日期或文件系统顺序。

skill SHALL 写明：

- **第一方内容文件夹**（`数字人概述/`、`论文笔记/`、`技术介绍/` 及以后新建的第一方主题目录）中的正文文档用 `order` 表达阅读顺序，取值以 10 为步长（`10, 20, 30`）。
- **外部复制件文件夹**（如 `knowledge/`，从博客与 InternWiki 复制的素材）不强制排序键：沿用来源元数据即可，MAY 只带既有 `id` 或都不带；本规则 MUST NOT 要求回填来源侧本就没有的作者、摘要等字段。
- 第一方文件夹中未写 `order` 的文档会落到该文件夹内的 `date` 降序（越新越靠前），因此新建文档 MUST NOT 依赖日期隐式排序来决定阅读顺序。
- 文件夹索引 README，无论属于第一方还是复制件文件夹，SHALL 带最小 frontmatter，使顺序工具在该目录可用，且列表标题不退化为裸 slug。
- 交付检查 SHALL 包含「**第一方**目录的 `order` 完整、无重复、与既定阅读顺序一致」。

#### Scenario: Agent 新建一篇文档

- **WHEN** Agent 在某个含既有文档的**第一方**文件夹中新增一篇文档，且该目录已有 `order: 10` 与 `order: 30`
- **THEN** skill 要求为新文档写入 `order`（占用 `20` 空位而非重排既有文档），并且不依赖 `date` 决定其位置

#### Scenario: 目录缺少显式排序键

- **WHEN** 某个**第一方**文件夹内多篇文档都没有 `order`
- **THEN** skill 说明列表会按该目录内的 `date` 降序排列，并要求 Agent 在交付前补齐 `order`

#### Scenario: 外部复制件文件夹豁免排序键

- **WHEN** `knowledge/` 这类外部复制件文件夹内的文档既没有 `order`、部分也没有 `id`
- **THEN** skill 说明该文件夹不强制排序键、不要求回填来源侧缺失的作者与摘要字段，并按既有 `id` → `date` 降序参与排序

#### Scenario: 索引 README 缺少 frontmatter

- **WHEN** 某文件夹内存在没有 frontmatter 的索引 `README.md`
- **THEN** skill 说明顺序工具在该目录会以缺 frontmatter 的错误直接失败，并给出补最小 frontmatter 的修复方式

#### Scenario: 交付前的顺序校验

- **WHEN** Agent 准备交付一次文档变更
- **THEN** skill 的交付检查要求确认**第一方**目录的 `order` 无缺失、无重复且与实际阅读顺序一致
