## Context

- **素材**（`.cache/article-note/liveportrait/`，已通过 `validate-analysis.py`）：主源 HTML（arXiv LaTeXML，公式在 `annotation`）+ PDF（16 页，页码/公式权威）；14 张原图已下载到 `raw/figures/`；`analysis/` 含 methodology / experiment / terminology / image-collection 四份；`synthesis.md` 为事实位置索引。
- **论文元信息**（取自 PDF 首页）：arXiv `2407.03168v2`；作者 Jianzhu Guo、Dingyun Zhang、Xiaoqiang Liu、Zhizhou Zhong、Yuan Zhang、Pengfei Wan、Di Zhang；单位 Kuaishou Technology、University of Science and Technology of China、Fudan University；代码库 `github.com/KwaiVGI/LivePortrait`。**首页未见会议标注 → 正文不声明会议（venue 写"arXiv 预印本"）**。
- **我方状态**：**未接入**（`~/code/CyberVerse/models` 下无对应目录），无第一手工程素材。因此第 8 节「我们的实测」只写"在表示谱系与概述里的位置"，不写实测结论。
- 用户已明确要求：完整结构 + 配图（不走"摘要档"）。

## Goals / Non-Goals

**Goals:**
- 按 `论文笔记/README.md` 的 10 节骨架成文，采用 5 张论文原图并逐图配中文图题与正文解读
- 关键结论附来源锚点（§/Fig./Table/页），数字标来源档；论文未披露项写"未披露"

**Non-Goals:**
- 不写我们的接入/实测结论（未接入，无素材）
- 不为凑结构编造数字；不补齐论文未披露的超参
- 不改其它笔记与概述正文（仅链接替换）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位 / venue（arXiv 预印本，不声明会议）/ arXiv / 代码库 / papers 库条目 `arxiv-2407.03168` |
| 1 | 一句话总结 | 非扩散 + 隐式关键点 + warping；两阶段（基模型 + 三个小 MLP：stitching / eyes / lip retargeting）；要点 4 条：12.8ms/帧（RTX 4090、naive PyTorch）、约 6900 万帧与 18.9K 身份、Stage II 只训小 MLP、论文把扩散列为"昂贵且精确可控性弱"（Abstract p.1；Sec. 1 p.1；Sec. 3.2 p.4；Sec. 5 p.11） |
| 2 | 问题与动机 | 扩散路线昂贵、精确可控性弱；隐式关键点框架效率高但泛化与可控性不足；数据质量与可扩展性为两个抓手（Sec. 1–3；Sec. 3.2「High quality data curation」） |
| 3 | 方法精析 | 主链路：外观提取器 F + 运动提取器 M + warping W + 解码器 G；Stage I 隐式关键点运动变换与级联损失（Eq. 1→Eq. 2→Eq. 7）；Stage II 冻结主干、只训 stitching 与 eyes/lip retargeting；关键假设「紧凑隐式关键点≈隐式 blendshape，组合可由小 MLP 学到」（Sec. 3.2 p.4；Sec. 3.3 p.5；Fig. 2；Fig. 3） |
| 4 | 训练与实现细节 | 数据整理（过滤前 9200 万帧 → 6900 万帧、约 18.9K 身份）、图像-视频混合训练、网络升级与可缩放运动变换；正式披露表列 10 项，其中**损失权重、训练步数/epoch、Stage II 学习率与 batch、隐关键点数量 K、eyes/lip condition 提取算法均写"未披露"** |
| 5 | 推理与系统链路 | 源图一次编码 + 逐帧驱动推理；12.8ms/帧口径（RTX 4090、naive PyTorch）；Mermaid 时序图；与我们链路的接口：Ditto 的 21×3 位移表与逐维扰动控制同源（链《数字人动作》） |
| 6 | 实验与结果 | **自重现**（Table 2，p.8）：PSNR/SSIM/LPIPS/L₁/CSIM/MAE 六项领先，MAE(°) 7.0535（TalkingHead-1KH）/ 6.6966（VFHQ）；**跨重现**（Table 3，p.9）：AED/APD/MAE 与 VFHQ FID 占优，但 TalkingHead-1KH FID 输给 AniPortrait、两数据集 CSIM 输给 X-Portrait（照录原值并标注）；**消融**（Fig. 7/8/9/10）**只有定性图示、无定量指标表** |
| 7 | 相关工作与定位 | 关键点/非扩散线（FOMM、Face Vid2vid、DaGAN、TPSM、MCNet）与扩散线（FADM、AniPortrait、X-Portrait）对比表 + 差异要点（在 warp 空间做控制、无需多次去噪） |
| 8 | 局限与启发 | 论文局限：大姿态跨身份重演不佳、驱动视频有肩部运动时可能抖动（Sec. 5 Limitations, p.11）；「论文局限 vs 我们结论」对照表（我方一栏写"未接入，无第一手结论"）；可操作启发展示"warp 空间 + 可插拔小 MLP 控制模块"的复用价值 |
| 9 | 术语与符号表 | implicit keypoint / implicit blendshape / stitching / retargeting / cascade loss；符号 F、M、W、G、K、MAE(°) |
| 10 | 相关文档 | `[[论文笔记/ditto]]`、`[[数字人概述/数字人身份]]`、`[[数字人概述/数字人动作]]`、`[[数字人概述/数字人加速]]`、knowledge 相关专题、papers 库条目、博客 `paper-liveportrait` |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | Figure 2（`pipeline_first_stage_v0618.png`） | 3 方法精析 | Stage I：F/M/W/G 从零训练 |
| 图 2 | Figure 3（`pipeline_second_stage_v0620.png`） | 3 方法精析 | Stage II：冻结主干，只训 stitching 与 retargeting |
| 图 3 | Figure 8（`fig7_opt.png`） | 3 方法精析 | 眼开合可控性（无需驱动帧）与跨重演大眼差校正 |
| 图 4 | Figure 6（`fig6_opt.png`） | 6 实验与结果 | 与扩散类方法的时序一致性差异 |
| 图 5 | Figure 4（`fig4_opt.png`） | 6 实验与结果 | 自重现定性对比：唇动/视线/大姿态/身份 |

- 公式：2–3 个（隐式关键点运动变换、warping、级联损失），LaTeX 以 `analysis/terminology.md` 的「公式与符号」为准，写作时逐项回 PDF 校对。
- Mermaid：1 张推理时序图（源图编码 → 关键点变换 → warping → 解码）。
- 可选（不占图位）：Figure 13 多人场景放第 8 节泛化段落。

## 缺料项与处理

- K 值、损失权重、训练步数、Stage II lr/batch、eyes/lip condition 提取算法 → 正文写「未披露」。
- Table 1（p.3）的星级标注与 12.8ms 口径细节 → 按论文原文照录，不推断口径。
- venue → 不声明会议（首页无标注）。
- `multi-person_opt.png`（7.0MB）等大图若采用须降采样；未采用则不入库。

## Decisions

- **D1 采用 10 节深读骨架**（用户要求完整结构与配图），不走"摘要档"。
- **D2 第 8 节不编造实测**：未接入即写明未接入，只给定位与同源关系。
- **D3 链接回补只在首现处挂一次**（《身份》82、《动作》41、《加速》159/177），同节重复不重复挂。
- **D4 图题与解读**：每图必须标注「论文 Figure N」并写中文解读，图号在正文连续。

## Risks / Trade-offs

- **论文消融仅定性** → 正文明确标注证据性质，不把它写成"已验证的机制增益"。
- **16 页长文里 HTML 与 PDF 存在少量不一致**（页数、Eq. 7 的 `CLOSE/OPEN` HTML bug）→ 一律以 PDF 为准，synthesis 已登记冲突项。
- **图片体积** → 采用 5 张并转 WebP，超限则降采样或替换为不占图位的文字描述。
