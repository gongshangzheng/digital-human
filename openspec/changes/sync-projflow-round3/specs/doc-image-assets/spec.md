# doc-image-assets（wiki 文档图片资产）

## Purpose

为 wiki 文档提供图片能力：约定图片存放位置、通过后端静态端点供图、在 Markdown 中以固定 URL 引用并渲染为语义化 figure，使论文精读笔记、架构文档等可正常配图。

> 移植自上游 ProjFlow `e505269`（wiki 文档图片支持），保持同等能力与引用约定。

## ADDED Requirements

### Requirement: 文档图片静态端点

后端 SHALL 把 `management/docs/_assets/` 挂载为只读静态目录并暴露于 `/api/management/docs-assets/`；该目录不存在时 SHALL 自动创建且不导致启动失败。

#### Scenario: 图片可访问
- **WHEN** `management/docs/_assets/<slug>/fig-1.webp` 存在
- **THEN** `GET /api/management/docs-assets/<slug>/fig-1.webp` 返回该图片，内容类型为 `image/webp`

#### Scenario: 目录为空或不存在
- **WHEN** `_assets/` 不存在或为空
- **THEN** 后端正常启动；访问不存在的图片返回 404，不返回目录列表

### Requirement: 图片存放约定

文档图片 SHALL 存放于 `management/docs/_assets/<slug>/`，其中 `<slug>` 与所属文档 slug 对齐；`_assets` 等下划线前缀目录 SHALL 不参与文档扫描（`GET /api/management/docs` 既排除其中的图片，也排除意外放入的 `.md`）。

#### Scenario: 图片不被识别为文档
- **WHEN** `_assets/` 下存在若干 `.webp` 文件
- **THEN** `GET /api/management/docs` 返回的文档列表中不包含这些文件

#### Scenario: 资产目录内误放的 markdown 也不入库
- **WHEN** `_assets/` 下存在一个 `.md` 文件（如误放的说明文档）
- **THEN** 文档列表不包含它；其它非下划线子目录（如 `论文笔记/`）中的文档仍正常收录

### Requirement: Markdown 引用使用绝对 URL

文档正文 SHALL 用绝对路径 `/api/management/docs-assets/<slug>/<file>` 引用图片，以保证在任意文档层级（含子目录）都能正确解析。

#### Scenario: 子目录文档中的图片
- **WHEN** 文档位于 `management/docs/论文笔记/<slug>.md` 并引用 `/api/management/docs-assets/<slug>/fig-1.webp`
- **THEN** 页面在 `/management/docs/论文笔记/<slug>` 路由下能正常加载该图片

### Requirement: 图片渲染为语义化 figure

Markdown 渲染 SHALL 把带 alt 文本的图片输出为 `<figure>` 结构：`<img>`（含 `loading="lazy"`）与 `<figcaption>`（内容为 alt 文本）；alt 为空时 SHALL 退化为裸 `<img>`。

#### Scenario: 带图题的图片
- **WHEN** 正文含 `![图 1 · 架构总览](/api/management/docs-assets/x/fig-1.webp)`
- **THEN** 渲染出 `<figure>`，其中 `figcaption` 文本为「图 1 · 架构总览」，`img` 带 `loading="lazy"`

#### Scenario: 行内小图标
- **WHEN** 正文含 `![](/api/management/docs-assets/x/icon.webp)`（无 alt）
- **THEN** 渲染为裸 `<img>`，不生成空的 `figcaption`

### Requirement: 图片自适应与图题样式

渲染后的图片 SHALL 自适应容器宽度（`max-width: 100%`），图题 SHALL 以区别于正文的小号弱色文本呈现。

#### Scenario: 窄屏适配
- **WHEN** 文档中含宽度大于容器的图片
- **THEN** 图片缩放至容器宽度内，不产生横向溢出

### Requirement: 不放开原始 HTML

渲染管线 SHALL 保持 `html: false`；图片仅能经由 Markdown 图片语法进入渲染，不得因本能力放开任意 HTML 注入。

#### Scenario: 内嵌 HTML 仍被转义
- **WHEN** 文档正文包含原始 `<img src=x onerror=...>` 字符串
- **THEN** 该字符串按文本渲染，不执行
