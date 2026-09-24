## 1. 素材与结构（待用户审核）

- [x] 1.1 建工作区 `.cache/article-note/fpsattention/`；抓取 arXiv `2506.04648`（HTML 成功；source tarball 406、PDF 首下截断后用 `curl -C -` 补到 31MB / 26 页）
- [x] 1.2 下载 3 张正文图（x1/x2/x3）；确认 HTML 中仅此 3 张位图（附录 96 张可视化网格按需排除）
- [x] 1.3 派生 `raw/sources/paper.txt`（91k 字符）
- [x] 1.4 跑 4 个委派 lane（methodology / experiment / local-crosscheck / image-collection）+ 自写 2 个 lane（citation / terminology）
- [x] 1.5 写 `synthesis.md`；`validate-analysis.py` 通过（exit 0，仅 `local-crosscheck` 触发「unknown lane」warning）
- [x] 1.6 image-collection lane 额外从 PDF 渲染出 Figure 5（p7）与 Figure 7（p10）备用
- [x] 1.7 写 change 的 proposal + design（含目标文档架构、10 节大纲、图表公式清单、待决项）
- [x] 1.8 **用户审核结构**（design 第 3、5、7 节，含三项待决：是否发布 Fig 5/7、order 取值、博客修正是否另开任务）

## 2. 图片发布

- [x] 2.1 `figures.py convert` 把 x1/x2/x3 转 WebP（三张合计约 498KB）
- [x] 2.2 `figures.py publish` 到 `management/docs/_assets/fpsattention/`
- [x] 2.3 若用户要求发布 Fig 5/7：`inspect` 确认 ≤1600px 与 ≤500KB 后一并发布
- [x] 2.4 核对 `GET /api/management/docs-assets/fpsattention/<file>` 全部 200
- [x] 2.5 记录三张图的图内小字可读性未目视确认（本机模型不支持读图）

## 3. 正文写作

- [x] 3.1 写第 0/1/2 节（元信息表、四条要点、三段式动机 + 图 1 + 高幅值机制解释）
- [x] 3.2 写第 3 节：粒度分工三句话（$Q/K$ tile-wise、$V$ channel-wise、$P$ 固定标量）、3D tile 理由、步感知三段（$\alpha_1/\alpha_2$）、kernel 取向；配图 2/图 3 与两张 Mermaid
- [x] 3.3 写第 4 节：训练配置披露表 + 数据过滤阈值 + **QAT 步数未披露**的如实标注
- [x] 3.4 写第 5 节：kernel 与 E2E 两套口径、评测分辨率与采样设置、硬件口径（H20/Hopper）
- [x] 3.5 写第 6 节：Table 1/2/3/4/5 逐格 + Figure 6 定性 + 附录 H；标注 Table 3/4 的数值重合
- [x] 3.6 写第 7 节：量化线与稀疏线谱系 + 三点批评 + 三类基线表 + SpargeAtten 是最直接对照 + 与步数蒸馏正交
- [x] 3.7 写第 8 节：Limitations 五条 + §5 两条边界 + **我们的一手经验**（A10 无 FP8）+ 本地素材三处出入 + 可操作启发（含「先问硬件代际再谈精度格式」）
- [x] 3.8 写第 9/10 节（术语表、符号表、六条口径易错、相关文档链接）
- [x] 3.9 写 sidecar `fpsattention.json`（`changelog` 记首次创建；`related` 用含 `slug`/`title` 的对象；不含 `papers/` 条目）

## 4. 交付物

- [x] 4.1 更新 `management/docs/论文笔记/README.md` 清单：`fpsattention.md` 状态改为已完成
- [x] 4.2 确认图片编号按笔记出现顺序重排（图 1–图 3，或含 Fig 5/7 时的图 1–图 5）
- [x] 4.3 按裁决写入 `order: 100`（原 70 与并行会话的 `omnimate` 撞号，按「不动既有文档」规则挪本方；100 作为加速组起点）

## 5. 校验与提交

- [x] 5.1 `validate-note.py` 通过（frontmatter / 标题层级 / 公式定界符 / 图片 URL / 图号连续 / sidecar / 内链）
- [x] 5.2 `check-delivery.py` 汇总通过
- [x] 5.3 浏览器实测：图片解码、公式与 Mermaid 渲染、内链可跳、表内无 `\|` 转义残留
- [x] 5.4 `docs_order.py list management/docs/论文笔记` 显示 order 无重复
- [x] 5.5 `openspec validate docs-note-fpsattention --strict` 通过
- [x] 5.6 提交（`docs(note): 新增 fpsattention 论文笔记 —— 训练感知的 FP8 与稀疏协同`），只包含本篇相关文件
