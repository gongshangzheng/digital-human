## Context

`论文笔记/` 现有 8 篇（`avatar-forcing`、`ditto`、`liveact`、`vorch-streamer`、`liveportrait`、`lia-x`、`float`、`face-vid2vid`），**全部是模型/算法路线**；README 登记的最后十行是一组性质不同的笔记——**生成侧加速**（FPSAttention、BLADE、NAR、FlashAR、LSM、WorldAttention、ZipAR、DAX、TurboDiffusion、Inferix）。它们的素材集中在两处：知识库《视频生成训练与推理加速专题》与博客页 `video-gen-acceleration`，而《数字人加速》正文已经点名这十个工作、**只差文档链接**（伞 change 的 3.1 依赖它）。

FPSAttention 是这十篇的第一篇，也是与我们既有经验最直接相关的一篇：它的加速建立在 **Hopper 的 FP8** 上，而 `liveact` 篇记录的正是「单张 A10 上 FP8 路线不可用」——两边合起来正好构成「硬件依赖」这条选型判据的两个方向。

素材状态：arXiv `2506.04648v2`（HTML + PDF 26 页 + 3 张正文图）；5 个分析 lane（methodology / experiment / local-crosscheck / image-collection / citation）已完成，`validate-analysis.py` 通过（仅 `local-crosscheck` 属自定义 lane 名，触发一条 warning）。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `fpsattention.md` + sidecar，讲清「训练感知的量化 × 稀疏协同设计」：粒度分工、步感知调度、kernel 取向，以及朴素组合为什么会崩。
- 用论文自己的数字建立两条口径：**kernel 与 E2E 两套加速比**（7.09× / 4.96×），以及**朴素组合 −21.1% vs 本文 +1.8%** 的质量对照。
- 把 Limitations 五条逐条写实，并接住我们的一手经验（`liveact` 的 A10 无 FP8），使「硬件依赖」成为可判定的选型条件而不是脚注。
- 如实登记本地素材与论文的出入（博客页两处误置；知识库「VBench 未降」的口径），避免把已发布内容里的错误复制进笔记。

**Non-Goals：**

- 不写接入实测与部署（我们没有这条链路的代码与权重；本篇是纯论文层深读）。
- 不评价另外九篇加速工作（各自独立成篇）；第 7 节只写论文自己的对话对象。
- 不修博客页（另一个仓库）；只在笔记里标注正确口径，并把修正建议留给用户裁决。
- 不补跑实验、不伪造未披露配置（**QAT 步数论文未披露**，只能写「2,000 步后 loss 轨迹几乎一致」这一线索）。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | FPSAttention: Training-Aware FP8 and Sparsity Co-Design for Fast Video Diffusion |
| 作者 | Akide Liu\*、Zeyu Zhang\*、Zhexin Li†、Xuehai Bai†、Yizeng Han、Jiasheng Tang‡、Yuanjie Xing、Jichao Wu、Mingyang Yang、Weihua Chen、Jiahao He、Yuanyu He、Fan Wang、Gholamreza Haffari、Bohan Zhuang‡（\* 共同一作，† 共同二作，‡ 项目负责人） |
| 单位 | Monash University、DAMO Academy (Alibaba Group)、ZIP Lab (Zhejiang University)、Hupan Lab |
| venue / 年份 | **NeurIPS 2025 Spotlight**（arXiv `v2`，2025-06-06） |
| arXiv | `2506.04648v2`（`[cs.CV]`） |
| 项目页 | https://fps.ziplab.co |
| 代码仓库 | 论文正文未给出仓库地址（项目页存在；本篇不写仓库，避免未核实） |
| papers 库 | **未入库**，frontmatter 只写 `arxiv_id`，不写 `papers_id` |

## 2. 一句话价值主张（≤100 字）

**把「量化 + 稀疏」从推理期的朴素叠加挪到训练期的联合优化**：$Q/K$ 按 3D tile 量化、$V$ 按 channel 量化、注意力概率用固定标量，稀疏度与精度按去噪步调度（粗→细→中），再配 Hopper 取向的 kernel——在 Wan2.1-14B/720p/单张 H20 上拿到 **kernel 7.09×、端到端 4.96×**，而朴素组合会把 VBench 总分打掉 21.1%。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/fpsattention.md`，沿用 10 节骨架；与模型笔记的差别在于 §3/§5 的分工改为「算法（§3）↔ kernel 与部署（§5）」：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「papers 库未入库」说明 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条要点（对比动机 / 粒度分工 / 步感知 / kernel） | 列表 | 200 |
| 2 | 问题与动机 | 三段式：视频 DiT 为什么贵 → 量化与稀疏各自的不足 → **朴素叠加更差**（含 §3.1 的机制解释：稀疏保留高幅值 token，而量化误差恰在高幅值处最大） | 图 1 + 一段机制说明 | 700 |
| 3 | 方法精析 | 3.1 tile 与量化粒度分工（$Q/K$ tile-wise、$V$ channel-wise、$P$ 固定标量 $1/448$ 沿用 SageAttention2）；3.2 联合决定量化与稀疏；3.3 步感知调度（$\alpha_1/\alpha_2$ 三段、粗→细→中、推理选参后迁移到训练）；3.4 与硬件对齐的设计取向 | 图 2、图 3 + 式(4)(5)(6) + Mermaid | 1300 |
| 4 | 训练与实现细节 | 十项配置披露表（含 64 节点 × 8×H20 / 7 天、数据过滤阈值、lr/warmup/EMA、FSDP、fp8、序列并行、480p/16fps/5s）；**QAT 步数未披露**的如实标注 | 配置表 | 700 |
| 5 | 推理与系统链路 | 评测口径澄清：**kernel 加速与端到端加速是两套数**；评测基于 480p、§‡ 为 720p 更长序列；采样设置（50 步、CFG 5.0）与硬件（H20/Hopper） | 口径表 + Mermaid 数据流 | 600 |
| 6 | 实验与结果 | Table 1（7.09×/4.96×）、Table 2（1.3B 2.45×、14B 4.96×、PSNR 25.74353）、Table 3 tile size、Table 4 稀疏窗口、Table 5 全 VBench（朴素 −21.1% vs 本文 +1.8%） | 五张表 | 1300 |
| 7 | 相关工作与定位 | 量化线（PTQ 的困难 → QAT 空白）与稀疏线（SparseVideoGen / STA / SpargeAttn / DiTFastAttn）及三点批评；三类基线对照表；**与步数蒸馏正交**（无叠加实测） | 定位表 | 500 |
| 8 | 局限与启发 | Limitations 五条逐条 + §5 的两条边界；**我们的实测对照**（`liveact` 的 A10 无 FP8）；本地素材出入三处；可操作启发 | 「论文边界 vs 我们结论」表 + 口径易错表 | 900 |
| 9 | 术语与符号表 | 术语表 + 符号表 + 六条命名口径（kernel/E2E、SageAttention 定性、VBench ±、硬件口径、附录 E、损失高低） | 两张表 | — |
| 10 | 相关文档 | 知识库专题 + 数字人加速 + 本组其余笔记的清单指向 | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 清单里 `fpsattention.md` 状态改「已完成」。
**不在本 change 内做**：在《数字人加速》正文里把这十个工作名换成文档链接（属伞 change 3.1 的任务，等十篇齐备后一次做完）。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 注意力占推理 >70%、生成 5 秒视频的量级；PTQ 的困难（激活统计随去噪步变化）；稀疏线三点批评（只做推理期、未与训练集成、与量化不兼容）；**朴素叠加的失败机制**与 Table 5 的 −21.1% | `methodology.md` §3.1；`citation.md` 1–2；`experiment.md` Table 5 | 无缺口 |
| 3 | 粒度分工三句话（$Q/K$ tile-wise / $V$ channel-wise / $P$ 固定标量）；3D tile 的选择理由（含「per-group 忽略 GPU compute tile 模式」）；步感知三段的阈值与「推理期选参后迁移到训练」；kernel 四个取向 | `methodology.md` §3.2–3.4、Appendix A/B | 式号以 PDF 为准，正文写「式(4)(5)(6)」并给符号表 |
| 4 | 训练资源（64 节点 × 8×H20 / 7 天 for 14B、16 节点 for 1.3B）、数据过滤阈值、Table 8 全部超参；**QAT 步数未披露** | `experiment.md` A | 未披露项写「未披露」，只保留「2,000 步后 loss 轨迹一致」线索 |
| 5 | kernel/E2E 两套口径；评测分辨率（质量与效率基于 480p，‡ 为 720p 更长序列）；每 prompt 采 5 条视频；16 个 VBench 维度 | `experiment.md` A/B；`terminology.md` 口径 1 | 无缺口 |
| 6 | Table 1/2/3/4/5 逐格；**Table 4 与 Table 3 有一行数值完全相同**（同一组数字，不当两处证据）；Figure 6 定性结论；附录 H 逐帧对比 | `experiment.md` B–D、G | 附录 D 的 VBench 全量表（Table 6/7）压成结论 + 指向 |
| 7 | 量化线/稀疏线的谱系与三点批评；三类基线表；SpargeAtten 是最直接对照；与步数蒸馏正交（**无叠加实测**） | `citation.md` 全文 | 前作机制细节只按论文转述引用，不引其数字 |
| 8 | Limitations 五条（硬件依赖 / 需 QAT / 超参多 / 只验证 Wan2.1 / 硬件细节仍可优化）+ §5 的「仅 Wan2.1」与「与步数蒸馏正交」；**我们的实测**：`liveact` 篇记录 A10 无 FP8 硬件 ⇒ 该路线在 Ampere 上不可用（**注意与论文口径的差别：论文说老硬件仍受益但打折，我们说 A10 上没有可用的 FP8 内核**）；本地素材出入三处；可操作启发 | `experiment.md` F/G；`local-crosscheck.md` 全文；`论文笔记/liveact` | 无本地性能实测 ⇒ 只做机制与选型层面结论 |
| 9 | 术语/符号两表 + 六条口径易错 | `terminology.md` | 无缺口 |

## 4. 口径与取舍

- **D1 kernel 与 E2E 是两套数**：Table 1 的 7.09× / 4.96× 分别是 kernel 与端到端；写的时候每次都要带是哪一个。
- **D2 SageAttention 在本论文里是 INT8 PTQ**，其端到端是 1.91×（1.3B）；**1.26× 属于 FP8 那一行**。本地博客页在这一点上有误置，笔记按论文口径写，并在 §8 记出入。
- **D3 「VBench 未降」要写准**：论文报告总分 **0.8160，相对基线 +1.8%**；同时要写出有下降的维度（如 Background Consistency、Motion Smoothness、Subject Consistency 等），并带上论文给出的解释（局部性归纳偏置 / 量化噪声的正则化效应）。
- **D4 附录 E 不是「VBench 指标失效」**：它讲的是**跨论文分数可比性受限**（随机性、prompt extension、CFG 等）与本文的公平评测口径。这是写作硬约束。
- **D5 不写「老卡跑不了」**：论文原话是老硬件仍能受益、只是 FP8 加速打折。但可以写**我们自己的实测**：A10（Ampere）上不存在 FP8 内核路径（`liveact` 篇），两者要分清是「谁的结论」。
- **D6 训练损失不写「更低」**：Figure 7 图内数字显示基线最低损失更低（0.0830 vs 0.0875），论文表述是「初期略高、最终可比」。
- **D7 Table 3 与 Table 4 有一行数值完全相同**，不当作两处独立证据。
- **D8 本篇是纯论文层**：没有我们的接入链，§8 只做机制与选型对照，不并列吞吐。
- **可选省略**：Appendix A 算法伪码压成一段；Appendix D 的 VBench 全量表只给结论与一两个代表维度。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/fpsattention/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件 | 用在哪 | 论文图 | 发布前处理 |
|---|---|---|---|---|
| 图 1 | `x1.png`（1384×610，193KB） | §2 问题与动机（训练无关 vs 训练感知的质量对比） | Figure 1 | 仅转 WebP |
| 图 2 | `x2.png`（1475×820，279KB） | §3 方法总览（量化与稀疏的联合优化、步感知） | Figure 3 | 仅转 WebP |
| 图 3 | `x3.png`（440×345，26KB） | §3 量化粒度对比（per-token / per-channel / per-group / per-3D-tile） | Figure 4 | 仅转 WebP，不放大 |

**暂不发布**（见待决项 1）：`raw/figures/fig5-p7-300.png`（Figure 5，各去噪步的误差模式，PDF 渲染）与 `fig7-p10-300.png`（Figure 7，训练损失对比）。两张都已在工作区就绪；不发布的理由是**本机无法目视确认渲染后的小字可读性**，且 Figure 5 的信息已由 §3 文字承担。Figure 2 与 Figure 6 在论文里是视频，无法产出静态图。

**公式**（KaTeX `$$...$$` + 符号表）：以 PDF 为准抄录式(4)(5)(6) —— tile 级 scale 的计算、稀疏窗口的注意力形式、步感知的分段调度；另给 $P$ 的固定标量约定。每个公式都配符号解释。

**Mermaid**：两张——① 量化与稀疏的协同数据流（$Q/K/V$ 各自粒度 → 3D tile → 稀疏窗口 → kernel）；② 推理期步感知调度（粗→细→中三段与 $\alpha_1/\alpha_2$ 阈值）。

**表格**：Table 1（效率）、Table 2（质量与效率，含 1.3B/14B 两档）、Table 3（tile size）、Table 4（稀疏窗口）、Table 5（VBench 总分对照：Baseline / Training-Free / FPSAttention）、训练配置披露表、Limitations 五条表、口径易错表、术语表、符号表。

## 6. 引用关系

- `[[knowledge/视频生成训练与推理加速专题|视频生成训练与推理加速专题]]`（本组十篇的公共素材）
- `[[数字人概述/数字人加速|数字人加速]]`（正文已点名这十个工作，链接待补）
- `[[论文笔记/liveact|SoulX-LiveAct 模型笔记]]`（我们的 A10 无 FP8 一手经验，作 §8 对照）
- `[[论文笔记/ditto|Ditto 模型笔记]]`、`[[论文笔记/vorch-streamer|Vorch-Streamer 模型笔记]]`（同为「算得慢怎么办」的另一类解法：空间与范式，而非数值格式）
- `[[knowledge/digital-human-realtime-gpu-comparison|实时数字人 GPU 横评]]`（硬件档位口径）
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

**现状风险与处理**

- [把 kernel 与 E2E 混用] → D1，每次出现都带口径。
- [复制本地素材的误置] → D2 与 §8 的出入表；`local-crosscheck.md` 已给出逐条判定。
- [把「VBench 未降」写成「提升」或反之] → D3：写 +1.8% 并列出下降维度与解释。
- [把附录 E 误读成「VBench 指标失效」] → D4 作为硬约束写进 §6 口径。
- [把我们的 A10 结论与论文的硬件口径混写] → D5，两者分开标注来源。
- [Figure 5 的可读性无法验证] → 默认不发布，见待决项 1。
- [Table 3/4 数值重合被当成两处证据] → D7。
- [本机不支持读图] → 三张发布图的可读性由尺寸推算，仍需你在浏览器里过一眼。

**待决项（需用户裁决）**

1. **是否发布 Figure 5 与 Figure 7**：两张已从 PDF 渲染到工作区（`fig5-p7-300.png`、`fig7-p10-300.png`）。默认**不发布**（可读性无法验证、且核心论证已由文字承担）；若你目视确认可读，我就把它们作为图 4/图 5 加进 §3.3 与 §4。
2. **order 取值**：**改为 100**。原默认 70 与并行会话新增的 `omnimate` 撞号（同批并行写入各自选了 70）；按「占空位、不动既有文档」的规则挪本方。100 作为**加速组的起点**，与模型笔记当前的 10–80 分段隔开，后续九篇依次取 110、120…
3. **博客页两处错误的修正**：位于另一个仓库（`~/gongshangzheng.github.io`，已发布站点），本 change 不处理。要不要我另开一个任务去修（改 `video-gen-acceleration.html` 的 1.26× 归属与「A10 跑不了完整版」两处）？
4. **是否在《数字人加速》补链接**：那是伞 change 3.1 的任务，需要等十篇齐备；本篇只改 README 清单一行。

## Migration Plan

1. 用户审核本 design（尤其第 3 节架构、第 5 节配图、第 7 节待决项）。
2. apply 阶段：`figures.py convert/publish` 发布 3 张图 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`check-delivery.py`、浏览器实测（3 图解码 / 公式 / Mermaid）、`docs_order.py list management/docs/论文笔记`（order 无重复）、`openspec validate docs-note-fpsattention --strict`；任一不过则回退本次改动。
