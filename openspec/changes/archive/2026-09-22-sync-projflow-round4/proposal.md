# Proposal: sync-projflow-round4（pick 上游侧边栏折叠持久化、紧凑折叠尺寸与强调色切换）

## Why

ProjFlow 新增了两组已提交的 `[shared]` 前端能力，本仓库尚未同步：主侧边栏刷新后会恢复展开且折叠占位偏宽；全站主色固定为靛蓝，用户不能切换。两组能力都属于共享脚手架层，应从上游同步，避免下游继续维护分叉实现。

## What Changes

从 ProjFlow 按依赖顺序同步：

1. `8b54bab`：主侧边栏折叠状态持久化 + 首次默认折叠
   - 新增 `web/src/config/layout.js`，提供下游可覆盖的 `SIDEBAR_DEFAULT_COLLAPSED`
   - `MainLayout.vue` 从独立 localStorage key 恢复折叠状态，用户手动收展后写回；存储不可用时降级到配置默认值
2. `0799f7e`：折叠态尺寸收缩 + 强调色切换
   - 主侧边栏折叠宽度 `64 → 56px`、菜单图标 `22 → 18px`
   - 文档页左右折叠边条 `28 → 20px`，竖排标签字号与字距同步收紧
   - 新增 `web/src/config/theme.js`：8 组 light/dark 强调色及派生函数
   - `stores/theme.js` 增加强调色状态、CSS 变量注入与跨会话持久化
   - `App.vue` 的 Naive UI `themeOverrides` 改为随强调色与明暗模式计算
   - `MainLayout.vue` 顶栏增加调色盘入口与当前色标识

**下游适配（不照抄上游项目身份）**：

- 保留产品名 `Digital Human` 与既有领域菜单、`HIDDEN_KEYS` 过滤逻辑
- 主题存储键沿用下游命名空间：`digital-human-theme`；新增 `digital-human-accent`，不引入 `projflow-*`
- 侧边栏折叠使用共享键 `app.sidebar-collapsed`（与上游一致，且与文档页 `doc-page.*` 键隔离）
- `SIDEBAR_DEFAULT_COLLAPSED` 下游先沿用上游默认值 `true`；用户本地已有偏好时以偏好为准
- 不同步 ProjFlow 当前未提交的 `add-gray-accent` 工作树改动；本轮强调色仍为已提交的 8 色
- 不携带上游 change 目录；在本 change 内维护 specs、设计、任务与验证记录

## Capabilities

### New Capabilities

- `sidebar-collapse`: 主侧边栏折叠偏好的持久化、默认值配置、存储异常降级与紧凑尺寸契约。
- `theme-accent`: 全站强调色预设、明暗模式变体、Naive UI/CSS 同源渲染、顶栏入口与持久化契约。

### Modified Capabilities

- `docs-page-layout`: 文档页左右面板折叠态边条由 28px 收紧至不超过 20px，并保证展开把手和竖排标签可用。

## Impact

- 前端：`web/src/App.vue`、`web/src/layouts/MainLayout.vue`、`web/src/stores/theme.js`、`web/src/views/management/DocPage.vue`
- 新增配置：`web/src/config/layout.js`、`web/src/config/theme.js`
- 浏览器状态：新增 `app.sidebar-collapsed`、`digital-human-accent`；既有 `digital-human-theme` 不迁移、不丢失
- Specs：新增 `sidebar-collapse`、`theme-accent`，修改 `docs-page-layout`
- 不影响：后端/API、领域数据、管理菜单可见性、端口、文档正文
- 上游来源：ProjFlow `8b54bab` → `0799f7e`；最终归档状态参考 `b167cd6`
