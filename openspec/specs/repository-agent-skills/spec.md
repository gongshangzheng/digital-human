# repository-agent-skills Specification

## Purpose
为仓库提供可随 Git 版本化、可被多个 Agent 发现和复用的共享 skill 目录，同时保证现有 pi 工作流在目录迁移后仍然可用。
## Requirements
### Requirement: Repository skills use a shared source directory

仓库级、与具体 Agent 实现无关的 skill SHALL 以 `.agents/skills/<skill-name>/` 作为版本化事实来源，并包含该 skill 的 `SKILL.md` 及其必要资源。

#### Scenario: Shared skill is discoverable from the repository

- **WHEN** 任一支持仓库级 Agent skill 的 Agent 在本仓库中查找共享 skill
- **THEN** 它 SHALL be able to locate the skill under `.agents/skills/<skill-name>/SKILL.md`

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

