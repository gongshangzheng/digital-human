## 1. 迁移现有 OpenSpec skill 到 `.agents/skills/`

- [x] 1.1 `git mv .pi/skills/openspec-apply-change .agents/skills/openspec-apply-change`（对其余 5 个 skill 同法处理：archive-change / explore / propose / sync-specs / update-change）
- [x] 1.2 确认 `.pi/skills/` 下不再保留通用 skill 真实文件；`.pi/prompts/`、`.pi/subagents/` 保持不动
- [x] 1.3 新增相对符号链接 `.claude/skills -> ../.agents/skills`
- [x] 1.4 实测 pi 能发现这 6 个 skill（列出可用 skill + 任选一个执行 `/skill:openspec-propose`），并确认无 `.agents/skills` 根级 `.md`

## 2. 接入并适配上游 `article-note`

- [x] 2.1 从上游 `4ff70a0` 取 `.agents/skills/article-note/` 到本仓库同路径
- [x] 2.2 适配产出目录：`management/docs/notes/` → 本仓库 `management/docs/论文笔记/`
- [x] 2.3 适配 OpenSpec 引用：使其步骤与本仓库 `openspec/changes/` 约定一致（propose → 审核 → apply）
- [x] 2.4 逐个检查其 `scripts/`（fetch-paper / figures / init-workspace / validate-* 等）在本仓库可运行或有明确前置说明
- [x] 2.5 记录 `article-note` 登记到 `docs/external-sources.md`（上游提交 `4ff70a0`）

## 3. 文档与登记更新

- [x] 3.1 更新 `AGENTS.md`：说明仓库级 skill 位于 `.agents/skills/`、pi 专属配置位于 `.pi/`
- [x] 3.2 `docs/external-sources.md`：撤回上一轮「`.agents/skills` 迁移不采纳」结论，改为「已采纳并适配」
- [x] 3.3 记录本变更的迁移映射表（旧 `.pi/skills/<name>` → 新 `.agents/skills/<name>`）

## 4. 校验与提交

- [x] 4.1 `openspec validate move-skills-to-agents --strict` 通过
- [x] 4.2 复核回滚路径可用（反向 `git mv` + 删除新增符号链接即可复原）
- [x] 4.3 提交（`chore: 迁移仓库级 skill 到 .agents/skills 并接入 article-note`）
