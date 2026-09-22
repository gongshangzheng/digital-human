## Purpose

外部代码源管理能力：CyberVerse（优化版实时数字人 Agent 框架，含 Avatar Forcing、Ditto 等模型插件）等外部代码资产的来源溯源、版本锚定与知识索引规范，保证代码来源可追溯、引入方式可复现。

## ADDED Requirements

### Requirement: 外部源溯源记录

被本仓库引用或索引的外部源（代码 / 文档 / 知识库），其溯源信息 SHALL 记录在知识库索引 `management/docs/knowledge/README.md` 的来源表或对应索引条目中，包含：来源位置（远端 URL / 本机路径）、引入方式、锚定 commit 与状态。仓库 MUST NOT 在根目录另设 `docs/` 或独立的外部源登记文件。溯源信息 MUST 在任何外部内容被本仓库引用或索引之前先写入。

#### Scenario: 溯源先于引用
- **WHEN** 本仓库首次引用或索引某外部源内容
- **THEN** 知识库索引的来源表或对应条目中已存在该源，且包含来源位置与锚定 commit

#### Scenario: 不另设根目录登记文件
- **WHEN** 检查仓库顶层目录与知识库索引
- **THEN** 根目录不存在 `docs/`，外部源信息只出现在 `management/docs/knowledge/README.md`（或对应知识条目）中，无重复的第二份登记表

### Requirement: 引入方式规范

外部代码引入 SHALL 采用以下方式之一并在溯源记录中注明：独立 clone（推荐，保留 git 历史与 upstream 溯源）、git submodule、或 vendored 拷贝（附版本/commit 信息）。引入的代码 MUST NOT 与本仓库自有代码混在同一目录层级造成归属混淆——统一存放于专用目录。

#### Scenario: 独立 clone 引入
- **WHEN** 引用 CyberVerse 源
- **THEN** 其位于 `~/code/CyberVerse` 独立 clone（保留 git 历史与远端），知识库索引记录远端 `github.com/gongshangzheng/CyberVerse` 与当前 commit hash

### Requirement: 版本锚定

对外部源中被本仓库知识库索引的关键内容（模型插件、设计文档、基准数据），溯源记录或索引条目 SHALL 记录其所在 commit，保证后续外部源演进后引用仍可复现。

#### Scenario: commit 锚定可复核
- **WHEN** 查看知识库中指向 CyberVerse `management/docs/avatarforcing-design.md` 的索引条目
- **THEN** 条目含该文件所属 commit 的 hash，`git -C ~/code/CyberVerse show <hash>:<path>` 可还原当时内容
