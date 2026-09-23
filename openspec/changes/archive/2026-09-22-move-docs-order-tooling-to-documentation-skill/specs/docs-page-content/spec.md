## ADDED Requirements

### Requirement: Document order maintenance supports explicit suffix shifting

文档 order 维护工具 SHALL 在正常插入时优先使用相邻文档之间已有的整数空位，且不得改动既有文档。用户或 Agent 显式要求连续十步编号时，工具 SHALL 支持将插入点及其后的文档重排为连续十步 order，同时保持插入点之前的文档 order 不变。所有写入 SHALL 默认先以 dry-run 展示，并仅在显式确认后写盘。

#### Scenario: Insert consumes an existing gap

- **WHEN** 文档目录已有 `order: 10` 与 `order: 30`，并在二者之间插入文档且未请求重排
- **THEN** 新文档获得 `order: 20`，既有文档的 order 不变

#### Scenario: Explicit shift creates a ten-step suffix

- **WHEN** 文档目录已有 `order: 10`、`order: 20`，用户在第一篇之后插入文档并显式请求后缀顺延
- **THEN** 新文档获得 `order: 20`，原 `order: 20` 文档及其后续文档按 `30, 40, ...` 顺延，原第一篇仍为 `order: 10`

#### Scenario: Write requires explicit apply

- **WHEN** 用户运行插入或重排命令但未提供写入确认参数
- **THEN** 工具只展示创建和更新计划，不修改任何 Markdown 文件
