## Purpose

定义文档详情接口与正文渲染的内容侧契约：中文（Unicode）文件名文档必须可访问；文档元数据走同名 sidecar json 并按规定布局渲染；章节列表对 Markdown 强调符号做处理。

## ADDED Requirements

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
