## 1. 固定上游输入与枪灰主题底座

- [x] 1.1 固定来源只为 ProjFlow 已提交 `2fbb3a6 → 888ef3f → 1341f31`；不从上游工作树读取文件，也不携带其 `openspec/changes/**`
- [x] 1.2 `web/src/config/theme.js`：增加 `gray`（枪灰）预设，并将 `DEFAULT_ACCENT` 改为 `gray`
- [x] 1.3 `web/src/styles/variables.scss` 与 `web/src/styles/index.scss`：将无 JS 的主色、hover/pressed 派生色、selected/soft 令牌改为与枪灰默认值同源；Markdown blockquote 改用 runtime `var(--color-primary)`
- [x] 1.4 验证现有 `digital-human-accent` 中合法的 indigo 等值仍优先于新枪灰默认，不做 localStorage 迁移或清理

## 2. favicon 配置、状态与静态兜底

- [x] 2.1 新增 `web/src/config/favicon.js`：6 个固定形状、默认 `bolt`、形状白名单校验、基于 `readableOn` 的 SVG 与 data URL 生成函数
- [x] 2.2 `web/src/stores/theme.js`：新增下游键 `digital-human-favicon`、读取校验、形状状态和 setter；在 init/toggle/setAccent/setFavicon 后用当前 accent/mode 更新 `<link rel="icon">`
- [x] 2.3 `web/public/favicon.svg`：替换历史紫色资产为枪灰底白色闪电，精确对应默认静态兜底

## 3. 主题面板集成

- [x] 3.1 `web/src/layouts/MainLayout.vue`：将现有主题色弹层扩展为「主题色」和「图标」两节，渲染 6 个受控 SVG 预览、当前形状标记和选择操作
- [x] 3.2 保留 Digital Human 标识、领域菜单路径、`HIDDEN_KEYS`、侧栏折叠持久化、breadcrumbs 和主题明暗切换；只合并目标 imports/template/styles

## 4. 验证

- [x] 4.1 `npm run build`（`web/`）通过，且 `git diff --check` 无错误
- [x] 4.2 静态检查：不存在 `projflow-theme` / `projflow-accent` / `projflow-favicon`；下游三类键、6 个形状、gray 预设和 6 个主题色块均可见
- [x] 4.3 浏览器：清除 accent 偏好后首次为枪灰；写入合法 indigo 后仍使用 indigo；选择青色后 Naive UI/CSS 变量、favicon data URL 同步更新
- [x] 4.4 浏览器：切换深色模式后 favicon 使用 accent.dark；选择至少两个形状并刷新，形状和颜色均保留；写入未知 favicon key 后回落 bolt
- [x] 4.5 浏览器：主题面板显示两节、6 个图标预览和当前选中态；静态 `/favicon.svg` 是枪灰闪电；领域菜单、HIDDEN_KEYS 和侧栏折叠行为仍在
- [x] 4.6 `openspec validate sync-projflow-round5 --strict` 通过

## 5. 提交与归档

- [ ] 5.1 提交 `[shared] feat: sync ProjFlow 枪灰默认主题与主题 favicon`，注明来源 `2fbb3a6 → 888ef3f → 1341f31`
- [ ] 5.2 同步 `theme-accent` 和 `theme-favicon` 主 specs 并归档 change
