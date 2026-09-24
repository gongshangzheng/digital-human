## Context

`论文笔记/` 刚完成 `adaptok.md`（自适应 + 时间因果的 1D 视频分词器）。TivTok 是同一命题的另一半：**不解决因果与预算，而解决"哪些信息可以跨帧复用"**。两篇合起来才构成 `数字人领域问题` 第七章首条目（1D 视觉分词器 → 从视频提身份）的证据面。

对我们最重要的三点：

1. **TIV 的定义是"语义稳定"而不是"像素静止"**——论文 §4.5 用像素交集基线做了对照，并明确说"运动物体只要身份与外观稳定也可进 TIV，TV 只负责姿态、位置等瞬变量"；
2. **这个分解是架构涌现的**：SIF 只改注意力范围（TIV 全局、TV 单帧），没有任何显式的分解监督；
3. **它的编码不是时间因果的**（TV 单帧可见、TIV 全 clip 可见，论文还解释了为什么不用因果掩码：会让 TV 吸收跨帧信息且代价升到 $O(T^2)$）。这一条与 AdapTok 的块级因果正面取舍。

素材：`.cache/article-note/tivtok/`（HTML 正文 259 KB 含全部题注、PDF、5 张原图）。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `tivtok.md` + sidecar，讲清动机（信息论）、分解定义、SIF、IB、跨块复用五段。
- 如实登记四组数字：重建（T512 = rFVD 12.65）、长视频（2.91×、延迟）、生成（16 帧 FVD 99）、TIV 容量与分配权衡（Tab.4/Tab.5）。
- 第 8 节写**与数字人的关系**：§4.5 那条机制的价值与三条限定（定性证据 / TIV 含场景 / 非因果），以及与 AdapTok、Face Vid2vid 的互补关系。
- 保留 5 张原图，其中 §4.5 的 TIV/TV 可视化图是重点。

**Non-Goals：**

- 不复现、不做本地实验；**不宣称 TivTok 能用于身份提取**（只陈述机制与限定，判断留给第七章）。
- 不修改 `数字人领域问题` 第七章正文。
- 不逐格抄录 Tab.6/Tab.7（组件消融与可扩展性）——只在正文引用其结论。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | TivTok: Broadcasting Time-Invariant Tokens for Scalable Video Tokenization |
| 作者 | Weiliang Chen、Yuanhui Huang、Xuebo Wang、Yueqi Duan |
| 单位 | 清华大学 |
| venue / 年份 | arXiv `2606.17590`（v1 2026-06-16）；**未声明 venue** |
| 代码仓库 | 论文未给出（HTML 未见项目页/代码链接） |
| 关键词 | Video tokenization、Temporal redundancy、Video compression、Video generation、Long video modeling |
| papers 库 | 未入库 ⇒ frontmatter 只写 `arxiv_id` |
| 素材 | `.cache/article-note/tivtok/`（HTML 正文、PDF、5 张原图） |

## 2. 一句话价值主张（≤100 字）

视频里的持久内容（背景、一致外观）本来就被逐帧重复编码。TivTok 把 clip 拆成 **TIV token**（跨帧共享语义）与 **TV token**（逐帧残差）：编码器用**非对称注意力范围**（TIV 看全 clip、TV 只看本帧）把分解"涌现"出来，解码器把同一批 TIV **广播**到每一帧并行重建，长视频再把各块的 TIV 平均合并复用。`16×256×256` 上 **rFVD 12.65**，128 帧视频压缩效率 **2.91×**，token 数仅为 downsample 类 tokenizer 的 **1.1%**。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/tivtok.md`，10 节骨架，`order: 180`（当前最大 170 已被并行会话占用，实施前复核）：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表（含"未声明 venue / 无代码"）+ 「papers 库未入库」 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（TIV/TV 分解、SIF、IB、跨块复用） | 列表 | 250 |
| 2 | 问题与动机 | 持久内容被重复表示；信息论论证与"节省随长度增长" | 图 1 + 式 (2) | 600 |
| 3 | 方法精析 | 3.1 前置：holistic tokenizer；3.2 TIV/TV 分解；3.3 SIF（非对称 scope）；3.4 IB（广播解码）；3.5 跨块 TIV 复用 | 图 2 + Mermaid ×2 + 式 (2)–(7) | ≥1500 |
| 4 | 训练与实现细节 | 骨干、分辨率、迭代数、优化器、损失（式 8）、生成侧配置、未披露项 | 10 项配置披露表 | 700 |
| 5 | 推理与系统链路 | 并行编码 → 逐帧解码（TIV 广播 + TV）→ 跨块合并；复杂度 $O(T)$/$O(K)$；长视频延迟 | Mermaid 时序 + 延迟表 | 600 |
| 6 | 实验与结果 | 重建（Tab.1）、长视频（Tab.2）、生成（Tab.3）、TIV 容量（Tab.4）、TIV:TV 分配（Tab.5） | 图 3、图 4、图 5 + 表格 | 1300 |
| 7 | 相关工作与定位 | 图像→视频 tokenizer；分解式 tokenizer（参考帧 / 运动掩码 / 频带） | 谱系表 | 500 |
| 8 | 局限与启发 | 论文自述局限 + **与数字人的关系**（§4.5 机制 + 三条限定 + 与 AdapTok/Face Vid2vid 的互补） | 「能对上 / 缺什么」表 | 900 |
| 9 | 术语与符号表 | 术语 + 符号 + 四处易错命名 | 两张表 | — |
| 10 | 相关文档 | 领域问题第七章、adaptok、face-vid2vid、causal-forcing | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 中 `tivtok.md` 状态改「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 冗余来源：持久内容跨帧重复编码；信息论论证 $H_{\text{indep}}-H_{\text{shared}}=\sum_t I(X_t;C)-H(C)\approx(T-1)H(C)>0$ | HTML §1、式 (2)、Fig 1 题注 | 无缺口 |
| 3.1 | 前置：基于 transformer 的 holistic visual tokenizer（ViT-based SoftVQ-VAE） | HTML §3.1、§4.1 | — |
| 3.2 | TIV（$N_{\text{TIV}}\times D$，跨帧共享）与 TV（$T\times N_{\text{TV}}\times D$，逐帧残差）的定义；论文强调 TIV **不限于像素级静态内容**，可含场景几何、**物体身份**、一致视觉模式 | HTML §3.2 | — |
| 3.3 | SIF：TIV 查询可见全局 scope $\mathcal{G}$、TV 查询只见 $\mathcal{L}_t=[Z_{\text{TIV}},Z_{\text{TV}}^{(t)},X_t]$；**为什么 TV 不用因果掩码**（会吸收跨帧信息 + 代价 $O(T^2)$）；复杂度从 $O(T^2(N_{\text{TIV}}+N_{\text{TV}}))$ 降到 $O(T^2N_{\text{TIV}}+TN_{\text{TV}})$ | HTML §3.3、式 (3)(4) | — |
| 3.4 | IB：$\hat{X}_t=D([Z_{\text{TIV}},Z_{\text{TV}}^{(t)}])$，逐帧并行、解码复杂度 $O(T^2)\to O(T)$ | HTML §3.4、式 (5) | — |
| 3.5 | 跨块：$\bar{Z}_{\text{TIV}}=\frac1K\sum_i Z^{(i)}_{\text{TIV}}$，重排表示后广播解码；token 数下降、复杂度 $O(K^2)\to O(K)$ | HTML §3.5、式 (6)(7)、Algorithm 1 | — |
| 4 | 骨干 ViT-based SoftVQ-VAE（12 层 / 768 / patch 4×8×8 / 3D RoPE）；UCF-101 + K600 混合，100K iters @256²；长视频另训 50K iters；AdamW wd 1e-4、(0.9,0.95)、batch 64、lr 1e-4、5K warmup、cosine；损失 = L1 + 感知 + 对抗（$\lambda_1=1,\lambda_2=0.2$，DINOv2-S 判别器自 30K 起，LeCAM 0.001）；生成侧 LightningDiT（dim 1152、28 层、16 头、patch 1、100K iters、batch 512、lr 1e-4 常数、Euler 50 步、CFG 0.1、shift 2）；硬件与种子**未披露** | HTML §4.1、式 (8) | 未披露项写「未披露」 |
| 5 | 并行编码（**非因果**）→ 逐帧解码 → 跨块 TIV 合并；长视频延迟：32×256×256 下 T128 = 0.20 s、128×256×256 下 0.71 s | §3.3–3.5、Tab.2 | 延迟测量硬件未说明 ⇒ 只报数字与对照 |
| 6 | Tab.1 重建（T512 = 12.65 最低 rFVD；T128 = 128 token / T/P 0.012 / 21.29）；Tab.2 长视频（160/640/1280 token，2.91×）；Tab.3 生成（T1024 = 99、T512 = 101）；Tab.4 TIV 数量（8/4/2/1 → 28.96/39.84/81.18/92.09）；Tab.5 TIV:TV（1:3 / 1:1 / 3:1 → 41.33/64.76/92.09） | HTML §4.2–4.6 与各表 | Tab.6/Tab.7 只引结论不逐格抄 |
| 7 | 两条脉络：图像 tokenizer → 视频 tokenizer；分解式 tokenizer 与本文的根本差别（**涌现的分量** vs 参考帧/运动掩码/频带等人为定义） | HTML §2.1/§2.2、§4.2 末段 | 引用文献只点名 |
| 8 | 论文自述局限（场景切换、非平稳相机、快速变化物体、持久内容少时假设变弱；与更大生成模型联合优化留作未来）+ **我们的三条限定**（定性证据 / TIV 含场景 / 编码非因果）+ 与 AdapTok（因果与预算）和 Face Vid2vid（单图提身份）的互补关系 + 可操作启发 | HTML §4.5、§5 Discussion；`adaptok.md`、`face-vid2vid.md` | 无本地实测 ⇒ 只做机制对照 |
| 9 | 术语/符号 + 易错点（TIV vs TV；SIF 是编码器注意力范围、IB 是解码器广播；TIV 数量 vs TV 档位；时间不变 ≠ 像素不变） | HTML §3 | — |

## 4. 口径与取舍

- **D1 "不变量"的定义要写死**：TIV 抓的是**语义稳定**，不是像素静止（论文用像素交集基线对照）；引用 §4.5 的滑冰者/台球例子时必须带上这一点。
- **D2 "运动物体进 TIV"是定性证据**：论文只给可视化示例，**没有身份判别指标**，也不是"TIV = 身份"。第 8 节必须写清这是待验证线索。
- **D3 编码非因果必须显式写**：TV 单帧可见、TIV 全 clip 可见；论文自己解释了为什么不用因果掩码。这是与 AdapTok 的关键区别，也是接流式时的硬伤。
- **D4 基线数字的二手性**：Tab.3 中 MeBT / PVDM / HVDM / CoordTok+SiT-L/2 的数字**取自 MALT 论文**（原文注明），必须标注。
- **D5 分辨率口径**：主表是 `16×256×256`；Tab.4/Tab.5 是 `128×256×256`；Tab.2 有 `32×256×256` 与 `128×256×256` 两档，且部分基线在 `128×128×128`。不可跨表横比。
- **D6 TIV 平均合并的代价**：跨块复用用的是 TIV 平均（式 6），场景切换时会稀释信息——与 §5 Discussion 的局限呼应，正文要连起来写。
- **可选省略**：Tab.6（组件消融）与 Tab.7（可扩展性）只给一句结论，不展开逐格数字。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/tivtok/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件（`.cache/article-note/tivtok/raw/figures/`） | 用在哪 | 论文图 | 处理 |
|---|---|---|---|---|
| 图 1 | `teaser.png`（2032×1302，2.4 MB） | §2 问题与动机 | Fig 1 | 缩到 ≤1600、转 WebP |
| 图 2 | `pipeline03.png`（1500×824） | §3 方法总览（SIF + IB） | Fig 2 | 转 WebP |
| 图 3 | `token.png`（2037×854，2.1 MB） | §6/§8 TIV/TV 可视化与语义不变性分析（**本篇关键图**） | Fig 5 | 缩到 ≤1600、转 WebP |
| 图 4 | `recon.png`（1883×907，1.7 MB） | §6 长视频重建对比 | Fig 3/4 | 缩到 ≤1600、转 WebP |
| 图 5 | `tivratio.png`（1263×687） | §6 TIV 容量 / 分配权衡 | Fig 7 | 转 WebP |

> 备选：`more-vis.png`（Fig 4 全帧重建）。**发布后需用户目视确认图 1、图 3 的小字可读性。**

**公式**（KaTeX `$$...$$` + 符号表）

1. 信息论动机 `H_indep − H_shared = Σ_t I(X_t;C) − H(C) ≈ (T−1)H(C) > 0`（式 2）
2. 两个 scope `G = [Z_TIV, Z_TV^(1..T), X_1..T]`、`L_t = [Z_TIV, Z_TV^(t), X_t]`（式 3）
3. 编码更新 `Z'_TIV = Attn(Z_TIV, G)`、`Z_TV^(t)' = Attn(Z_TV^(t), L_t)`（式 4）
4. 广播解码 `X̂_t = D([Z_TIV, Z_TV^(t)])`（式 5）
5. 跨块 TIV 合并 `Z̄_TIV = (1/K) Σ_i Z_TIV^(i)`（式 6）
6. 复合损失 `L = L_recon + λ₁L_percept + λ₂λ_∇L_adv`，`λ_∇ = ∇_φ(L_recon+λ₁L_percept) / ∇_φL_adv`（式 8）

**Mermaid**：两张——① 编码/分解/解码数据流（clip → SIF 编码 → TIV+TV → IB 广播解码）；② 长视频跨块流程（K 个 chunk 并行编码 → TIV 平均合并 → 广播并行重建）。

**表格**：10 项配置披露表、TIV/TV 定义对照表、重建表、长视频表、生成表、TIV 容量表、TIV:TV 分配表、「能对上 / 缺什么」对照表、术语表、符号表。

## 6. 引用关系

- `[[数字人概述/数字人领域问题|数字人领域问题]]`（第七章首条目的两篇素材之一）
- `[[论文笔记/adaptok|AdapTok 模型笔记]]`（**成对**：一给因果与自适应预算、一给不变/变分分解）
- `[[论文笔记/face-vid2vid|Face Vid2vid 模型笔记]]`（**成对**：单图提身份 vs 视频 token 提身份）
- `[[论文笔记/causal-forcing|Causal Forcing 模型笔记]]`
- `[[数字人概述/数字人身份|数字人身份]]`（selective sensitivity 判据所在）
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

- [把 TIV 读成"身份分支"] → D1/D2；正文只写"语义稳定，含场景几何与背景，身份是其中一部分"，并标注定性。
- [忽略"编码非因果"] → D3；§3.3 与 §8 各写一次。
- [二手数字当一手] → D4。
- [跨表/跨分辨率横比] → D5。
- [把 SIF 说成显式监督] → §3.3 明确"分解由架构涌现，没有显式监督"。
- [Tab.7 数值未回填] → Non-Goal，只引结论。
- [order 冲突] → 默认 `order: 180`（170 已被占用），实施前用 `docs_order.py list` 复核；并行会话近期持续新增笔记，必要时再顺延。
- [图 1、图 3 小字不可读] → 发布后请用户目视；必要时按面板切分。

## Migration Plan

1. 用户审核本 design（§3 结构、§4 的 D1–D6、§5 五张图与六条公式、§7 的 order 与配图风险）。
2. apply 阶段：5 张原图转 WebP 发布 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py` / `validate-analysis.py` / `check-delivery.py` / 浏览器实测 / `docs_order.py list` / FastAPI 详情接口 / `openspec validate docs-note-tivtok --strict`；任一不过则回退。
4. 本笔记完成后，**两篇素材齐**，再写 `数字人领域问题` 第七章首条目（属 `docs-dh-field-tech-applicability`，含 TIV 身份纯度判据）。
