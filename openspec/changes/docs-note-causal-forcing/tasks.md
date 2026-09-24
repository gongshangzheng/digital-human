## 1. 素材与分析

- [x] 1.1 初始化工作区 `.cache/article-note/causal-forcing/` 并抓取：LaTeX 源（`example_paper.tex` 834 行）、HTML 派生正文、PDF、17 张候选图。
- [x] 1.2 读完全文主线与附录实现细节，事实位置索引落到 `analysis/`（methodology / experiment / terminology 三 lane）与 `synthesis.md`。
- [x] 1.3 核对元信息：作者与单位（清华 / ShengShu / UT Austin / 人大）、ICML 2026、arXiv `2602.02214`（v1 2026-02-02、v5 2026-06-01）、开源仓库 `thu-ml/Causal-Forcing` 与项目页。
- [x] 1.4 登记 6 张主图与源文件映射（`Fig2.pdf`–`Fig6.pdf` + `qualitive.pdf` 对应论文 Fig 1–6），确认转换工具可用（`pdftoppm` / `magick` / Pillow 12）。
- [x] 1.5 记录与 `avatar-forcing.md` 的 diffusion forcing 张力，写进 `synthesis.md` 与 `analysis/methodology.md` 的「不确定性与缺口」。

## 2. 结构审批

- [x] 2.1 创建 `openspec/changes/docs-note-causal-forcing/`（proposal / design / tasks，`skip_specs: true`）。
- [x] 2.2 用户审核 design 通过（"好的"）。
- [x] 2.3 design 修订一处：`order` 由 70 顺延为 **80**（70 被同时段新增的 `omnimate` 占用）。

## 3. 图片发布

- [x] 3.1 用 `pdftoppm` 把 6 张 PDF 转 PNG（150 DPI），再用 `figures.py convert` 转 WebP：最长边 ≤1600px、单图 ≤500KB。
- [x] 3.2 发布到 `management/docs/_assets/causal-forcing/`，命名 `fig-1-…` 至 `fig-6-…`。
- [x] 3.3 逐张确认存在与体积合规（总 888 KB，单张最大 359 KB）；图 3（三面板）与图 6（多面板）小字可读性已提请用户目视。
- [x] 3.4 单篇图片总量 888 KB ≤5MB。

## 4. 正文与 sidecar

- [x] 4.1 §0 论文信息（含「papers 库未入库」）、§1 一句话总结（4 条贡献）。
- [x] 4.2 §2 问题与动机：两层 gap、Self Forcing vs standard DMD，配图 1。
- [x] 4.3 §3：3.1 现有方法局限（图 2）；3.2 frame-level injectivity 与条件期望塌陷（图 3 + 式 3–5 + 符号表）；3.3 三阶段（图 4、图 5 + DMD 梯度）；3.4 causal CD 扩展；两张 Mermaid。
- [x] 4.4 §4 训练与实现细节：10 项配置披露表，硬件与随机种子写「未披露」。
- [x] 4.5 §5 推理与系统链路：chunk-wise / frame-wise、4 步时间步、temporal KV cache、FPS/延迟口径警告。
- [x] 4.6 §6 实验与结果：主表、消融表、评测口径，配图 6；三个提升百分比已自洽校验（+19.3% / +8.7% / +16.7%）。
- [x] 4.7 §7 相关工作与定位（含与 APT2 的三点区别、长视频适配为正交问题）。
- [x] 4.8 §8 局限与启发：论文自述局限 + DF 张力三段式（论文结论 / 我们结论 / 未验证推断）+ 可操作启发。
- [x] 4.9 §9 术语与符号表（含三处易错命名）、§10 相关文档（6 组链接）。
- [x] 4.10 `causal-forcing.json`：frontmatter 只含 `arxiv_id`、sidecar 含 `changelog` / `progress` / `appendix` / `related`。

## 5. 验证与交付

- [x] 5.1 `validate-note.py` = OK、`validate-analysis.py` = OK、`check-delivery.py` = OK（首次因 `synthesis.md` 超 1000 字与 lane 缺四个规定小标题而失败，已按规范拆分到 `analysis/` 三 lane 并重写 synthesis）。
- [x] 5.2 frontmatter 键与既有笔记一致（`title`/`author`/`date`/`tags`/`arxiv_id`/`summary`/`order`），无 `papers_id`。
- [x] 5.3 结构自检：11 个 `##`、10 个 `###`、表格列数全一致、`$` 无奇数行、2 个 Mermaid 块配对且无单 `$`；6 张图 URL 全部命中资产；9 处站内链接目标全部存在。
- [x] 5.4 `docs_order.py list management/docs/论文笔记` 确认 `order: 80` 无重复（70 已被 omnimate 占用）。
- [x] 5.5 FastAPI 详情接口 200（16,431 字符，6 张图 URL 齐全），sidecar 5 条 `related` 全部解析。
- [x] 5.6 `openspec validate docs-note-causal-forcing --strict` 通过。
- [x] 5.7 提交 `docs(note): 新增 Causal Forcing 论文笔记`。

> 遗留：图 3、图 6 的图内小字可读性需用户目视确认（本机模型不支持读图）。
