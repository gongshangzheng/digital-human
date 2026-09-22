# Proposal: move-skills-to-agents（迁移仓库级 Skill 到跨 Agent 目录）

## Why

当前仓库的 OpenSpec skill 位于 `.pi/skills/`，目录命名绑定 pi，无法清晰表达这些 skill 是仓库级、可供多个 Agent 共用的工作流。ProjFlow 已将共享 skill 统一到 `.agents/skills/`，本仓库需要对齐这一约定，同时保留 pi 的专属配置目录。

## What Changes

- 将当前仓库已跟踪的 `.pi/skills/openspec-*` 迁移到 `.agents/skills/openspec-*`，使其成为跨 Agent 共享的真实目录。
- 接入 ProjFlow 最新共享 skill 目录中的 `article-note`，用于论文精读笔记流水线。
- 从上游接入 `article-note`（论文精读笔记流水线），并按本仓库目录与 OpenSpec 流程适配。
- 不与本变更同时引入上游其他共享 skill（`doc-writing`、`upstream-sync`）与业务 skill（`management`、`papers`、`evaluation`、`web`、`design-principles`），留待独立评估。
- 保留 `.pi/` 用于 pi 专属的 prompts、subagents 等配置，不再把通用 skill 作为 `.pi/skills` 的真实文件维护。
- 为 pi 提供兼容加载入口，确保迁移前后现有 skill 名称和调用方式不失效。
- 更新仓库说明、外部源登记和 OpenSpec 记录，明确 `.agents/skills` 为仓库级跨 Agent skill 的事实来源。

## Capabilities

### New Capabilities

- `repository-agent-skills`: 提供随 Git 版本化、可供多个 Agent 发现和复用的仓库级 skill 目录，并保证现有 pi 调用兼容。

### Modified Capabilities

（无）

## Impact

- 文件结构：新增 `.agents/skills/`，迁移 `.pi/skills/` 下的 OpenSpec skill。
- Agent 配置：可能新增兼容符号链接或其他入口，具体按 pi 与仓库现有加载规则确定。
- 文档：更新 `AGENTS.md`、`docs/external-sources.md` 或相关维护说明。
- OpenSpec：引入/同步 `article-note` 相关规划产物；不改变后端 API、前端运行时、端口或业务数据。
- 兼容性：任何依赖 `.pi/skills` 路径的现有调用必须继续可用，迁移应可回滚。
