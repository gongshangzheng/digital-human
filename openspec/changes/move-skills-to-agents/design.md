## Context

- 当前仓库级 skill 的真实文件在 `.pi/skills/`，共 6 个 OpenSpec skill（apply / archive / explore / propose / sync-specs / update-change），已被 Git 跟踪。
- `.pi/` 下另有 pi 专属的 `prompts/` 与 `subagents/` 目录，与 skill 无关，不应随迁移改动。
- pi 的项目级 skill 发现路径包含 `.pi/skills/` 与 `.agents/skills/`（cwd 及祖先目录，截至 git 仓库根）；`.agents/skills/` 中只识别含 `SKILL.md` 的子目录，根级 `.md` 被忽略。
- 上游 ProjFlow 已将共享 skill 迁至 `.agents/skills/`（`db9fdf8`），并以 `.claude/skills -> ../.agents/skills` 符号链接兼容 Claude Code；最新提交 `4ff70a0` 新增 `article-note` skill。
- 本机 `~/.pi/agent/skills/openspec-*` 是用户级符号链接，指向另一个仓库的副本，与本次仓库级迁移叠加后存在同名 skill。pi 对同名 skill 的处理是「警告并保留先发现的」。
- `article-note` 上游写入路径为 `management/docs/notes/`，本仓库的论文笔记目录是 `management/docs/论文笔记/`，需要适配。

## Goals / Non-Goals

**Goals：**

- 让 `.agents/skills/` 成为本仓库共享 skill 的单一事实来源，且 pi 与其他 Agent 都能发现。
- 迁移现有 OpenSpec skill 且不改变其名称、入口与工作流语义。
- 从上游接入 `article-note`，并适配本仓库的论文笔记目录与 OpenSpec 流程约定。
- 保留 `.pi/` 作为 pi 专属配置目录。

**Non-Goals：**

- 不迁移到用户级 `~/.pi/agent/skills/`，也不清理用户级同名链接（本机全局状态，另行处理）。
- 不采纳上游与本仓库无关的业务 skill（`management`、`papers`、`evaluation`、`web`、`design-principles`）。
- 不改动后端 API、前端运行时、端口、业务数据。
- 不改动 `.pi/prompts/`、`.pi/subagents/` 的内容。

## Decisions

### D1：以 `.agents/skills/` 为单一事实来源（`git mv`，非复制）

把 `.pi/skills/openspec-*` 用 `git mv` 迁到 `.agents/skills/openspec-*`，保留 Git 历史。pi 原生发现项目 `.agents/skills/`，因此**不需要**为了 pi 保留 `.pi/skills` 副本。

- 备选一：复制到两处并存 —— 会产生双份漂移，且同名 skill 触发 pi 的冲突告警，不采用。
- 备选二：保留 `.pi/skills` 真实文件、`.agents/skills` 做符号链接 —— 与「跨 Agent 事实来源」的意图相反，且 pi 的 `.agents/skills` 只认子目录内的 `SKILL.md`，符号链接目录虽可用但语义更绕，不采用。

### D2：pi 专属配置留在 `.pi/`

`.pi/prompts/`、`.pi/subagents/` 不动；迁移后 `.pi/` 不再持有通用 skill 真实文件。若将来 pi 需要额外加载路径（如复用他仓 skill），通过 `.pi/settings.json` 的 `skills` 数组声明，而不是把文件搬进 `.pi/skills`。

### D3：新增 `.claude/skills -> ../.agents/skills` 符号链接

对齐上游做法，让 Claude Code 及读取 `.claude/skills` 的 Agent 复用同一份 skill，无需二次维护。

- 备选：在 `.pi/settings.json` 里加 `"skills": ["../.claude/skills"]` —— 方向相反（让 pi 去读 Claude 的目录），在本仓库不需要，不采用。

### D4：上游 skill 只接入 `article-note`，其余记为后续独立变更

本变更只从上游接入 `article-note`（与本仓库「论文笔记」工作直接相关）。

- `doc-writing`、`upstream-sync` 等上游共享 skill 与本仓库现有流程可能重叠，需要单独评估，**不在本变更内**。
- `management`、`papers`、`evaluation`、`web`、`design-principles` 属上游业务 skill，不引入。

### D5：`article-note` 按本仓库路径与流程适配

保留其门禁结构（素材 → 分析 → 结构审批 → 写入），但将产出目录改为本仓库的 `management/docs/论文笔记/`，并使其引用的 OpenSpec 步骤与本仓库 `openspec/changes/` 约定一致。不做「原样照抄」。

## Risks / Trade-offs

- [用户级同名 skill 遮蔽] `~/.pi/agent/skills/openspec-*` 与仓库级 `.agents/skills/openspec-*` 同名，pi 只保留先发现的一个并告警 → 缓解：以仓库级为权威，记录该全局链接为待清理项；本变更内先验证仓库级 skill 内容与调用语义正确。
- [迁移后 skill 不被发现] 若 pi 未信任项目或未扫描 `.agents/skills` 子目录 → 缓解：迁移后实测 6 个 skill 均可被列出并调用，且在 `.agents/skills` 下只放含 `SKILL.md` 的子目录，不放根级 `.md`。
- [上游 `article-note` 与本仓库目录/流程不匹配] 直接照抄会写到错误目录 → 缓解：D5 显式适配并在任务中列验收项。
- [符号链接在部分平台的兼容性] `.claude/skills` 用相对符号链接 → 缓解：沿用上游同款相对链接 `../.agents/skills`，并实测可解析。

## Migration Plan

1. `git mv` 六个 OpenSpec skill 到 `.agents/skills/`。
2. 新增 `.claude/skills -> ../.agents/skills` 符号链接。
3. 从上游引入 `article-note` 到 `.agents/skills/article-note/` 并适配。
4. 更新 `AGENTS.md` / `docs/external-sources.md` 的 skill 目录与同步记录（含撤回上一轮「`.agents/skills` 不采纳」的结论）。
5. 校验：列出并调用 skill、`openspec validate move-skills-to-agents --strict`。

回滚：`git mv` 反向操作恢复 `.pi/skills/`，删除 `.agents/` 与 `.claude/skills` 符号链接即可，无数据或运行时副作用。

## Open Questions

- 是否在后续单独清理用户级 `~/.pi/agent/skills/openspec-*` 符号链接，以彻底消除同名遮蔽？（不影响本变更的 specs、方案与任务拆分。）
