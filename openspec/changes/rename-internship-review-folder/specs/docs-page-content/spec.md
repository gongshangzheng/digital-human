## MODIFIED Requirements

### Requirement: 中文（Unicode）文件名文档可访问

文档详情接口 SHALL 接受包含 Unicode 字符（含中文、空格）的 slug，并能正确解析到对应 `.md` 文件。slug 校验 MUST NOT 仅允许 ASCII 字符集。

#### Scenario: 打开中文名文档
- **WHEN** 请求 `GET /api/management/docs/knowledge/数字人基础`
- **THEN** 返回 200 与该文档内容（title/content 与文件一致）
- **WHEN** 请求 `GET /api/management/docs/数字人概述/数字人介绍与技术路线`
- **THEN** 返回 200 与正文内容

#### Scenario: 路径穿越仍被拒绝
- **WHEN** slug 含 `..` 或超出文档根目录的路径
- **THEN** 返回 400 或 404，不读取根目录外文件

### Requirement: 文件夹在列表中的先后可配置

文档列表树中文件夹的先后 SHALL 由服务端配置的顺序决定（本仓库默认 `数字人概述 → 论文笔记 → knowledge`）；未列入配置的文件夹 SHALL 排在已配置的之后，并在其后按 `order` → `id` → `date` 排序。

#### Scenario: 默认顺序
- **WHEN** 文档树包含 `数字人概述/`、`论文笔记/`、`knowledge/` 三个文件夹
- **THEN** 列表中依次出现 数字人概述 → 论文笔记 → knowledge

#### Scenario: 未配置的文件夹
- **WHEN** 新增一个未列入配置的文件夹（如 `temp/`）
- **THEN** 它排在已配置文件夹之后，不报错
