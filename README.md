# Digital Human

数字人研发管理平台——论文知识库、评测体系、项目管理三大模块。基于 [ProjFlow](https://github.com/) 共享脚手架派生（Vue 3 + FastAPI + Markdown/SQLite），面向钉钉会议面试官数字人方向。

## 项目背景

本仓库是数字人方向的单一事实来源，收拢分散在四个信息源的资产：

- **ProjFlow**（`~/code/ProjFlow`）：共享脚手架上游（management / papers / evaluation 三模块）
- **博客**（`~/gongshangzheng.github.io`）：数字人论文精读、工程解读、survey（~156 篇，导入论文库）
- **InternWiki**（`~/code/InternWiki`）：数字人知识库（基础 / 模型精读 / 工程与评测，复制到 `management/docs/knowledge/`）
- **CyberVerse**（`~/code/CyberVerse`）：实时数字人 Agent 框架优化 fork（avatarforcing / ditto 等模型插件），独立 clone + commit 锚定；四源溯源登记见 `management/docs/knowledge/README.md`

## 项目结构

```
digital-human/
├── management/      # 项目管理体系（项目树、任务看板、文档；团队/报告/里程碑/会议已隐藏）
│   └── docs/knowledge/  # 知识库（InternWiki / 博客精选复制）
├── papers/          # 论文搜集模块（数字人论文元数据 + 笔记）
├── evaluation/      # 评测体系（模型/数据集/配置/结果）
├── data/            # 数据目录（papers.db）
├── scripts/         # 工具脚本（博客论文提取、arXiv 导入）
├── server/          # FastAPI 后端（端口 8812）
├── web/             # Vue 3 前端（端口 3212）
└── start_services.sh # 一键启动
```

## 快速开始

```bash
# 一键启动（后端 8812 + 前端 3212）
bash start_services.sh
```

启动后访问 http://localhost:3212

## 技术栈

| 层 | 技术 | 端口 |
|----|------|------|
| 前端 | Vue 3 + Vite + Naive UI + Vue Router | 3212 |
| 后端 | FastAPI (Python) | 8812 |
| 数据源 | Markdown 文件 + SQLite | — |

> 端口分配遵循 ProjFlow 生态惯例：ProjFlow=8809/3210，pet-action-recognition=8788/3000，本仓库=8812/3212。

## License

MIT
