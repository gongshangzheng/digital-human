## Purpose

外部代码源管理能力：CyberVerse（优化版实时数字人 Agent 框架，含 Avatar Forcing、Ditto 等模型插件）等外部代码资产的登记、版本锚定与知识索引规范，保证代码来源可追溯、引入方式可复现。

## ADDED Requirements

### Requirement: 外部源登记表

仓库 SHALL 维护一份外部代码源登记表（Markdown），记录每个外部源的名称、用途、来源位置（远端 URL 与本机路径）、引入方式、锚定 commit 与状态。登记表 MUST 在任何外部代码被本仓库引用或索引之前先创建。

#### Scenario: 登记先于引用
- **WHEN** 本仓库首次引用或索引某外部源内容
- **THEN** 登记表中已存在该源条目且包含远端 URL、本机路径与锚定 commit

### Requirement: 引入方式规范

外部代码引入 SHALL 采用以下方式之一并在登记表中注明：独立 clone（推荐，保留 git 历史与 upstream 溯源）、git submodule、或 vendored 拷贝（附版本/commit 信息）。引入的代码 MUST NOT 与本仓库自有代码混在同一目录层级造成归属混淆——统一存放于专用目录。

#### Scenario: 独立 clone 引入
- **WHEN** 登记 CyberVerse 源
- **THEN** 其位于 `~/code/CyberVerse` 独立 clone（保留 git 历史与远端），本仓库登记表记录远端 `github.com/gongshangzheng/CyberVerse` 与当前 commit hash

### Requirement: 版本锚定

对外部源中被本仓库知识库索引的关键内容（模型插件、设计文档、基准数据），登记表或索引条目 SHALL 记录其所在 commit，保证后续外部源演进后引用仍可复现。

#### Scenario: commit 锚定可复核
- **WHEN** 查看知识库中指向 CyberVerse `management/docs/avatarforcing-design.md` 的索引条目
- **THEN** 条目含该文件所属 commit 的 hash，`git -C ~/code/CyberVerse show <hash>:<path>` 可还原当时内容
