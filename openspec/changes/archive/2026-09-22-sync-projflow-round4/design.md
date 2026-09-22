# Design: sync-projflow-round4

## Context

- 上游功能来自两个有依赖关系的 `[shared]` commit：`8b54bab`（折叠状态底座）→ `0799f7e`（尺寸收缩 + 强调色）。`0799f7e` 的 `MainLayout.vue` 已假设 `web/src/config/layout.js` 存在，不能单独 pick。
- 本仓库与上游共享 App / theme store / MainLayout / DocPage 骨架，但有三处下游差异必须保留：产品名 `Digital Human`、领域菜单与 `HIDDEN_KEYS`、主题存储键 `digital-human-theme`。
- 上游当前工作树还有未提交的 `add-gray-accent`（`web/src/config/theme.js` 已脏），它不属于任何已提交 `[shared]` commit，本轮不得混入。
- 上游 `b167cd6` 已把相关 changes 归档并同步主 specs；本仓库需在自己的 change 内引入同等 specs，而不是复制上游 archive 目录。

## Goals / Non-Goals

**Goals：**

- 同步主侧边栏折叠偏好、首次默认折叠和紧凑折叠尺寸。
- 同步 8 色强调色切换，让 Naive UI 与 CSS 变量同源且跨会话保留。
- 同步文档页左右边条 20px 收缩，不破坏把手和竖排标签。
- 保留 Digital Human 的项目身份与领域定制。

**Non-Goals：**

- 不同步上游未提交的灰色强调色。
- 不替换本仓库整份 MainLayout / DocPage（会吞掉领域菜单、隐藏逻辑与 sidecar/滚动恢复等下游增量）。
- 不改后端、API、领域数据与端口。
- 不引入新的前端依赖。

## Decisions

### D1：选择性移植文件与代码块，不裸 cherry-pick 两个提交

上游 commit 同时包含 change artifacts 和共享前端；且本仓库对应文件已分叉。实施时：

- **整文件取上游最终版后做下游键名适配**：`web/src/config/layout.js`、`web/src/config/theme.js`（新增文件，跨库通用）
- **按代码块合并**：`App.vue`、`stores/theme.js`、`MainLayout.vue`、`DocPage.vue`
- **不取**：上游 `openspec/changes/**`，本 change 自己维护 specs/tasks

备选「依次 cherry-pick 8b54bab、0799f7e 再解冲突」会先引入上游 change 目录并删除/重命名其中一部分，噪音大且容易误带 ProjFlow 身份；不采用。

### D2：存储键分层

| 状态 | 键 | 理由 |
|---|---|---|
| 明暗主题 | `digital-human-theme` | 既有下游键，必须保持兼容 |
| 强调色 | `digital-human-accent` | 新增下游命名空间，避免 `projflow-accent` 泄漏 |
| 主侧边栏折叠 | `app.sidebar-collapsed` | 跨项目 UI 偏好，沿用上游共享键 |
| 文档页两栏 | `doc-page.sidebar-collapsed` / `doc-page.toc-collapsed` | 既有独立键，不改 |

localStorage 读写全部 try/catch；无记录时采用默认值，异常时不白屏。

### D3：侧边栏首次默认折叠沿用上游 `true`

`SIDEBAR_DEFAULT_COLLAPSED = true`。首次访问节省正文空间；用户手动展开后写入偏好，以后不受默认值影响；删除键即可回默认。若实测影响发现性，可只改下游配置为 `false`，不动组件。

### D4：主题颜色只有一个事实来源

`web/src/config/theme.js` 的 `ACCENTS` 是唯一色值源：

- `App.vue` 用 `accentThemeOverrides()` 生成 Naive UI primary 系列
- theme store 用 `accentFor()` / `toRgba()` 写 `--color-primary/-soft/--color-selected`
- MainLayout 色块也直接读取 `ACCENTS`

不在组件或 SCSS 中复制色值；默认 indigo 的 light 值 `#4f46e5` 与改造前一致，未选择颜色时视觉零变化。

### D5：MainLayout 与 DocPage 只合并目标差异

MainLayout 保留：`Digital Human` logo、领域菜单、`visibleMenuOptions`/`HIDDEN_KEYS`、breadcrumb 和全部路由判断；只加入：折叠持久化、56/18 尺寸、调色盘组件与样式。

DocPage 保留：sidecar UI、滚动位置恢复、子目录折叠与当前 responsive 规则；只改：左右 collapsed width 28→20、竖排标签 11/2→10/1。

## Risks / Trade-offs

- [Risk] 上游 theme store 使用 `projflow-*`，直接覆盖会丢失本地下游主题偏好 → 保留 `digital-human-theme`，新增 `digital-human-accent`。
- [Risk] MainLayout 整文件覆盖会吞领域菜单与 HIDDEN_KEYS → 仅合并目标代码块，并用菜单文案/路径快照核对。
- [Risk] DocPage 覆盖会吞 sidecar/滚动恢复 → 仅改 4 个 CSS 数值，diff 必须限制在对应选择器。
- [Risk] 默认折叠降低首次菜单发现性 → 配置独立，必要时下游切 `false`；用户偏好优先。
- [Risk] 未提交灰色强调色混入 → 所有来源固定到 commit `0799f7e`/`b167cd6`，不从上游工作树复制。
- [Risk] 当前上游 change 已归档，而本仓库主 specs 未含能力 → 本 change 建 delta specs，实施完成后归档同步。

## Migration Plan

1. 按 `8b54bab → 0799f7e` 的最终状态实现共享行为；应用下游键名与身份适配。
2. 构建、浏览器验证折叠/强调色/文档边条及 localStorage 隔离。
3. 比对上游最终功能块，残余差异只能是下游身份、菜单、键名和既有增量。
4. 归档 change，将 `sidebar-collapse`、`theme-accent` 和更新后的 `docs-page-layout` 同步到主 specs。

回滚：删除新增 config、恢复四个 Vue/JS 文件到实施前版本；localStorage 多出的键不会影响旧版本，可选清理。
