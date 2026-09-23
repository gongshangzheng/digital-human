# repository-agent-skills Specification

## Purpose
为仓库提供可随 Git 版本化、可被多个 Agent 发现和复用的共享 skill 目录，同时保证现有 pi 工作流在目录迁移后仍然可用。
## Requirements
### Requirement: Repository skills use a shared source directory

仓库级、与具体 Agent 实现无关的 skill SHALL 以 `.agents/skills/<skill-name>/` 作为版本化事实来源，并包含该 skill 的 `SKILL.md` 及其必要资源。

#### Scenario: Shared skill is discoverable from the repository

- **WHEN** 任一支持仓库级 Agent skill 的 Agent 在本仓库中查找共享 skill
- **THEN** 它 SHALL be able to locate the skill under `.agents/skills/<skill-name>/SKILL.md`

### Requirement: Documentation workflow has one project-scoped entry point

仓库 SHALL 在 `.agents/skills/documentation/` 提供唯一的文档写作 skill。该 skill MUST 同时包含文档结构级变更的 OpenSpec 审核门禁，以及 Markdown 正文的落点、frontmatter、内部链接、图片与图题、LaTeX、Mermaid 和写作格式约定。仓库 MUST NOT 保留职责重叠的 `.agents/skills/doc-writing/` skill。

#### Scenario: Agent 查找文档写作规范

- **WHEN** Agent 需要创建、重构或格式化仓库内说明性 Markdown 文档
- **THEN** 它可从 `.agents/skills/documentation/SKILL.md` 找到流程门禁与内容规范，无需依赖全局 skill

#### Scenario: 旧入口不再保留

- **WHEN** 检查项目共享 skills 目录
- **THEN** 不存在 `.agents/skills/doc-writing/`，文档写作流程不出现两个重叠入口

### Requirement: Article-note formula guidance matches rendered Markdown

项目级 `article-note` skill SHALL 指导论文笔记以 `$...$` 和 `$$...$$` 书写可渲染的 LaTeX 公式，并要求为公式提供符号表与中文解释。该 skill SHALL 指明 Mermaid 节点公式使用 `$$...$$`，并在校验中提示不受支持的 `\(...\)`、`\[...\]` 与 `\begin{equation}` 写法。

#### Scenario: 撰写带公式的论文笔记

- **WHEN** 作者需要在论文笔记中呈现行内、块级或 Mermaid 节点公式
- **THEN** skill 分别指导使用 `$...$`、`$$...$$` 和 Mermaid 内的 `$$...$$`，并保留符号解释要求

#### Scenario: 校验不支持的公式定界符

- **WHEN** 论文笔记包含 `\(...\)`、`\[...\]` 或 `\begin{equation}`
- **THEN** article-note 校验提示替换为受支持的 `$...$` 或 `$$...$$` 写法，而不把可渲染公式误报为必须代码块

### Requirement: Documentation skill packages document order tooling

项目级 `documentation` skill SHALL 随 Git 在 `.agents/skills/documentation/` 下提供文档 order 维护工具及其可发现的使用说明。该工具 SHALL 支持列出文档排序、以默认 dry-run 方式插入文档、经显式确认后写入，以及按当前阅读顺序重新编号；它 SHALL 不要求第三方 Python 依赖。

#### Scenario: Agent discovers ordering support while writing a document

- **WHEN** Agent 读取 `.agents/skills/documentation/SKILL.md` 并需要在文档目录中插入或重排文档
- **THEN** 它能够从该 skill 得到工具的仓库内路径、默认安全行为和适用命令

#### Scenario: Repository is used without optional Python packages

- **WHEN** 环境只提供 Python 标准库
- **THEN** skill 随附的排序工具仍能列出、插入和重排包含有效 frontmatter 的 Markdown 文档

### Requirement: Pi-specific configuration remains separate

pi 专属的 prompts、subagents 和其他运行配置 SHALL 继续位于 `.pi/`，不得通过迁移共享 skill 的方式混入全局用户目录。

#### Scenario: Repository is used by pi

- **WHEN** pi 在本仓库中加载项目配置
- **THEN** `.pi/prompts/` 与 `.pi/subagents/` 等 pi 专属目录 SHALL remain available

### Requirement: Existing skill invocation remains compatible

迁移前已经存在的 OpenSpec skill SHALL 在迁移后保持相同的 skill 名称、入口文件和工作流语义；依赖旧 `.pi/skills` 路径的调用 SHALL receive a compatibility path or equivalent resolution.

#### Scenario: Existing OpenSpec skill is invoked after migration

- **WHEN** 用户调用现有的 OpenSpec apply、propose、explore、archive、sync 或 update skill
- **THEN** the invocation SHALL resolve to the migrated skill under `.agents/skills` without requiring a new global installation

### Requirement: Shared skills are selected by project relevance

从上游同步 skill 时，仓库 SHALL only include skills relevant to the project workflow and SHALL NOT copy unrelated business-specific skills or demo data merely because they exist upstream.

#### Scenario: Upstream contains mixed shared skills

- **WHEN** the repository synchronizes skills from ProjFlow
- **THEN** only approved workflow skills and their required resources SHALL be included, while unrelated modules SHALL remain absent

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

### Requirement: Paper-note validation accepts the folder ordering key

`article-note` 的笔记校验 SHALL 接受 `documentation` skill 要求的排序键 `order`，使带阅读顺序的论文笔记能通过交付校验；校验 SHALL 继续拒绝其他未知的 frontmatter 字段。

#### Scenario: 笔记带 order 字段

- **WHEN** 论文笔记 frontmatter 含 `order: 10`
- **THEN** 笔记校验通过，不报「unsupported frontmatter fields」

#### Scenario: 未知字段仍被拒绝

- **WHEN** 论文笔记 frontmatter 含 `order` 之外的未声明字段
- **THEN** 校验仍报错并列出该字段

