## ADDED Requirements

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
