# pages-deploy Specification

## Purpose

定义 Digital Human 前端部署至 GitHub Pages 的自动化路径、部署基路径和静态文档产物要求，使仓库可在无后端环境中稳定发布可读文档。

## Requirements

### Requirement: 推送主分支自动部署 GitHub Pages

仓库 SHALL 提供 GitHub Actions 工作流，在 `master` 分支收到推送或通过手动触发时，于 `web/` 下安装依赖、执行 `npm run build`，并将 `web/dist` 发布至 GitHub Pages。工作流 MUST 使用并发控制，避免旧构建覆盖新部署。

#### Scenario: 推送触发部署
- **WHEN** 新提交推送到 `master`
- **THEN** 工作流构建 `web/dist` 并部署到 GitHub Pages，且同一时间只保留一个有效部署

#### Scenario: 手动触发部署
- **WHEN** 维护者通过 `workflow_dispatch` 启动工作流
- **THEN** 工作流执行与主分支推送相同的构建和部署步骤

#### Scenario: 构建调用完整 npm 脚本
- **WHEN** 工作流构建前端
- **THEN** 使用 `npm run build`，从而包含静态文档、静态图片和 `404.html` 的生成步骤

### Requirement: 部署基路径不改变本地开发路径

构建与预览产物 SHALL 使用 `/<仓库名>/` 作为基路径，Vue Router SHALL 使用当前环境的基路径；本地开发服务器 SHALL 继续使用 `/` 作为基路径，保留现有本地访问 URL。

#### Scenario: 本地开发地址保持不变
- **WHEN** 开发者运行前端开发服务器
- **THEN** 应用可在 `http://localhost:3212/` 访问，无需仓库名子路径

#### Scenario: 子路径部署可以路由
- **WHEN** 构建产物部署到 `https://<owner>.github.io/<repository>/`
- **THEN** 资源和 Vue 路由均以 `/<repository>/` 为基路径，文档首页和详情路由能够匹配

#### Scenario: 本地预览复现部署路径
- **WHEN** 开发者运行生产产物预览
- **THEN** 预览使用与构建产物相同的仓库子路径，可用于验证静态文档和深链接

### Requirement: Pages 产物保留静态文档能力

部署产物 SHALL 包含静态文档数据、文档图片和 SPA 回退页；在没有 FastAPI 的 GitHub Pages 环境中，文档首页、文档详情、正文图片与文档深链接 MUST 可用。

#### Scenario: Pages 上浏览有图文档
- **WHEN** 读者打开 GitHub Pages 上带图片的文档详情
- **THEN** 列表、正文和图片均从部署产物加载，无需请求 FastAPI

#### Scenario: Pages 上非文档模块的边界
- **WHEN** 读者打开依赖 FastAPI 或 SQLite 的非文档模块
- **THEN** 本 capability 不保证其数据可用；部署说明明确该边界
