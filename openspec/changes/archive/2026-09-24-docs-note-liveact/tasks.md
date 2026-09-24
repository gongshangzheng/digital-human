## 1. 素材与结构（待用户审核）

- [x] 1.1 建工作区 `.cache/article-note/liveact/`；抓取 arXiv `2603.11746` HTML(v2) + PDF（source tarball 406 失败已降级）
- [x] 1.2 下载 7 张正文图并逐个 PIL 校验；排除机构 logo 与 LaTeXML 徽标
- [x] 1.3 派生 `raw/sources/paper.txt`（HTML → 纯文本，公式保留 `$alttext$`）
- [x] 1.4 跑 4 个委派 lane（methodology / experiment / code-analysis / image-collection）+ 自写 2 个 lane（citation / terminology）
- [x] 1.5 写 `synthesis.md`；`validate-analysis.py` 通过（exit 0）
- [x] 1.6 填 `workspace.json` 的 `repository` 字段（CyberVerse `models/SoulX-LiveAct` @4968280）
- [x] 1.7 写 change 的 proposal + design（含目标文档架构、10 节大纲、图表公式清单、风险项）
- [x] 1.8 **用户审核结构**（design 第 3、5、7 节）；确认后才进入第 2 组
- [x] 1.9 核对 $m$：论文式(5) 掩码用 block size $m$，消融给出首块 6、后续块 8；代码 `BLKSZ_LST=[6,8]` 一致 ⇒ 按 chunk 计，无冲突

## 2. 图片发布

- [x] 2.1 `figures.py inspect` 清点 7 张原图（原始合计 9.26MB，需转换）
- [x] 2.2 `figures.py convert` 转 WebP：5 张缩到最长边 ≤1600px、压到单图 ≤500KB
- [x] 2.3 `figures.py publish` 到 `management/docs/_assets/liveact/`；确认单篇合计 ≤5MB
- [x] 2.4 核对 `GET /api/management/docs-assets/liveact/<file>` 全部 200
- [x] 2.5 记录图内小字可读性未目视确认（本机模型不支持读图），供用户复核

## 3. 正文写作

- [x] 3.1 写第 0/1/2 节（元信息表、四条贡献、两个挑战 + Figure 1 现象 + ARPP 定位表）
- [x] 3.2 写第 3 节：式(1)(2)(3)(4) 与逐项解释、step alignment 的实质、ConvKV 的卷积压缩；配图 2/图 3 与两张 Mermaid
- [x] 3.3 写第 4 节：十项配置披露表 + 初始化来源 + 蒸馏步数 400/300 的如实标注 + 未披露清单
- [x] 3.4 写第 5 节：推理时序、20 FPS 与 <50ms 约束、FP8/序列并行/算子融合、ConvKV 1.9% 开销；hour-scale 记为机制论证
- [x] 3.5 写第 6 节：Table 2/3/4/5 全量数字 + EMTD 异常 + 失败标签 + 定性结论；配图 4/5/6/7
- [x] 3.6 写第 7 节：两条脉络与「与 Self Forcing 的差别在 ARPP」
- [x] 3.7 写第 8 节：无 Limitations 节的事实、论文缺口 vs 我们结论表、两条接入路径、A10 两组冒烟、走不通的路与可操作启发
- [x] 3.8 写第 9/10 节（术语表、符号表、命名易错、相关文档链接）
- [x] 3.9 写 sidecar `liveact.json`（`changelog` 记首次创建；`related` 用含 `slug`/`title` 的对象）

## 4. 交付物

- [x] 4.1 更新 `management/docs/论文笔记/README.md` 清单：`liveact.md` 状态改为已完成
- [x] 4.2 确认图片编号按笔记出现顺序重排（图 1–7），未沿用论文 Figure 编号

## 5. 校验与提交

- [x] 5.1 `validate-note.py` 通过（frontmatter / 标题层级 / 公式定界符 / 图片 URL / 图号连续 / sidecar / 内链）
- [x] 5.2 `check-delivery.py` 汇总通过
- [x] 5.3 浏览器实测：7 张图片解码、公式与 Mermaid 渲染、内链可跳
- [x] 5.4 `docs_order.py list management/docs/论文笔记` 显示 order 完整无重复
- [x] 5.5 `openspec validate docs-note-liveact --strict` 通过
- [x] 5.6 提交（`docs(note): 新增 liveact 论文笔记 —— Neighbor Forcing + ConvKV Memory`），只包含本篇相关文件
