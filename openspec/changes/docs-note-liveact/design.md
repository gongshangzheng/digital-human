## Context

`论文笔记/` 现有 `avatar-forcing` 与 `ditto` 两篇，都落在「运动空间/潜在空间 + 流式」这条线上。`liveact` 是 README 待写清单的第一步，也是三条路线里的第三条：Avatar Forcing 用块因果 + 历史 offset，Ditto 用参考锚定渲染，SoulX-LiveAct 则把问题定义为「AR 链上该传播什么表示」（ARPP），并用 ConvKV 把历史压成定长记忆。

素材三类齐备：论文（arXiv `2603.11746v2`，7 张原图，55k 字符派生正文）、代码（CyberVerse `models/SoulX-LiveAct/`）、第一手实测（单卡 A10 两组完整跑通记录）。分析阶段 4 个委派 lane + 2 个自写 lane 已完成，`validate-analysis.py` 通过。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `liveact.md` + sidecar，讲清 ARPP 视角下 Neighbor Forcing 与 ConvKV Memory 的机制，并用论文表格数字支撑。
- **如实登记论文自身的三处内部不一致**，让笔记成为可信的第一手整理，而不是论文摘要的复述。
- 把工程层写成**两条不同路径**：官方 `generate.py` 单卡路线（我们跑通）与 CyberVerse `avatar.live_act` 插件路线（多卡硬门槛、未在 A10 跑通），并给出第一手 A10 数字。

**Non-Goals：**

- 不把论文的 2×H100/FP8 官方口径与我们单卡 A10 的 bf16 数字混排成同一张性能表。
- 不写 Talker-T2AV / OmniMate 等其他模型的对比（各自独立成篇）。
- 不补跑实验、不伪造未披露配置；论文没有 Limitations 节这一点要写成事实而非推断。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | SoulX-LiveAct: Towards Hour-Scale Real-Time Human Animation with Neighbor Forcing and ConvKV Memory |
| 作者 | Dingcheng Zhen\*†、Xu Zheng\*、Ruixin Zhang\*、Zhiqi Jiang\*、Yichao Yan、Ming Tao、Shunshun Yin（\* 同等贡献，† 通讯） |
| 单位 | Soul AI Lab（中国）、HKUST(GZ)、Soochow University |
| venue / 年份 | 本地 arXiv `v2` 未声明 venue（页首为 `arXiv:2603.11746v2 [cs.CV] 18 Mar 2026`） |
| arXiv | `2603.11746v2`（HTML/PDF 均为 v2） |
| 项目页 | https://soul-ailab.github.io/soulx-liveact/ |
| 代码仓库 | https://github.com/Soul-AILab/SoulX-LiveAct；**我们接入的是 CyberVerse `models/SoulX-LiveAct/`**（锚定 `4968280`） |
| papers 库 | `arxiv-2603.11746` |
| 素材 | `.cache/article-note/liveact/`（paper.txt 派生自 HTML v2、PDF、7 张原图、6 lane 分析） |

## 2. 一句话价值主张（≤100 字）

把争论点从「是否自回归」移到**沿 AR 链传播什么**：用**同一步**的时间邻居 latent 做条件（Neighbor Forcing），使所有 block 共享一个扩散步、可复用 KV，训练不再需要 ODE 初始化；再用**对 K/V 做轻量 1D 卷积**的 ConvKV Memory 把历史压成定长记忆，换来**常数内存的小时级实时生成**（2 卡 20 FPS，27.2 TFLOPs/帧）。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/liveact.md`，沿用 10 节骨架，落点如下：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 与我们接入版本的说明 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（ARPP 重述 / Neighbor Forcing / ConvKV / 系统实时化） | 列表 | 200 |
| 2 | 问题与动机 | 论文自述的两个挑战（传播表示的**扩散步不匹配**、历史表示**无界且无结构**）；Figure 1 的零样本现象 | 图 1 + ARPP 定位表（Table 1） | 600 |
| 3 | 方法精析 | 3.1 整体与块级 AR（式(1)、两阶段训练）；3.2 Neighbor Forcing（式(2)(3)(4)、step alignment、掩码）；3.3 ConvKV Memory（卷积压缩、固定长度记忆、推理管线） | 图 2、图 3 + 式(1)(2)(3)(4) + Mermaid | 1400 |
| 4 | 训练与实现细节 | 十项配置披露表；主干与初始化来源；**蒸馏步数 400 vs 300 的如实标注**；未披露项清单 | 配置表 | 700 |
| 5 | 推理与系统链路 | 3-step 推理、KV 复用与压缩的推理时序、FP8/序列并行/算子融合、20 FPS 门槛（<50ms/帧） | 图 3 回链 + Mermaid + Table 5 | 600 |
| 6 | 实验与结果 | Table 2 主结果（含 EMTD 的 FID/FVD 异常）、Table 3 效率、Table 4/5 与四组消融、定性结论与失败标签 | 图 4–7 + 四张表 | 1200 |
| 7 | 相关工作与定位 | AR 视频生成线（Teacher Forcing → Diffusion Forcing → Self Forcing → Self-Forcing++ / Self-Resampling）与记忆压缩线（FramePack 等） | 两轴定位表 | 500 |
| 8 | 局限与启发 | 论文未设 Limitations 一节（事实）；EMTD 的 FID/FVD 与正文回避；两个挑战的残留；**我们的实测**（两条接入路径、A10 数字、走不通的路）；可操作启发 | 「论文缺口 vs 我们结论」表 + 本地 A10 冒烟表 | 900 |
| 9 | 术语与符号表 | 术语表 + 符号表 + 命名易错（`Ours` / `Neighbor-forcing` / `SoulX-LiveAct`） | 两张表 | — |
| 10 | 相关文档 | knowledge 六篇 + 数字人概述三篇 + 两篇对照笔记 | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 清单里 `liveact.md` 状态由「待写」改为「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点（只写有据可查的） | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 两个挑战的原文表述；Figure 1 的零样本现象（既有 forcing 不训练就出不了连贯视频 vs 同一步邻居零样本可行）；Table 1 的 ARPP/KV Reuse 两列 | `methodology.md` A/§1.4；`citation.md` 1–2；图 `intro` | 无缺口 |
| 3 | 式(1) 的逐项含义（含 $x_t^{1:n-1}$ 带下标 $t$ 的关键读法）；式(2) flow-matching 加噪；式(3)→式(4) 从「逐块各一步」到「全链一步」；ConvKV = 逐通道 1D 卷积、kernel=stride=5、常数初始化 1/5 ⇒ 5× 压缩 | `methodology.md` 1.2/2.2/2.3；`code-analysis.md` D | $m$（每块 chunk 数）论文与代码口径需并列标注 |
| 4 | 初始化（Wan2.1 + InfiniteTalk）、Stage 1（300 小时）、Stage 2（DMD、3-step）、评测集与指标；**400 vs 300 两处并存** | `experiment.md` A、F3；`methodology.md` 1.5 | 总机时/种子/代码与权重的完整清单未披露 ⇒ 写「未披露」 |
| 5 | 20 FPS 的前置约束（<50ms/帧）、Table 5 的 6/8 组合、FP8/序列并行/算子融合、ConvKV 仅增 1.9% | `experiment.md` C/F4；`methodology.md` 1.6 | 论文无「生成 1 小时」实测数字 ⇒ 明写「机制论证，非实测」 |
| 6 | Table 2 逐格数字与「EMTD 的 FID/FVD 最差」；Table 3 的 20 FPS / 0.94s / 2 卡 / 27.2 TFLOPs；Table 4 训练成本对比；失败标签（ID Drift / Lost of Ring / Texture Drift / Color Drift） | `experiment.md` B/C/E/F | VBench-2.0 细分维度只在正文 ⇒ 标注「主表无对应列」 |
| 7 | 两条脉络与「与 Self Forcing 的差别在 ARPP 而非是否 AR」 | `citation.md` 1–3、6 | 前作文献编号未逐一核实 ⇒ 只点名不给数字 |
| 8 | 无 Limitations 节；EMTD 异常；两条接入路径（官方 `generate.py` vs 插件 `world_size>1` 需 torchrun）；A10 两组冒烟（42/42、0.8–0.9 FPS、10.4 GiB、113/125 GiB 主机内存；416×720 为 43/43、0.67 FPS、11.7 GiB、118 GiB）；主机内存构成；A10 无 FP8 ⇒ FP8 路线作废；5090 ≈6 FPS 与 2×H100 20 FPS 的官方口径 | `code-analysis.md` A/B/C/D；`experiment.md` G | 插件路径未在 A10 跑通的表述必须与官方直跑区分 |
| 9 | 术语/符号两表 + 三条命名易错（方法名三种写法、$m$ 歧义、hour-scale 非实测） | `terminology.md` | 无缺口 |

## 4. 口径与取舍

- **D1 论文内部不一致必须写成事实**：三处（EMTD 段引用 97.6/63.0 实为 HDTF 行数字；EMTD 的 FID 80.90 / FVD 771.6 为全文最差且正文回避；蒸馏步数 400 vs 300）。写在对应小节内，不集中成一个「纠错」小节。
- **D2 本地实测与论文口径分开成表**：A10 的 bf16 数字属我们，2×H100/FP8 的 20 FPS 属论文；第 8 节两张表并列且各标来源与硬件。
- **D3 两条接入路径不合并**：官方 `generate.py`（单卡，已跑通）与 CyberVerse 插件（`world_size>1` 必须 torchrun，未在 A10 跑通）。禁止写成「LiveAct 接入完成」。
- **D4 hour-scale 只写机制论证**：记为「常数内存 + 定长 KV 的机制论证」，不写成已验证的时长指标。
- **D5 工程层压在第 8 节**：TRT/offload 细节、内存构成、被推翻的路线只保留结论与外链，细节留给 `knowledge/` 与 `数字人概述/数字人加速`。
- **D6 代码级事实不写行号**，只写文件与功能（避免随代码漂移失效）。
- **可选省略**：Appendix A 的数学推导压成一句加结论；Appendix B 的文献逐篇导读写进第 7 节的两线谱系，不逐篇展开。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/liveact/`，WebP，最长边 ≤1600px、单图 ≤500KB；原始 9.26MB 需转换）

| 笔记图号 | 源文件 | 用在哪 | 论文图 | 发布前处理 |
|---|---|---|---|---|
| 图 1 | `intro.png` | §2 零样本现象 | Fig 1 | 缩到 1600 + WebP |
| 图 2 | `method_overall.png` | §3 总览与两阶段 | Fig 2 | 缩到 1600 + WebP |
| 图 3 | `method_memory.png` | §3 ConvKV Memory（含推理管线，§5 回链） | Fig 3 | 缩到 1600 + WebP |
| 图 4 | `lip_action_quality.png` | §6 唇动与情绪-动作定性 | Fig 4 | 仅压体积 |
| 图 5 | `compare2.png` | §6 长视频一致性（含 ID Drift 等标签） | Fig 5 | 缩到 1600 + WebP |
| 图 6 | `ab1.png` | §6 ConvKV 消融（Texture/Color Drift） | Fig 6 | 缩到 1600 + WebP（压缩比要求最高） |
| 图 7 | `ab2.png` | §6 情绪与动作编辑模块 | Fig 7 | 仅压体积 |

每图必须有图题与正文解读；图号按笔记出现顺序重排，不沿用论文 Figure 编号。

**公式**（KaTeX `$$...$$` + 符号表）

1. 块级 AR 与条件：$\hat{x}^{1:N}=\{\Psi_{T:0}(G_\theta,\,c^n,\,t)\mid n=1,\dots,N\}$，$c^n=\{x_{ref},\,x_t^{1:n-1},\,c_{audio},\,c_{text}\}$（式 1）
2. Flow-matching 加噪：$x_t^n=(1-t)x_0^n+t\epsilon^n,\ \epsilon^n\sim\mathcal{N}(0,I)$（式 2）
3. 同一步条件的训练损失：$\mathcal{L}(\theta)=\mathbb{E}\left[\lVert(\epsilon^n-x^n)-G_\theta(x_t^n,\,t\mid x_t^{1:n-1})\rVert^2\right]$（式 3）
4. 全 block 共享同一步的简化形式（式 4，含块级因果掩码）
5. 块大小与实时约束的对照（不写成公式，用 Table 5 原文表格）

**Mermaid**：两张——① 训练/推理数据流（3D VAE → block AR → ConvKV 压缩 → 输出）；② 推理时序（前两个 block 不压缩、第三次迭代起启用压缩）。

**表格**：十项配置披露表、ARPP 定位表（Table 1）、主结果表（Table 2，含 EMTD 异常标注）、效率表（Table 3）、消融表（Table 4/5）、本地 A10 冒烟表、官方硬件口径表、论文内部不一致与缺口对照表、术语表、符号表。

## 6. 引用关系

- `[[knowledge/cyberverse-realtime-digital-human-agent|CyberVerse 工程专题]]`、`[[knowledge/digital-human-engineering-benchmark|数字人工程解读（四）]]`、`[[knowledge/模型探索与未采纳实验复盘|模型探索与未采纳实验复盘]]`
- `[[knowledge/digital-human-realtime-gpu-comparison|实时数字人 GPU 横评]]`、`[[knowledge/视频生成训练与推理加速专题|视频生成训练与推理加速专题]]`、`[[knowledge/hardware-assessment|硬件评估]]`
- `[[数字人概述/数字人领域问题|数字人领域问题]]`、`[[数字人概述/数字人加速|数字人加速]]`、`[[数字人概述/数字人行业全景|数字人行业全景]]`
- 对照篇：`[[论文笔记/avatar-forcing|Avatar Forcing 模型笔记]]`、`[[论文笔记/ditto|Ditto 模型笔记]]`
- sidecar `related`：`papers/arxiv-2603.11746`、上述 knowledge/数字人概述条目、两张对照笔记；`changelog` 记首次创建。

## 7. 风险与待确认项

**现状风险与处理**

- [论文数字内部不一致被误当成笔误略过] → D1，三处都写进对应小节并给 PDF 页码。
- [把 A10 与 2×H100 的数字混排] → D2 两张表分开，各标硬件与精度路径。
- [把「插件接通」写成「已跑通」] → D3；第 8 节明确「插件路径未在 A10 跑通」。
- [hour-scale 被写成绩效指标] → D4。
- [图内小字可读性未验证] → 本机模型不支持读图，`ab1.png`（2043px 多面板）与 `compare2.png` 的图内标签需你在发布前目视确认；不可读时改为正文转录标签（ID Drift / Lost of Ring / Texture Drift / Color Drift）。
- [论文无 Limitations 节] → 写成事实，并从 §3.2 失败模式与 §3.3 消融里提取边界，不编造作者的局限自述。
- [$m$（每块 chunk 数）口径未落定] → 实施前从论文 §3 与代码配置双向核对；若不一致则两处并列标注。

## Migration Plan

1. 用户审核本 design（尤其第 3 节架构、第 5 节配图与公式、第 7 节风险项）。
2. apply 阶段：`figures.py inspect/convert/publish` 发布 7 张图 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`check-delivery.py`、浏览器实测（图片/公式/Mermaid）、`docs_order.py list management/docs/论文笔记`、`openspec validate docs-note-liveact --strict`；任一不过则回退本次改动。
