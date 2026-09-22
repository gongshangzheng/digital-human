# docs-page-content（文档页内容契约）

## Purpose

定义文档详情接口与正文渲染的内容侧契约：中文（Unicode）文件名文档必须可访问；文档元数据走同名 sidecar json 并按规定布局渲染；章节列表对 Markdown 强调符号做处理。
## Requirements
### Requirement: 中文（Unicode）文件名文档可访问

文档详情接口 SHALL 接受包含 Unicode 字符（含中文、空格）的 slug，并能正确解析到对应 `.md` 文件。slug 校验 MUST NOT 仅允许 ASCII 字符集。

#### Scenario: 打开中文名文档
- **WHEN** 请求 `GET /api/management/docs/knowledge/数字人基础`
- **THEN** 返回 200 与该文档内容（title/content 与文件一致）
- **WHEN** 请求 `GET /api/management/docs/实习复盘/数字人介绍与技术路线`
- **THEN** 返回 200 与正文内容

#### Scenario: 路径穿越仍被拒绝
- **WHEN** slug 含 `..` 或超出文档根目录的路径
- **THEN** 返回 400 或 404，不读取根目录外文件

### Requirement: 文档元数据存于同名 sidecar json

每篇文档（`<slug>.md`）SHALL 支持同名 sidecar json（`<slug>.json`）承载元数据：`changelog`（演进：日期 + 一句话 + commit）、`progress`（进度）、`appendix`（附录设计说明）、`related`（相关文档）；详情接口 SHALL 一并返回。这些元数据 SHALL NOT 出现在正文章节与章节列表中。

#### Scenario: 更新演进记录
- **WHEN** 某文档发生一次值得记录的演进
- **THEN** 只更新 `<slug>.json` 的 `changelog`，正文不变、不触发章节重排

### Requirement: 元数据的渲染布局

文档页 SHALL 在文章顶部提供按钮展示演进记录与进度（点击弹层），在文章底部以独立块渲染相关文档与附录；无对应字段的文档 MUST NOT 渲染空块。

#### Scenario: 打开带完整 sidecar 的文档
- **WHEN** 读者打开某篇配有完整四字段 sidecar json 的文档
- **THEN** 顶部可见「演进记录」「进度」按钮，底部出现「相关文档」与「附录」独立块，正文不含这些内容

#### Scenario: 无 sidecar 的文档
- **WHEN** 某文档没有同名 json 或 json 为空
- **THEN** 不渲染顶部按钮与底部块，页面正常

### Requirement: 章节列表对标题强调符号的处理

文档页右侧章节列表 SHALL 对 Heading 中的 Markdown 强调符号（`**`）做处理——丢弃或渲染为强调；MUST NOT 原样显示符号字符。

#### Scenario: 标题含加粗
- **WHEN** 某标题为 `### §4.2 任务看板：**三段表结构**`
- **THEN** 章节列表显示「§4.2 任务看板：三段表结构」（符号丢弃）或同等强调渲染，且不出现 `**` 字符

### Requirement: 文内锚点链接与 TOC 行为一致

正文里 `href` 以 `#` 开头的链接 SHALL 由前端接管：点击时阻止默认跳转，按锚点 id 找到目标元素并平滑滚动到视口顶部；MUST NOT 修改浏览器 URL（不留 hash）。

#### Scenario: 点击文内锚点
- **WHEN** 文档正文含 `[CSIM 当损失函数（已放弃）](#csim-当损失函数已放弃)`，读者点击它
- **THEN** 页面平滑滚动到该小节标题处，URL 保持不变

#### Scenario: 锚点指向不存在的 id
- **WHEN** 链接的锚点在当前文档里不存在
- **THEN** 点击无任何副作用（不报错、不改 URL），页面不跳动

### Requirement: 不影响既有链接行为

接管文内锚点 SHALL NOT 影响三类既有链接：跨文档链接（`[[slug|显示名]]` 与 `/management/docs/...`）、外部链接（`https://...`）、以及右侧 TOC 的滚动行为。

#### Scenario: 三类链接照常
- **WHEN** 正文同时含跨文档链接、外部链接与文内锚点链接
- **THEN** 前两类按原行为工作（站内路由跳转 / 新链接触发），文内锚点平滑滚动，右侧 TOC 点击仍平滑滚动

### Requirement: 用 `order` 字段显式表达阅读顺序

文档 frontmatter SHALL 支持 `order` 字段（数字）。列表排序中 `order` 的优先级 SHALL 高于 `id`：`order` 越小越靠前。未写 `order` 的文档 SHALL 继续按 `id` 排序，行为与改动前一致。

#### Scenario: 两篇都写了 order
- **WHEN** `A.md` 写 `order: 1`、`B.md` 写 `order: 2`（其余字段相同）
- **THEN** 列表中 A 排在 B 之前

#### Scenario: 未写 order 时不改变现状
- **WHEN** 某文档没有 `order` 字段
- **THEN** 它仍按 `id` 升序参与排序（知识库 22 篇的顺序不变）

#### Scenario: order 非数字
- **WHEN** `order` 的值不是数字
- **THEN** 该字段被忽略，回退到 `id` → `date` 排序，不报错

### Requirement: 排序链最终必须确定（不得落到文件系统顺序）

当 `order`、`id`、`date` 都无法区分两篇文档时，系统 SHALL 以稳定且与文件系统无关的附加键（如 slug 字典序）作为最后一级，保证列表顺序确定、可复现。

#### Scenario: 全部排序键相同
- **WHEN** 两篇文档同 `date`、同 `id`、都无 `order`
- **THEN** 它们的先后由 slug 字典序决定，且重复请求结果一致

### Requirement: 文件夹在列表中的先后可配置

文档列表树中文件夹的先后 SHALL 由服务端配置的顺序决定（默认 `实习复盘 → 论文笔记 → knowledge`）；未列入配置的文件夹 SHALL 排在已配置的之后，并在其后按 `order` → `id` → `date` 排序。

#### Scenario: 默认顺序
- **WHEN** 文档树包含 `实习复盘/`、`论文笔记/`、`knowledge/` 三个文件夹
- **THEN** 列表中依次出现 实习复盘 → 论文笔记 → knowledge

#### Scenario: 未配置的文件夹
- **WHEN** 新增一个未列入配置的文件夹（如 `temp/`）
- **THEN** 它排在已配置文件夹之后，不报错

