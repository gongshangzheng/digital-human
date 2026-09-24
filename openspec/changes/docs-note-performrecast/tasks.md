## 1. 设计与素材确认

- [x] 1.1 ✅ 用户以「继续」确认 design（表 1 两列 / venue 口径 / 6 图 / 第 8 节对照）。
- [x] 1.2 ✅ 素材抓取：arXiv HTML 成功（`paper.txt`）、source/PDF 406、博客精读、9 张原图。
- [x] 1.3 ✅ `validate-analysis.py` 通过。
- [x] 1.4 ✅ 逐格核对 Table 1（含 Enhancement 列）、Table 2、消融与附录训练配置；Table 3（MEAD）只作定性登记。

## 2. 图片处理与发布

- [x] 2.1 ✅ 6 张图转 WebP（teaser 1600px / two_infer_modes 1600px / keypoints 1526px），合计 460KB。
- [x] 2.2 ✅ 发布到 `management/docs/_assets/performrecast/`。
- [x] 2.3 ✅ 正文 6 处图题与解读，URL 用绝对 `/api/management/docs-assets/performrecast/...`。

## 3. 正文写作

- [x] 3.1 ✅ 第 0/1 节。
- [x] 3.2 ✅ 第 2 节（任务边界 + 运算顺序 Mermaid + 图 1）。
- [x] 3.3 ✅ 第 3 节（式 1–5、7、8；三组关键点；BAM；图 2/3/4）。
- [x] 3.4 ✅ 第 4 节（Teacher-Student + 10 项披露表 + 加噪 / x_d,self / mask）。
- [x] 3.5 ✅ 第 5 节（式 6/9、三模式、Mermaid、图 5、6 images/s）。
- [x] 3.6 ✅ 第 6 节（MetaHuman benchmark + Table 1 两列 + 消融 + Table 2 + Table 3 定性 + 图 6）。
- [x] 3.7 ✅ 第 7 节（谱系对照表）。
- [x] 3.8 ✅ 第 8 节（论文局限 + 缺口 vs 我们结论 + 4 条启发）。
- [x] 3.9 ✅ 第 9/10 节（术语符号表 + 相关文档）。

## 4. sidecar 与索引

- [x] 4.1 ✅ `performrecast.json`（changelog / progress / appendix / related）。
- [x] 4.2 ✅ `论文笔记/README.md` 清单补一行（order 65）。

## 5. 验证与交付

- [x] 5.1 ✅ `validate-note.py` 通过。
- [x] 5.2 ✅ 表格列数一致、公式定界符合法、Mermaid 可渲染、6 张图 URL 与资产存在。
- [x] 5.3 ✅ `docs_order.py list` 中本篇 order 65 无冲突（目录内另有并行会话遗留的重复 order 160，与本篇无关）。
- [x] 5.4 ✅ `openspec validate docs-note-performrecast --strict` 通过。
- [x] 5.5 ✅ 提交 `docs(note): 新增 performrecast 论文笔记`。
