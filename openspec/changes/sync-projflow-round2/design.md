# Design: sync-projflow-round2

## Context

- 上游新增：`afea6a3`（scrollMemory + DocPage 接入）；`db9fdf8`（技能目录迁到 `.agents/skills`）
- 上游已 pick 我们的修复：`c47d588`（中文/Unicode slug）
- 我们的独有改动：`MarkdownRenderer.handleClick` 的文内锚点接管
- 本地 DocPage 与上游差异约 37 行（我们已有 sidecar / 侧栏收起 / 子目录折叠）

## Goals / Non-Goals

**Goals：** 把上游的滚动位置恢复合并进来，且不破坏我们已有的定制（侧栏收起、sidecar、锚点接管、HIDDEN_KEYS）。
**Non-Goals：** 不做 `.agents/skills` 目录迁移（本仓库没有仓库级技能）；不改动上一轮已合并的文档系统能力。

## Decisions

- **D1 按上游文件移植**：直接取上游 `web/src/utils/scrollMemory.js`，`DocPage.vue` 按上游接入点手工合并（我们的定制点保留）。理由：文件小、耦合低；cherry-pick 会因我们的改名/定制冲突。
- **D2 锚点与滚动恢复共存**：滚动恢复只在**文档 slug 变化或首次加载**时写入/读取；锚点跳转与 TOC 跳转仍走各自的 `scrollIntoView`，互不覆盖。
- **D3 `.agents/skills` 不迁移**：本仓库无仓库级技能目录，写作规范在用户级；迁移没有收益，记录原因即可。
- **D4 回灌候选登记**：文内锚点接管按 `[shared]` 记入 `docs/external-sources.md`，并在上游侧实现后回填状态。

## Risks / Trade-offs

- [滚动恢复与锚点跳转互相覆盖] → 恢复只在文档切换后执行一次；锚点跳转不写记忆
- [与本地定制冲突] → 合并后在浏览器里逐项验收：滚动恢复、锚点跳转、侧栏收起、sidecar、HIDDEN_KEYS
- [上游仍在演进] → 记录对照基准为本轮上游 HEAD

## Migration Plan

1. 取上游 `scrollMemory.js` → 合并 `DocPage.vue` 接入
2. 构建 + 浏览器验收（刷新恢复 / 切换恢复 / 锚点仍可用）
3. 更新 `docs/external-sources.md`（slug 回灌完成、锚点回灌新增）
4. 回滚 = 去掉 `scrollMemory` 接入

## Open Questions

- 上游是否也想要文内锚点接管？（回灌后由上游决定）
