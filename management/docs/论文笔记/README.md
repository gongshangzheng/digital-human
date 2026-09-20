# 论文笔记

> 数字人论文精读笔记，夹内平铺、不嵌套。历史博客精读（~90 篇）已入 papers 库（带 blog_url），此处只写**新写**的精读笔记。

## 命名规范

- 文件名 = 论文短名 slug，与 papers 库条目对应：`{slug}.md`（如 `vasa1.md`、`leaptalk-2026.md`）
- frontmatter 必填：`arxiv_id`（有则填）、`papers_id`（papers 库 id，如 `arxiv-2605.29316` / `blog-leaptalk-2026`）、`date`
- 笔记与 papers 库互链：笔记 frontmatter 指向 papers_id；papers 库条目 blog_url/笔记字段回填本文件路径

## 结构建议

问题定义 → 方法核心（一图一表）→ 与我们工作的关系（身份一致性/PasteBack/实时性视角）→ 可复用点与复现成本
