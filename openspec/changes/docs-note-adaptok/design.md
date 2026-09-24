## Context

`论文笔记/` 已有 10 篇（流式/实时路线 7 篇 + 刚完成的 `causal-forcing`）。本篇是**第一篇"视觉分词器"类笔记**，也是 `数字人领域问题` 第七章首条目（1D 视觉分词器 → 从视频提身份）的两篇素材之一。

它对我们判断的价值集中在两点，都不是"它多好"，而是"它的设计对我们意味着什么"：

- **分配依据是重建质量，不是判别性**：AdapTok 用感知损失做 token 分配的分数，整套机制里没有任何身份/判别监督；
- **因果性是块级**：block-causal（K=4 块、每块 4 帧），不是帧级因果——接进流式管线的最小延迟粒度由此确定。

素材：`.cache/article-note/adaptok/` 下 HTML 正文（284 KB，含全部图表题注）、PDF（22 页）、5 张原图；另有博客 `drafts/adaptok.md` 快读草稿可作二手核对源。arXiv 的 LaTeX source 抓取失败（HTTP 406），因此公式以 HTML 为准，必要时对照 PDF。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `adaptok.md` + sidecar，讲清三段机制：自适应 tokenizer（含训练期 mask 采样）、adaptive scorer、IPAL（ILP 分配）。
- 用数字说话：重建 rFVD、生成 gFVD、模型规模、三组消融、延迟对比；并说明"自建 CausalTok 基线"的性质与公平性口径。
- 第 8 节写**与数字人的关系**：两个特性各自对上什么约束、缺什么（无解耦机制）、块级因果的延迟含义、以及用它做身份表示前必须先验证的两条判据。
- 保留 5–6 张原图，每图配图题与正文解读。

**Non-Goals：**

- 不复现、不做本地实验；不宣称 AdapTok 能用于身份提取（那是第七章要判断的，本篇只提供事实与判据）。
- 不修改 `数字人领域问题` 第七章正文（另一个 change）。
- 不写与 ElasticTok 的逐项对标细节到表格之外的程度（只在 §6/§8 引用）。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Learning Adaptive and Temporally Causal Video Tokenization in a 1D Latent Space |
| 作者 | Yan Li\*、Changyao Tian\*、Renqiu Xia、Ning Liao、Weiwei Guo、Junchi Yan、Hongsheng Li、Jifeng Dai、Hao Li†、Xue Yang†（\* 同等贡献，† 通讯） |
| 单位 | 上海交通大学、香港中文大学 MMLab、上海 AI Lab OpenGVLab、同济大学、清华大学 |
| venue / 年份 | arXiv `2505.17011`（v1 2025-05-22；v2 2025-10-14）；PDF 标注 Preprint–Under review，会议未确认 |
| 项目页 / 代码 | 代码 `https://github.com/VisionXLab/AdapTok` |
| 会议状态 | **未确认**（OpenReview 有评审页，最终收录未见） |
| papers 库 | 未入库 ⇒ frontmatter 只写 `arxiv_id` |
| 素材 | `.cache/article-note/adaptok/`（HTML 正文、PDF 22 页、5 张原图） |

> 作者口径核对：OpenAlex 该 arXiv-DOI 记录把第一作者写成 Menqqi Li，与论文 HTML 的 `Yan Li` 不符——以论文为准（本笔记不采用 OpenAlex 的作者字段）。

## 2. 一句话价值主张（≤100 字）

固定 token 预算会把预算浪费在时间冗余上——静止背景与剧烈运动片段拿同样多的 token。AdapTok 让 tokenizer 在**训练期**以随机块掩码学会变长编码，在**推理期**用 block-causal 打分器预测不同 token 数的重建质量，再用**整数线性规划**在全局预算下把 token 分配给最需要的块；`16×128×128` 上 1024 token 得 **rFVD 36**（自建基线 CausalTok 37、ElasticTok 230），延迟 **50.9 ms** 对比 ElasticTok **571.7 ms**（11×）。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/adaptok.md`，10 节骨架，`order: 90`（现有最大 80，见 §7 风险项）：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 会议状态 + 作者口径说明 + 「papers 库未入库」 | 表格 | 180 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（变长训练 / 块因果打分器 / ILP 分配 / AR 生成验证） | 列表 | 250 |
| 2 | 问题与动机 | 固定预算的时间冗余；已有 causal tokenizer 都是固定分配 | 图 1 + 冗余示意 | 600 |
| 3 | 方法精析 | 3.1 自适应 tokenizer（3D patchify + block causal transformer + 训练 mask 采样）；3.2 adaptive scorer（GT 分数构造 + 打分器）；3.3 IPAL（ILP 形式化 + 三种替代策略）；3.4 AR 生成 | 图 2 + Mermaid ×2 + 式 (4)/(5)/(6)/(7) | ≥1500 |
| 4 | 训练与实现细节 | 分辨率/块/patch/码本/优化器/步数/数据集/模型规模/AR 模型 | 10 项配置披露表 | 700 |
| 5 | 推理与系统链路 | 编码 → 打分 → ILP 分配 → 截断 → 解码；块级因果的延迟含义 | Mermaid 时序 + 延迟表 | 600 |
| 6 | 实验与结果 | 重建（Tab.1）、生成（Tab.2）、规模（Tab.3）、自适应消融（Tab.4）、延迟（Tab.5）、分配策略（Tab.6）、打分指标（Tab.7） | 图 3、图 4 + 表格 | 1200 |
| 7 | 相关工作与定位 | 离散视频 tokenizer（MAGVIT / OmniTokenizer / Cosmos / VidTok / ElasticTok）与自适应 tokenizer（LaViT / ElasticTok） | 谱系表 | 500 |
| 8 | 局限与启发 | 论文自述局限 + **与数字人的关系**（两特性对上什么、缺什么、块级因果、两条待验证判据） | 「能对上 / 缺什么」表 | 900 |
| 9 | 术语与符号表 | 术语 + 符号 + 易错命名 | 两张表 | — |
| 10 | 相关文档 | 领域问题第七章、causal-forcing、ditto/liveact、FLOAT（运动隐空间对照） | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 中 `adaptok.md` 状态改「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 冗余来源：固定预算对静止背景与剧烈运动一视同仁；已有 causal tokenizer（ElasticTok / OmniTokenizer / Cosmos）均固定分配 | HTML 摘要、§1、Fig 1 题注 | 无缺口 |
| 3.1 | 3D patchify：patch 4×8×8 → L=1024 token/clip；分 K=4 块、每块 M=512；block causal transformer；训练期 block-wise mask sampler 从截断高斯（μ=256、σ=128、界 [32,512]）采样每块 token 数 | HTML §3.1（含 3.1.1–3.1.3）、§4.1 | source 失败 ⇒ 公式按 HTML 文本给出，必要时对照 PDF |
| 3.2 | GT 分数构造：采样目标块 q、复制 latent 序列、施加一系列 latent mask（前块长度随机、后续块全掩），以感知损失为分数；打分器 S_φ 为 block-causal transformer encoder，输入连续+量化 token，一次前向预测该块所有候选长度的分数；MSE 训练 | HTML §3.2，式 (4)(5) | — |
| 3.3 | IPAL：二值变量 b_kj、目标 min Σ ŝ_kj·b_kj、约束①每样本恰选一个长度 ②总预算 B·N_b；最优解给出每样本 token 数；三种替代策略 Fixed / BiThr / BiDelta 与 ILP 的对比 | HTML §3.3、Algorithm 1、附录 B.2、Tab.6 | 别把 ILP 说成"最优分配"而无条件——它优化的是**预测感知损失之和** |
| 3.4 | 每块末尾附 `<EOB>`，拼接后送 Llama 式 transformer 自回归；交叉熵损失 | HTML §3.4，式 (7) | — |
| 4 | `16×128×128` 训练与评测；patch 4×8×8；L=1024；K=4 / M=512；码本 8,192；UCF-101 + Kinetics-600（5 帧条件）；250 epochs、batch 128、Adam β1=0.5/β2=0.9、lr 1e-4 余弦退火到 1e-6；变体 S/L/XL = 59M/259M/913M；AR 模型 633M；训练硬件与随机种子**未披露** | HTML §4.1、Tab.3、附录 A | 未披露项写「未披露」 |
| 5 | 推理链：编码 → scorer 预测 → ILP 分配 → 按分配截断 latent → 解码；块级因果（每块 4 帧）决定流式最小粒度；延迟 50.9 vs 571.7 ms/video（Tab.5） | HTML §3.3/§4.3、Tab.5、Fig 1 题注 | 延迟测量硬件需从附录核对；未核实则只给相对倍数 |
| 6 | Tab.1 重建 rFVD：AdapTok 512/1024/2048 = 60/36/28，CausalTok† 37、ElasticTok† 230、OmniTokenizer† 94、ElasticTok 390/93、OmniTokenizer 42、Cosmos 140；Tab.2 生成 gFVD：K600 = 11、UCF = 67（633M 参数）；Tab.3 规模；Tab.4 自适应机制（1024 行 37.13 → 38.79 → 36.36；512 行 509.95 → 121.88 → 59.96）；Tab.6 分配策略（Fixed 38.79 / BiThr 42.12 / BiDelta 38.13 / ILP 36.36）；Tab.7 打分指标（感知损失最好） | HTML §4.2/§4.3 与各表 | 带宽/分辨率口径差异（16×128×128）必须写明，避免与他篇 256² 数字横比 |
| 7 | 两条脉络与差异；本文定位：把"自适应分配"从图像侧（LaViT 一类）搬到**时间因果的视频 token** 上 | HTML §2.1/§2.2 | 引用文献只点名，不给数字 |
| 8 | 论文自述局限（若有）；**与数字人的关系**：① AdapTok 的对上项=块级时间因果 + 预算按内容密度分配（流式与算力）；② 缺项=没有任何身份/判别监督，也没有"跨帧不变 vs 逐帧变化"的分解（后者是 TivTok 的机制）；③ 块级因果 ⇒ 流式最小延迟 ≈ 4 帧；④ 两条待验证判据：token 分配是否与身份信息量相关（很可能相关的是运动/复杂度）、跨条件身份 token 的可比性 | HTML §5 结论 + `数字人领域问题` 第七章首条目的判据设计 | 无本地实测 ⇒ 只做机制对照，不宣称可用于身份 |
| 9 | 术语/符号 + 易错点（tokenizer vs AR 生成器；block causal vs frame causal；IPAL 是推理期策略、不是训练；`<EOB>`；rFVD vs gFVD） | HTML 各节 | — |

## 4. 口径与取舍

- **D1 分配依据是重建质量**：全文凡涉及"token 分配"，都要点明依据是**感知损失**这一重建质量分数，不是判别性、不是身份。第 8 节由此推出"身份信息量与分配策略是否相关"这条待验证判据。
- **D2 块级因果要说清**：K=4 块、每块 4 帧（Fig 1 题注），因此时间因果的粒度是**块**而非帧；接流式管线的最小延迟按块计。
- **D3 自建基线要标明**：CausalTok† 与 ElasticTok†/OmniTokenizer† 是作者**同数据同配方复现**的版本，与原始论文数字不可混读；Tab.1 的 Data size 列（<0.5M）必须一并呈现。
- **D4 分辨率口径不同**：本文为 `16×128×128`；与他篇常见 `256²` 的 rFVD 不能直接横比，需显式标注。
- **D5 ILP 的说法要收着**：它优化的是"预测的感知损失之和在预算约束下的最小化"，不是"最优 token 分配"；BIThr/BiDelta/Fixed 是消融对照。
- **D6 会议状态写"未确认"**：只写 arXiv 与"Preprint–Under review"，不写"被 XX 接收"。
- **可选省略**：附录的量化方法与更多可视化（Fig 7–13）只在正文各引用一句，不逐图展开。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/adaptok/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件（`.cache/article-note/adaptok/raw/figures/`） | 用在哪 | 论文图 | 处理 |
|---|---|---|---|---|
| 图 1 | `adaptive_vis_fig1.png`（2.4 MB） | §2 问题与动机（时间与样本双向自适应） | Fig 1 | 缩到 ≤1600、转 WebP |
| 图 2 | `framework.png`（575 KB） | §3 方法总览（含 scorer 与 mask 示意） | Fig 2 | 转 WebP |
| 图 3 | `fvd_compare_curve.png` | §6 不同 token 预算下的 rFVD | Fig 3 | 转 WebP |
| 图 4 | `ab2_token_allocation_metrics1.png` | §6 分配策略对比 | Fig 4 | 转 WebP |
| 图 5 | `attn_map.png` | §6/§8 隐 token 的注意力分布（与"token 学什么"相关） | Fig 5 | 转 WebP |

> 备选：`figs_compare_with_elastictok.png`（Fig 7）、`vis_scores.png`（Fig 6/13）、`vis_content_aware.png`、`vis_temporal_dynamics.png`。后两者在 HTML 里的相对路径不同（`images/` 前缀），实施时按实际 URL 抓取；若抓不到就退回博客已有的 `drafts/assets/adaptok/vis.png`（1652×1041）。**发布前需用户目视确认图 1、图 2 的小字可读性。**

**公式**（KaTeX `$$...$$` + 符号表）

1. latent mask 构造 `m'_p = [m_{p,1} ⊕ … ⊕ m_{p,q} ⊕ 0]`（式 4，GT 分数生成）
2. 打分器前向 `ŝ = S_φ(z ⊕ z_q, M'_s)_{qM:(q+1)M}`（式 5）
3. IPAL 的 ILP：`min_b Σ ŝ_kj b_kj` s.t. `Σ_j b_kj = 1 ∀k`、`Σ_kj j·b_kj = B·N_b`（式 6）
4. 每样本 token 数 `n_k = Σ_j j · b*_kj`（式 6 后）
5. AR 生成损失 `L = −Σ_i log P(ŷ_i | c, y_{1:i−1}; θ)`（式 7）

**Mermaid**：两张——① tokenizer 训练/推理数据流（patchify → block causal encoder → mask 采样/scorer → 量化 → 块因果解码）；② 推理期分配与解码时序（编码 → scorer → ILP → 截断 → 解码，标出块边界与 `<EOB>`）。

**表格**：10 项配置披露表、块与 token 口径表、重建 rFVD 表、生成 gFVD 表、模型规模表、自适应消融表、分配策略表、打分指标表、「能对上 / 缺什么」对照表、术语表、符号表。

## 6. 引用关系

- `[[数字人概述/数字人领域问题|数字人领域问题]]`（第七章首条目的两篇素材之一）
- `[[论文笔记/causal-forcing|Causal Forcing 模型笔记]]`（同为"因果 + 蒸馏/表示"这条线）
- `[[论文笔记/float|FLOAT 模型笔记]]`（运动隐空间：与本篇"token 空间"对照）
- `[[论文笔记/liveact|SoulX-LiveAct]]`、`[[论文笔记/ditto|Ditto]]`（实时流式的另一条路线）
- `[[数字人概述/数字人加速|数字人加速]]`
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

- [把 tokenizer 的"自适应"读成"自适应地保身份"] → D1；第 8 节明确写"分配依据是重建质量"。
- [把块级因果当帧级因果] → D2；图示与正文都标块边界。
- [自建基线与原论文数字混读] → D3；表格保留 Data size 列与 `†` 标记。
- [跨分辨率横比] → D4。
- [把 ILP 说成最优解] → D5。
- [会议状态写错] → D6。
- [LaTeX source 抓取失败导致公式不准] → 公式以 HTML 为准并对照 PDF；若发现 HTML 公式排版破碎，则在正文用 fenced `text` 保留原始 TeX 并加中文说明。
- [order 冲突] → 现最大 `order: 80`（causal-forcing）；本笔记默认 **`order: 90`**，实施前用 `docs_order.py list` 复核（并行会话可能新增）。
- [图 1 体量大（2.4 MB）] → 转换后须 ≤500 KB；若压不下去则降到 6 张中更小的替代图。

## Migration Plan

1. 用户审核本 design（尤其 §3 结构、§4 的 D1–D6、§5 五张图与五条公式、§7 的 order 与配图风险）。
2. apply 阶段：把 5 张原图转 WebP 并发布 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`validate-analysis.py`、`check-delivery.py`、浏览器实测（图/公式/Mermaid）、`docs_order.py list`、FastAPI 详情接口、`openspec validate docs-note-adaptok --strict`；任一不过则回退。
4. 本笔记完成后，再做 **TivTok** 的 change；两篇都完成后才写 `数字人领域问题` 第七章首条目（属 `docs-dh-field-tech-applicability`）。
