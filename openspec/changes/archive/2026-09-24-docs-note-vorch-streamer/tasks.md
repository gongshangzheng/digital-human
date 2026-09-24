## 1. 素材与结构（待用户审核）

- [x] 1.1 建工作区 `.cache/article-note/vorch-streamer/`；抓取 arXiv `2608.05663` HTML(v2) + PDF（source tarball 406 失败已降级）
- [x] 1.2 下载 3 张 png 正文图；**补抓 Figure 2 的 SVG**（HTML 用 `<object>` 引用，按 `<img src>` 扫描会漏），确认 `rsvg-convert` 可用
- [x] 1.3 派生 `raw/sources/paper.txt`（HTML → 纯文本，公式保留 `$alttext$`）
- [x] 1.4 跑 4 个委派 lane（methodology / experiment / citation / image-collection）+ 自写 1 个 lane（terminology）
- [x] 1.5 写 `synthesis.md`；`validate-analysis.py` 通过（exit 0）
- [x] 1.6 写 change 的 proposal + design（含目标文档架构、10 节大纲、图表公式清单、风险项）
- [x] 1.7 **用户审核结构**（design 第 3、5、7 节）；确认后才进入第 2 组

## 2. 图片发布

- [x] 2.1 `rsvg-convert` 把 `VorchStreamer_framework.svg` 栅格化到最长边 ≤1600px 的 PNG
- [x] 2.2 `figures.py convert` 把 4 张图转 WebP，单图 ≤500KB、合计 ≤5MB
- [x] 2.3 `figures.py publish` 到 `management/docs/_assets/vorch-streamer/`；确认 4 张到位（不是 3 张）
- [x] 2.4 核对 `GET /api/management/docs-assets/vorch-streamer/<file>` 全部 200
- [x] 2.5 记录图内小字可读性未目视确认（本机模型不支持读图），供用户复核

## 3. 正文写作

- [x] 3.1 写第 0/1/2 节（元信息表、四条贡献、两个困境 + 图 1）
- [x] 3.2 写第 3 节：3.1 合成语料 / 3.2 因果流式（式 1–4、同步块≈1s、TF 10%/DF 90%）/ 3.3 长时自强制与 DMD（式 5–10）/ 3.4 LLM 语音规划（式 11–13）；配图 2 与两张 Mermaid
- [x] 3.3 写第 4 节：三阶段训练量 + 22B/22.8B 两个口径 + 未披露清单
- [x] 3.4 写第 5 节：每块 4 步、推理默认 3+1（训练 3+3）、windowed KV cache + eviction、FPS 口径
- [x] 3.5 写第 6 节：Table 1/2/3/4/6 全量数字与加粗读法 + T2AV/TIA2V 口径警告；配图 3、图 4
- [x] 3.6 写第 7 节：三条脉络 + OmniForcing 最近前作 + Wan-Streamer 互补
- [x] 3.7 写第 8 节：三处口径问题 + 与四篇笔记的漂移路线对照 + 可操作启发
- [x] 3.8 写第 9/10 节（术语表、符号表、六条命名易错、相关文档链接）
- [x] 3.9 写 sidecar `vorch-streamer.json`（`changelog` 记首次创建；`related` 用含 `slug`/`title` 的对象；不含 `papers/` 条目）

## 4. 交付物

- [x] 4.1 更新 `management/docs/论文笔记/README.md` 清单：`vorch-streamer.md` 状态改为已完成
- [x] 4.2 确认图片编号按笔记出现顺序重排（图 1–4），未沿用论文 Figure 编号

## 5. 校验与提交

- [x] 5.1 `validate-note.py` 通过（frontmatter / 标题层级 / 公式定界符 / 图片 URL / 图号连续 / sidecar / 内链）
- [x] 5.2 `check-delivery.py` 汇总通过
- [x] 5.3 浏览器实测：4 张图片解码、公式与 Mermaid 渲染、内链可跳
- [x] 5.4 `docs_order.py list management/docs/论文笔记` 显示 order 完整无重复（注意并行会话已占用 liveportrait 30 / lia-x 40）
- [x] 5.5 `openspec validate docs-note-vorch-streamer --strict` 通过
- [x] 5.6 提交（`docs(note): 新增 vorch-streamer 论文笔记 —— 长时自强制 + DMD + LLM 语音规划`），只包含本篇相关文件
