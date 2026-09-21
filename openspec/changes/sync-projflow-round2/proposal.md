# Proposal: sync-projflow-round2（再同步上游 [shared] 更新 + 回灌候选）

## Why

上一轮同步后又过了一段时间，上游 ProjFlow 新增了一批 `[shared]` 改动，其中有一条直接影响文档阅读体验；同时**我们本地有一项上游没有的修复**（文内锚点接管），应当作为回灌候选登记。

## What Changes

**从上游 pick**：
- `afea6a3` **文档页滚动位置恢复**：新增 `web/src/utils/scrollMemory.js`，并在 `DocPage.vue` 接入（刷新 / 切换文档后恢复滚动位置）

**向upstream回灌（候选）**：
- 我们的 `MarkdownRenderer.handleClick` **文内锚点接管**（`#` 链接 → `preventDefault` + `getElementById` + `scrollIntoView`，不改 URL）——上游目前没有这段，锚点链接会走浏览器默认行为、改变 URL 且不平滑

**状态更新**：
- `c47d588` 显示**上游已 pick 我们的中文 slug 修复**（pick 自 digital-human `486c925`）→ `docs/external-sources.md` 的对应回灌待办可标记为已完成

**不采纳（记录原因）**：
- `db9fdf8` 把 skill 真实目录迁到 `.agents/skills`、`.claude/skills` 改符号链接：本仓库**没有仓库级技能目录**（写作规范在用户级 `~/.pi/agent/skills`），暂不适用；若将来把技能纳入仓库再对齐

## Capabilities

### New Capabilities
- `docs-page-scroll-memory`：文档页滚动位置在刷新/切换后恢复

### Modified Capabilities
（无）

## Impact
- 代码：新增 `web/src/utils/scrollMemory.js`；改 `web/src/views/management/DocPage.vue`
- 文档：`docs/external-sources.md` 回灌待办状态更新（slug 项完成、锚点项新增）
- 不影响：端口 8812/3212、身份命名、`order` 排序、HIDDEN_KEYS、sidecar 与锚点链接本体
