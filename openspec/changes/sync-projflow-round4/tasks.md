## 1. 上游来源与配置底座

- [ ] 1.1 固定上游来源：仅使用 ProjFlow `8b54bab → 0799f7e` / `b167cd6` 的已提交文件；确认不从其含 `add-gray-accent` 的脏工作树取文件
- [ ] 1.2 新增 `web/src/config/layout.js`：`SIDEBAR_DEFAULT_COLLAPSED = true`，保留“下游可覆盖”说明
- [ ] 1.3 新增 `web/src/config/theme.js`：从上游已提交版本移植 8 色 `ACCENTS`、默认色、颜色派生函数与 Naive UI theme override 函数；不带未提交灰色强调色

## 2. 主侧边栏折叠与强调色

- [ ] 2.1 `web/src/stores/theme.js`：保留 `digital-human-theme`，增加 `digital-human-accent`；实现强调色恢复、`setAccent`、明暗切换时 CSS 变量同步与 localStorage 异常降级
- [ ] 2.2 `web/src/App.vue`：Naive UI themeOverrides 改为强调色 + 明暗模式的 computed 值，保留圆角与现有主题 provider 嵌套
- [ ] 2.3 `web/src/layouts/MainLayout.vue`：实现主侧边栏折叠状态读写 `app.sidebar-collapsed`（默认值取 layout config）；折叠宽度/图标改 56/18；保留 Digital Human logo、菜单、HIDDEN_KEYS、breadcrumb 和路由逻辑
- [ ] 2.4 `web/src/layouts/MainLayout.vue`：在明暗按钮旁加入调色盘入口、8 色网格与当前项标记；色块与 Naive UI/CSS 变量共用 `config/theme.js`

## 3. 文档页紧凑折叠态

- [ ] 3.1 `web/src/views/management/DocPage.vue`：仅将左右 `.collapsed` 宽度 28→20、竖排标签字号 11→10、字距 2→1；保留 sidecar、滚动恢复、子目录折叠与断点逻辑
- [ ] 3.2 核对折叠态宽度、展开把手命中区域与竖排标签不裁切，满足 `docs-page-layout` delta

## 4. 验证

- [ ] 4.1 `npm run build`（`web/`）通过
- [ ] 4.2 静态核对：MainLayout 仍保留 Digital Human 标识、领域菜单路径与 `HIDDEN_KEYS`；DocPage 除目标 CSS 数值外没有丢失下游 sidecar/滚动恢复逻辑
- [ ] 4.3 浏览器：清除 `app.sidebar-collapsed` 后首次默认折叠；展开/折叠后刷新均保留；清除键后回默认；localStorage 键不干扰 `doc-page.sidebar-collapsed` / `doc-page.toc-collapsed`
- [ ] 4.4 浏览器：折叠侧边栏宽约 56px、图标约 18px；文档页双边条宽不超过 20px、标签完整、把手可展开；窄屏断点不出现把手
- [ ] 4.5 浏览器：切换至少两种强调色和明暗模式；Naive UI 按钮与自定义菜单/文档选中态同色；刷新后强调色保留；默认靛蓝视觉与改造前一致
- [ ] 4.6 localStorage 异常冒烟：模拟或代码审查确认读写均 try/catch，页面可按默认状态渲染
- [ ] 4.7 `openspec validate sync-projflow-round4 --strict` 通过

## 5. 提交与归档

- [ ] 5.1 提交（`[shared] feat: sync ProjFlow 侧边栏折叠、紧凑尺寸与强调色切换`），正文注明来源 `8b54bab → 0799f7e`
- [ ] 5.2 归档 change，同步 `sidebar-collapse`、`theme-accent` 和 `docs-page-layout` delta 到主 specs
