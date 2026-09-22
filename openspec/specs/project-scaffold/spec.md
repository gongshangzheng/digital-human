# project-scaffold Specification

## Purpose

数字人项目的基础设施能力：定义仓库从 ProjFlow 脚手架派生后的目录结构、服务启动行为与版本控制基线，使团队可以开箱即用地运行项目管理、论文、评测三模块。

## Requirements

### Requirement: 仓库脚手架结构

仓库 SHALL 提供 ProjFlow 同构的目录结构：`management/`（团队档案、日报/周报/月报、文档）、`papers/`（论文数据与脚本）、`evaluation/`（模型/数据集/配置/结果）、`data/`（SQLite）、`scripts/`、`server/`（FastAPI 后端）、`web/`（Vue3 前端）、`openspec/`。README SHALL 描述项目为 digital-human（数字人研发管理平台），而非 ProjFlow demo。

#### Scenario: 目录完整性检查
- **WHEN** 检查仓库顶层目录
- **THEN** `management/`、`papers/`、`evaluation/`、`server/`、`web/`、`scripts/`、`openspec/` 全部存在且非空（脚手架文件）

#### Scenario: 身份改名
- **WHEN** 阅读 README 或启动服务
- **THEN** 项目名称与描述指向 digital-human，不残留 ProjFlow demo 字样

### Requirement: 一键启动

仓库 SHALL 提供 `start_services.sh`，一键启动后端（uvicorn，端口 8812）与前端（vite，端口 3212，`--strict-port`）。端口分配固定为 8812/3212（已实测不与 ProjFlow 8809/3210、pet-action-recognition 8788/3000 及本机已监听端口冲突），MUST 写入 `start_services.sh` 头部注释（端口分配清单），启动前执行端口冲突检查。启动后 `http://localhost:3212` 可访问、后端 `http://localhost:8812/api` 可响应。

#### Scenario: 一键启动成功
- **WHEN** 在仓库根目录执行 `bash start_services.sh`
- **THEN** 后端监听 8812、前端监听 3212，无端口冲突报错，前端页面可加载且能请求后端 API

#### Scenario: 与生态下游端口隔离
- **WHEN** ProjFlow（8809/3210）与 pet-action-recognition（8788/3000）同时运行
- **THEN** 本仓库服务仍可在自己的端口上正常启动，互不干扰

### Requirement: 版本控制基线

仓库 SHALL 在初始化完成后进行 git init 并产生首次提交，`.gitignore` SHALL 覆盖 `data/*.db`、`node_modules/`、`__pycache__/` 等生成物。

#### Scenario: 首次提交
- **WHEN** 初始化任务完成
- **THEN** `git log` 存在至少一个提交，`git status` 无未跟踪的生成物

### Requirement: 协作类管理模块隐藏

前端 SHALL 通过配置化的 hidden 列表（单一配置点）将协作类管理模块从导航菜单中隐藏，默认隐藏集合至少含：团队成员、报告（日报/周报/月报）、里程碑、会议纪要。项目树、任务看板、文档 MUST 保持可见。隐藏仅作用于菜单展示：对应路由 MUST 保留（URL 直达仍可用），后端 API 不变——修改 hidden 列表即可恢复显示，无需改代码结构。

#### Scenario: 菜单隐藏生效
- **WHEN** 加载前端导航
- **THEN** 菜单不出现团队成员/报告/里程碑/会议纪要入口，但项目树/任务看板/文档入口存在

#### Scenario: 路由保留可直达
- **WHEN** 浏览器直接访问被隐藏模块的 URL（如 /management/team）
- **THEN** 页面正常渲染（无导航高亮即可），不报 404

#### Scenario: 配置可恢复
- **WHEN** 从 hidden 列表移除某模块
- **THEN** 菜单重新显示该模块，无需其他代码改动

### Requirement: demo 数据清理

从 ProjFlow 拷贝时，management/ 中与数字人无关的示例成员、示例报告 MUST NOT 出现在新仓库；team 档案保留为空模板或待填结构。

#### Scenario: 无 ProjFlow demo 残留
- **WHEN** 检查 `management/team/` 与报告目录
- **THEN** 不含 ProjFlow 的示例成员与示例报告内容
