## ADDED Requirements

### Requirement: Documentation skill packages document order tooling

项目级 `documentation` skill SHALL 随 Git 在 `.agents/skills/documentation/` 下提供文档 order 维护工具及其可发现的使用说明。该工具 SHALL 支持列出文档排序、以默认 dry-run 方式插入文档、经显式确认后写入，以及按当前阅读顺序重新编号；它 SHALL 不要求第三方 Python 依赖。

#### Scenario: Agent discovers ordering support while writing a document

- **WHEN** Agent 读取 `.agents/skills/documentation/SKILL.md` 并需要在文档目录中插入或重排文档
- **THEN** 它能够从该 skill 得到工具的仓库内路径、默认安全行为和适用命令

#### Scenario: Repository is used without optional Python packages

- **WHEN** 环境只提供 Python 标准库
- **THEN** skill 随附的排序工具仍能列出、插入和重排包含有效 frontmatter 的 Markdown 文档
