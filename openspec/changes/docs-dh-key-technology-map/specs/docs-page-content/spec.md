## ADDED Requirements

### Requirement: sidecar 承载论文信息对并由文档内表格渲染

文档同名 sidecar json SHALL 在既有 `changelog` / `progress` / `appendix` / `related` 之外支持可选字段 `papers`，其值为记录数组；每条记录 SHALL 至少含 `id`、`title`、`qa`，并 MAY 含 `institution`、`venue`、`year`、`authors`、`method_family`、`blog_url`、`blog_date`、`note`、`note_type`、`derives_from`、`derived_by`、`tags`。`qa` SHALL 为问题-解法对数组，每项含 `question` 与 `answer`；一条记录 MAY 含多个 `qa` 项。

文档正文 SHALL 可放置占位标记 `<!-- papers-table -->`。文档页 SHALL 从正文中剥离该标记，并在其位置渲染一张由当前文档 sidecar 的 `papers` 驱动的表格。

该表格 SHALL 至少展示：标题、发布机构、venue·年份、提出的问题、解法、继承自、笔记。表格 SHALL 支持按列排序，并 SHALL 支持按 `method_family` 筛选。

「笔记」列的行为 SHALL 由 `note_type` 决定：`doc` 时以站内文档路由 `/management/docs/<note>` 打开；`blog` 时以新窗口打开外链；`note` 缺失时 SHALL 显示占位（如「未建」）而非空链接。

文档页取数层 SHALL 在开发模式从详情接口取得 `papers`，在生产静态构建中从构建期生成的同等详情数据取得 `papers`；两种来源的表格渲染契约必须一致。

无 `papers` 字段或 `papers` 为空的文档 MUST NOT 渲染表格区块，也 MUST NOT 因占位标记存在而报错。

#### Scenario: 按 sidecar 渲染信息表

- **WHEN** 某文档的 sidecar 含非空 `papers`，且正文含占位标记 `<!-- papers-table -->`
- **THEN** 文档页在该位置渲染出一张表格，正文不出现占位标记文字
- **AND** 某条记录含多个 `qa` 项时，这些 Q-A 对各占一行（或同一论文分组内全部列出），不丢失问题与解法

#### Scenario: 表格排序与筛选

- **WHEN** 读者在信息表上点击「年份」表头或选择某个 `method_family`
- **THEN** 表格按年份排序 / 只显示该方法族的条目，其余字段内容不变

#### Scenario: 笔记列区分站内与外部

- **WHEN** 某条记录 `note_type` 为 `doc`、另一条为 `blog`
- **THEN** 前者的笔记链接走站内文档路由，后者在新窗口打开外链；`note` 缺失的记录显示占位而非可点击空链接

#### Scenario: 静态构建下表格一致

- **WHEN** 生产静态构建完成并打开同一文档
- **THEN** 表格从构建期注入的同等 sidecar 数据渲染，行数、字段与开发模式一致

#### Scenario: 无数据的文档

- **WHEN** 文档 sidecar 无 `papers` 字段或为空数组，正文仍含占位标记
- **THEN** 不渲染表格区块，页面正常，无报错
