# Design: sync-projflow-round5

## Context

- 本仓库在 `d6b6280` 已选择性同步 ProjFlow 的强调色系统，但当时上游 `add-gray-accent` 仍是未提交工作树，故明确排除。
- 上游现在已正式提交完整依赖链：`2fbb3a6` 增加枪灰 → `888ef3f` 将其变为默认及无 JS CSS 兜底 → `1341f31` 使用默认色与现有 accent API 驱动 favicon。
- 当前 Digital Human 的 JS 默认值为 indigo；`index.scss` / `variables.scss` 无 JS 令牌为 indigo，`public/favicon.svg` 是历史紫色，三者彼此不一致。
- 当前主题 state 已使用下游键 `digital-human-theme`、`digital-human-accent`；MainLayout 已有主题色 popover，须合并 favicon UI 而不丢领域菜单、HIDDEN_KEYS 和侧栏持久化。

## Goals / Non-Goals

**Goals：**

- 将默认强调色、静态 CSS 令牌与静态 favicon 收敛到枪灰。
- 添加 6 个固定 favicon 形状，随 accent/mode 更新并持久化用户选择。
- 保持旧的有效用户强调色选择；只对没有记录的首次访问应用新默认。
- 保持下游身份与储存键命名空间。

**Non-Goals：**

- 不允许上传或编辑自定义 favicon/SVG。
- 不同步上游 OpenSpec history，也不直接覆写 MainLayout / theme store 整文件。
- 不改变 `index.html` 的 favicon link 结构；其静态 SVG 始终作为 JS 未加载的回退。
- 不逐页清理其他硬编码主题色；只处理全局令牌和现有主题控制链。

## Decisions

### D1：整条依赖链一起移植

取 `2fbb3a6 → 888ef3f → 1341f31`。favicon 静态回退必须与默认 accent 一致，不能只 pick 末端；而 default gray 若无 CSS 兜底又会在 JS 启动前闪出靛蓝。备选「只移植 favicon 并保留 indigo 默认」会需要重写上游 spec 的静态一致性契约，不采用。

### D2：持久化兼容与下游键名

| 状态 | 键 | 规则 |
|---|---|---|
| 明暗主题 | `digital-human-theme` | 保持不变 |
| 强调色 | `digital-human-accent` | 保持不变；有效旧值优先 |
| favicon 形状 | `digital-human-favicon` | 新增；未知/不可读回落 `bolt` |

不清理任何旧 accent：`readAccent()` 继续以预设白名单校验，indigo 等旧值仍有效。localStorage 的所有访问保持 try/catch。

### D3：favicon 生成、预览与安全边界

新增 `config/favicon.js`：固定的几何 SVG 字符串模板以 `readableOn(bg)` 选择前景色；同一 `faviconSvg()` 同时用于安全的代码生成预览和 data URL favicon。没有用户输入拼进 SVG，`v-html` 只渲染受控模板输出。store 在 `init`、`toggle`、`setAccent`、`setFavicon` 后都更新 `<link rel="icon">`。

### D4：局部合并而非裸 cherry-pick

- 整文件来源于 `1341f31`：`config/favicon.js`；静态 `favicon.svg` 采用同一 bolt/gray 内容。
- 手工合并：theme config/store、MainLayout、Sass 两文件。
- 不取：上游 `openspec/changes/**`。

MainLayout 只将现有 color popover 扩展为两节；必须保留 Digital Human logo、领域路由/menu、HIDDEN_KEYS、侧栏折叠状态和 breadcrumb。

### D5：静态 CSS 令牌与 runtime 注入的职责

`variables.scss` / `index.scss` 是 JS 执行前的枪灰安全默认值；theme store 在初始化与任何切换后，以 CSS 自定义属性覆盖它们。Markdown blockquote 改为 `var(--color-primary)`，确保已切换 accent 时也同步，不再锁定 Sass 编译期默认。

## Risks / Trade-offs

- [旧用户偏好被默认枪灰覆盖] → 仅无值或无效值回落默认，已有 indigo 等合法值保留。
- [data URL favicon 在旧浏览器失效] → `index.html` 保持静态 SVG link，最差降级为默认枪灰闪电。
- [MainLayout 合并吞掉下游菜单逻辑] → 仅替换 popover 区与相邻 imports/styles；用静态检查验证 `HIDDEN_KEYS`、领域路径和 Digital Human 标识存在。
- [主题面板 `v-html` 引入注入] → SVG 内容仅来自本地常量和受控 hex 色表，无用户文本输入。
- [浏览器 favicon 缓存] → data URL 的内容随状态变化，运行时不复用静态路径；无 JS 静态图标可被旧缓存短暂保留，属浏览器缓存行为。

## Migration Plan

1. 从固定 SHA 合并整条上游链，按下游键名调整。
2. 构建，并验证静态兜底、accent/mode/shape 切换、刷新恢复、无效 key 回退和菜单未回退。
3. 同步 `theme-accent` 与新增 `theme-favicon` 主 specs，再归档本 change。

回滚：revert 实现 commit；`digital-human-favicon` 残留键将被旧版本忽略，新版本会校验回退。
