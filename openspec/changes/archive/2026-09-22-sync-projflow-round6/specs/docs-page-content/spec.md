## MODIFIED Requirements

### Requirement: 文档元数据存于同名 sidecar json

每篇文档（`<slug>.md`）SHALL 支持同名 sidecar json（`<slug>.json`）承载元数据：`changelog`（演进：日期 + 一句话 + commit）、`progress`（进度）、`appendix`（附录设计说明）、`related`（相关文档）；详情接口 SHALL 一并返回。这些元数据 SHALL NOT 出现在正文章节与章节列表中。文档页的统一取数层 SHALL 在开发模式从详情接口取得这些字段，在生产静态构建中从构建期生成的同等详情数据取得这些字段；两种来源的页面渲染契约必须一致。

#### Scenario: 更新演进记录
- **WHEN** 某文档发生一次值得记录的演进
- **THEN** 只更新 `<slug>.json` 的 `changelog`，正文不变、不触发章节重排

#### Scenario: 静态构建保留 sidecar
- **WHEN** 某文档存在同名 sidecar 且前端生产构建完成
- **THEN** 静态详情数据包含该 sidecar，文档页仍可渲染相同的演进、进度、相关文档与附录区块

### Requirement: 不影响既有链接行为

接管文内锚点 SHALL NOT 影响三类既有链接：跨文档链接（`[[slug|显示名]]` 与 `/management/docs/...`）、外部链接（`https://...`）、以及右侧 TOC 的滚动行为。文档正文按 `/api/management/docs-assets/<slug>/<file>` 约定引用的图片，在开发模式 SHALL 保持通过该 API 路径加载；生产静态构建 SHALL 在保持源 Markdown 不变的前提下，将该前缀解析为当前部署基路径下的静态资产，使图片链接同样可用。

#### Scenario: 三类链接照常
- **WHEN** 正文同时含跨文档链接、外部链接与文内锚点链接
- **THEN** 前两类按原行为工作（站内路由跳转 / 新链接触发），文内锚点平滑滚动，右侧 TOC 点击仍平滑滚动

#### Scenario: 静态托管下文档图片可用
- **WHEN** 静态部署的文档正文包含 `/api/management/docs-assets/<slug>/<file>` 图片链接
- **THEN** 页面从当前部署基路径下的静态文档资产加载图片，源 Markdown 文件没有被改写
