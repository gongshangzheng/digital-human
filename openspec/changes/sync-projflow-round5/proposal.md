# Proposal: sync-projflow-round5（pick 上游枪灰默认主题与主题联动 favicon）

## Why

上一轮已同步强调色切换，但 Digital Human 仍是靛蓝默认、无 JavaScript 时 CSS 令牌也固定靛蓝，浏览器标签页 favicon 更保留历史紫色。ProjFlow 随后将这三处收敛为「枪灰默认强调色 + 同源静态兜底 + 跟随主题的可选 favicon」，属于共享界面基础设施，应继续同步以避免两库主题契约分叉。

## What Changes

按上游依赖顺序同步以下已提交 `[shared]` commits：

1. `2fbb3a6`：为强调色预设加入 `gray`（枪灰）。
2. `888ef3f`：默认强调色改为枪灰，并让 Sass/CSS 的无 JS 令牌、Markdown 引用边框与默认值保持同源。
3. `1341f31`：新增 favicon 形状集合（闪电/脉冲/网格/层级/六边形/星芒）；图标的底色随当前强调色和明暗模式更新，形状选择持久化；主题面板展示主题色和图标两节；静态 `favicon.svg` 作为与默认值一致的无 JS 兜底。

**下游适配：**

- 保留 `Digital Human` 产品名、领域菜单、`HIDDEN_KEYS` 与既有路由/布局行为。
- 主题状态延续下游键：`digital-human-theme`、`digital-human-accent`；新增 `digital-human-favicon`，不带入 `projflow-*`。
- 完整取 `2fbb3a6 → 888ef3f → 1341f31` 链，默认枪灰与静态 favicon 一致；已有用户的有效强调色偏好（含 indigo）优先于新默认值，不做迁移或强制覆盖。
- favicon 图形只来自代码内固定模板；不新增上传、自定义 SVG 或用户提供的 HTML 注入入口。
- 不同步上游 change/archive 目录；在本仓库 change 内管理 artifacts 和 specs。

## Capabilities

### New Capabilities

- `theme-favicon`: 浏览器标签页图标随强调色、明暗模式和用户选择的固定图形形状更新，并在 JS 未执行时提供一致的静态兜底。

### Modified Capabilities

- `theme-accent`: 在现有可切换预设中增加枪灰，首次访问无强调色偏好时默认使用枪灰；Sass/CSS 无 JS 令牌须与此默认值一致。

## Impact

- 新增：`web/src/config/favicon.js`
- 更新：`web/src/config/theme.js`、`web/src/stores/theme.js`、`web/src/layouts/MainLayout.vue`、`web/src/styles/index.scss`、`web/src/styles/variables.scss`、`web/public/favicon.svg`
- 浏览器状态：新增 `digital-human-favicon`；保留的 `digital-human-accent` 值继续优先于默认值
- Specs：新增 `theme-favicon`，修改 `theme-accent`
- 不影响：后端/API、领域数据、管理菜单可见性、端口、文档内容
- 上游来源：ProjFlow `2fbb3a6 → 888ef3f → 1341f31`
