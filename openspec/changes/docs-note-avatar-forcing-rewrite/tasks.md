## 1. 素材与结构（已完成，待审核）

- [x] 1.1 建工作区 `.cache/article-note/avatar-forcing/`；抓取 2601.00664 的 source tarball + HTML + PDF（16 张候选图）
- [x] 1.2 填 `workspace.json` 的 repository 字段（CyberVerse `models/avatarforcing/` @4968280）
- [x] 1.3 写分析 lane：`methodology` / `experiment` / `terminology` / `citation` / `code-analysis`
- [x] 1.4 写 `synthesis.md`；`validate-analysis.py` 通过
- [x] 1.5 写 change 的 design 大纲（论文速览 / 价值主张 / 10 节大纲 / 取舍 / 图表公式清单 / 引用关系 / 待确认项）
- [x] 1.6 **用户审核结构**（design 第 3、7 节）；确认后才进入第 2 组

## 2. 图片发布

- [x] 2.1 用 `pdftoppm` 把选定 PDF 图转 PNG，再用 Pillow 转 WebP（≤1600px、≤500KB）
- [x] 2.2 `figures.py publish` 发布到 `management/docs/_assets/avatar-forcing/`；`figures.py inspect` 确认体积
- [x] 2.3 核对 `GET /api/management/docs-assets/avatar-forcing/<file>` 全部 200

## 3. 正文写作

- [x] 3.1 从 PDF 抄录主结果表 / talking / listening / 消融表数值（不依赖摘要）
- [x] 3.2 按 10 节骨架写 `management/docs/论文笔记/avatar-forcing.md`（frontmatter 改 `arxiv_id: 2601.00664`；公式用 fenced code block；标题只用 `##` / `###`）
- [x] 3.3 工程层压缩进第 8 节，细节外链 `实习复盘/`
- [x] 3.4 第 0 节写入与 2603.14331 的区分说明

## 4. 交付物

- [x] 4.1 写 sidecar `management/docs/论文笔记/avatar-forcing.json`（`changelog` 记录重写与旧版错引；`progress`；`related`）
- [x] 4.2 更新 `management/docs/论文笔记/README.md`：该篇状态改「已完成」；若确认采用 10 节骨架，同步更新「统一模板」节
- [x] 4.3 处理 `papers_id`（按裁决：补录 2601.00664 / 省略 / 其它）

## 5. 校验与提交

- [x] 5.1 `validate-note.py` 通过（frontmatter / 标题层级 / 公式 / 图片 URL / 图号连续 / sidecar / 内链）
- [x] 5.2 `check-delivery.py` 汇总通过
- [x] 5.3 浏览器实测：文档页图片正常显示（figure + figcaption）、Mermaid 渲染、内链可跳
- [x] 5.4 `openspec validate docs-note-avatar-forcing-rewrite --strict` 通过
- [x] 5.5 提交（`docs(note): 按 article-note 重写 avatar-forcing —— 纠正 2601.00664/2603.14331 错引 + 补图与 sidecar`）
