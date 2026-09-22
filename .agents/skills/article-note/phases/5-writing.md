# Phase 5/6：Writing 与交付

仅在用户确认结构后执行。

## 顺序

1. 运行 `figures.py inspect/convert`，只发布已选图片：`figures.py publish`（需文档图片端点已就绪；未就绪则跳过发布，图片留在 raw）。
2. 创建 `management/docs/论文笔记/<slug>.md` 与同名 `.json` sidecar。
3. 按 change design 逐节写作；偏离时先更新 change。
4. 运行 `validate-note.py` 和 `check-delivery.py`。

## Markdown 适配

- frontmatter 含 `title/author/date/tags/summary`，论文类笔记另加 `arxiv_id/papers_id`，可选 `id`。
- 顶层用 `##`，次级用 `###`，不使用 `####`。
- 公式放 fenced code block，随后给符号表和中文解释。
- 图片用 `![图 N · 说明](/api/management/docs-assets/<slug>/<file>)`；图号连续，每图在正文有解读。
- 流程和模块关系用 Mermaid；表格过宽时拆表或转纵向表。
- 内部文档使用 `[[slug]]` 或 `[[slug|label]]`；本仓库带命名空间的链接写成 `[[knowledge/xxx|label]]`、`[[project:<项目>]]`。

## 交付自检

核对来源可追溯、未披露项、图片 URL/体积、sidecar JSON、内部链接、Mermaid、TOC 层级、OpenSpec 状态和 Git diff。脚本只报告问题，不代替主 agent 判断。