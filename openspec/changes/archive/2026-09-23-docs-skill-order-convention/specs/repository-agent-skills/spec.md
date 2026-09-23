## ADDED Requirements

### Requirement: Documentation skill states explicit ordering conventions per folder

`documentation` skill SHALL 规定 `management/docs/` 下每个含说明性文档的文件夹使用**显式排序键**，并说明缺省行为、索引文件要求与交付校验，使新建文档的顺序不依赖文件日期或文件系统顺序。

skill SHALL 写明：

- 正文文档用 `order` 表达阅读顺序，取值以 10 为步长（`10, 20, 30`）；外部复制件一类沿用既有 `id` 排序键的文件夹（如 `knowledge/`）MAY 继续用 `id`。
- 未写 `order` 与 `id` 的文档会落到该文件夹内的 `date` 降序（越新越靠前），因此新建文档 MUST NOT 依赖日期隐式排序来决定阅读顺序。
- 文件夹索引 README SHALL 带最小 frontmatter，使顺序工具在该目录可用，且列表标题不退化为裸 slug。
- 交付检查 SHALL 包含「同目录 `order` 完整、无重复、与既定阅读顺序一致」。

#### Scenario: Agent 新建一篇文档

- **WHEN** Agent 在某个含既有文档的文件夹中新增一篇文档，且该目录已有 `order: 10` 与 `order: 30`
- **THEN** skill 要求为新文档写入 `order`（占用 `20` 空位而非重排既有文档），并且不依赖 `date` 决定其位置

#### Scenario: 目录缺少显式排序键

- **WHEN** 某文件夹内多篇文档都没有 `order` 与 `id`
- **THEN** skill 说明列表会按该目录内的 `date` 降序排列，并要求 Agent 在交付前补齐 `order`

#### Scenario: 索引 README 缺少 frontmatter

- **WHEN** 文件夹内存在没有 frontmatter 的索引 `README.md`
- **THEN** skill 说明顺序工具在该目录会以缺 frontmatter 的错误直接失败，并给出补最小 frontmatter 的修复方式

#### Scenario: 交付前的顺序校验

- **WHEN** Agent 准备交付一次文档变更
- **THEN** skill 的交付检查要求确认同目录 `order` 无缺失、无重复且与实际阅读顺序一致

### Requirement: Paper-note validation accepts the folder ordering key

`article-note` 的笔记校验 SHALL 接受 `documentation` skill 要求的排序键 `order`，使带阅读顺序的论文笔记能通过交付校验；校验 SHALL 继续拒绝其他未知的 frontmatter 字段。

#### Scenario: 笔记带 order 字段

- **WHEN** 论文笔记 frontmatter 含 `order: 10`
- **THEN** 笔记校验通过，不报「unsupported frontmatter fields」

#### Scenario: 未知字段仍被拒绝

- **WHEN** 论文笔记 frontmatter 含 `order` 之外的未声明字段
- **THEN** 校验仍报错并列出该字段
