# paper-knowledge-base Specification

## Purpose

数字人论文与知识库能力：从博客与 InternWiki 导入的论文、笔记、工程文档构成的可检索知识底座，支持分类浏览、元数据查询与笔记关联。

## Requirements

### Requirement: 博客论文资产导入

系统 SHALL 从博客 `src/pages/` 中识别数字人相关页面（关键词：talking head / talking face / avatar / digital human / 数字人 / audio-driven / lip sync 等及 `paper-*`、`digital-human-*`、`*survey*`、`arxiv-digest-*` 文件名模式），提取每篇的 title、tags、日期、slug，转为结构化清单存入仓库。识别结果 MUST 可复核（含命中原因），误命中（如 php-security 等无关页）MUST 可被人工排除。

#### Scenario: 关键词命中导入
- **WHEN** 运行博客导入脚本处理 `paper-wav2lip.html`
- **THEN** 生成一条包含 title、tags、日期、原文件相对路径的记录

#### Scenario: 误命中可排除
- **WHEN** 某页面仅因弱关键词命中但主题无关
- **THEN** 可通过排除清单（denylist）将其移出导入结果并留痕

### Requirement: arXiv 元数据补全

对导入记录中能解析出 arXiv id 的论文，系统 SHALL 调用 arXiv API 补全作者、摘要、发表信息，写入 SQLite 论文库（沿用 ProjFlow papers 模块的表结构与 API）。

#### Scenario: arXiv 补全成功
- **WHEN** 记录含 arXiv id 且 API 可达
- **THEN** 论文库中该条目具备作者、摘要、分类字段

#### Scenario: API 不可达降级
- **WHEN** arXiv API 超时或不可达
- **THEN** 导入不失败，条目落库并标记元数据缺失，可后续重试补全

### Requirement: 知识库文档复制

系统 SHALL 将 InternWiki 中数字人相关文档（tangwen 的基础/模型精读/工程与评测/快速导读/微调与实践，junjiawang 的 voice-agent-web 数字人文档，及 digital-human 项目 notes）复制到仓库知识目录，保留 frontmatter 元数据，并在 README 或索引中登记来源与复制日期。

#### Scenario: 文档复制保真
- **WHEN** 复制完成
- **THEN** 目标文档与源文档内容一致，frontmatter 完整，索引中有对应条目与来源路径

### Requirement: 分类体系

论文库 SHALL 按数字人主题提供分类（至少：2D talking head、3D 头像（3DGS/NeRF）、语音驱动动画、实时系统与加速、评测与数据集、survey），每条记录 MUST 归入至少一个分类。

#### Scenario: 分类归属
- **WHEN** 浏览论文库任意条目
- **THEN** 该条目有至少一个分类标签，且分类属于预定义集合
