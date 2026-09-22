## Purpose

定义无 FastAPI 的静态托管环境中管理文档、sidecar 与文档图片的构建和读取契约，使文档页与其深链接可作为静态站点可靠浏览。

## ADDED Requirements

### Requirement: 构建期生成文档静态数据

构建流程 SHALL 扫描 `management/docs/` 下的 Markdown 与同名 sidecar JSON，产出前端可读取的静态数据；列表项 SHALL 包含 `slug`、`title`、`author`、`date`、`tags`、`summary`、`id` 与 `order`，详情项 SHALL 额外包含去除 frontmatter 的正文和 sidecar。扫描 SHALL 跳过下划线前缀目录，排序 SHALL 与后端文档接口一致：文件夹优先级、`order`、`id`、日期降序、slug 字典序。

#### Scenario: 生成文档列表与详情
- **WHEN** 执行生产构建
- **THEN** 产物含所有非资产 Markdown 的列表与按 slug 索引的详情，详情保留同名 sidecar 的内容

#### Scenario: 静态数据排序与后端一致
- **WHEN** 比较静态数据列表与 `GET /api/management/docs`
- **THEN** 两者按相同的文件夹优先级、`order`、`id`、日期和 slug 排序，缺失或非数字的 `order`、`id` 排在有效数字之后

#### Scenario: 资产目录不参与文档扫描
- **WHEN** `management/docs/_assets/` 下存在文件
- **THEN** 这些文件不出现在静态文档列表或详情中

### Requirement: 生产和开发使用适合的数据来源

文档页 SHALL 经统一取数层取得文档数据；开发模式 MUST 请求既有 FastAPI 文档接口，生产构建 MUST 读取构建产物中的静态数据。静态数据中不存在的 slug MUST 以与后端 404 等价的错误结束，页面不得崩溃。

#### Scenario: 本地开发读取实时文档
- **WHEN** 前端以开发模式运行且管理文档被修改
- **THEN** 刷新后的文档页从 FastAPI 获取更新后的列表和正文

#### Scenario: 静态托管读取构建快照
- **WHEN** 生产构建运行在没有 FastAPI 的静态托管环境
- **THEN** 文档列表和正文从静态数据加载并正常渲染

#### Scenario: 静态数据缺少目标文档
- **WHEN** 请求不在静态数据中的文档 slug
- **THEN** 取数层返回错误，由页面显示现有空态而不是抛出未处理异常

### Requirement: 文档图片随构建静态化

构建流程 SHALL 将 `management/docs/_assets/` 的非隐藏文件复制到前端可部署的静态资产目录，并在每次构建前清理旧目标，确保构建产物仅包含当前源资产。生产模式加载文档正文时 MUST 把 `/api/management/docs-assets/` 前缀改写为当前部署基路径下的静态资产前缀；开发模式与源 Markdown MUST 保持原 API 路径。

#### Scenario: 生产文档图片可见
- **WHEN** 文档正文以 `/api/management/docs-assets/<slug>/<file>` 引用图片且站点部署在子路径
- **THEN** 生产文档页从该子路径下的静态资产加载图片并正常显示

#### Scenario: 已删除图片不残留
- **WHEN** 某源图片被删除后再次执行生产构建
- **THEN** 对应静态资产不再存在于新的构建产物

#### Scenario: 开发模式不改写图片路径
- **WHEN** 前端以开发模式加载含文档图片的正文
- **THEN** 图片继续从 FastAPI 的 `/api/management/docs-assets/` 端点加载

### Requirement: 静态构建对不完整输入显式失败

当文档目录缺失、没有 Markdown、frontmatter 不可解析或 sidecar JSON 非法时，静态数据生成 SHALL 以非零状态退出并输出可定位的错误；MUST NOT 静默发布残缺文档数据。构建器支持单行标量与内联数组；实施 SHALL 将既有非关键文档 `management/docs/knowledge/project-README.md` 的嵌套 frontmatter 降级为该受支持子集，正文不变。

#### Scenario: 文档输入不可解析
- **WHEN** 除已适配的 `knowledge/project-README` 外，frontmatter 使用构建器不支持的格式或同名 sidecar 不是合法 JSON
- **THEN** 构建失败且输出文件路径及可用的行号或解析错误

#### Scenario: 非关键嵌套元数据被适配
- **WHEN** 静态构建扫描 `management/docs/knowledge/project-README.md`
- **THEN** 该文档仅使用扁平的列表与详情字段完成构建，正文保持不变

### Requirement: SPA 文档深链接有静态回退

生产构建完成后 SHALL 生成内容与入口 HTML 一致的 `404.html`，使静态托管平台将未知 history 路由交给 SPA。

#### Scenario: 直接打开文档深链接
- **WHEN** 用户直接访问或刷新一个文档详情 URL
- **THEN** 静态托管返回 SPA 回退页，应用启动后渲染该文档而非显示平台 404 页
