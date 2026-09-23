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

