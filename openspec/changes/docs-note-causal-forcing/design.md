## Context

`论文笔记/` 已有七篇流式/实时路线笔记（`avatar-forcing` 块因果 + 历史 offset、`ditto` 参考锚定、`liveact` Neighbor Forcing/ConvKV、`liveportrait`、`lia-x`、`float`、`face-vid2vid`）。本篇是**第八篇**，也是其中唯一一篇**纯后训练/蒸馏理论**取向的工作：它不提出新的生成架构，而是论证"把双向基座蒸成因果学生"这件事**错在哪**。

来源：它是我们查 `Avatar Forcing`（`2601.00664`）被引列表时的最高被引后续工作（Semantic Scholar `2602.02214` 被引 134），已登记进待读清单，本次按 article-note 流程读第一篇。

与既有材料的关系有且只有一处需要"我们判断"：本文的中心命题（diffusion forcing 存在训练-推理分布失配、会塌陷）与我们 `avatar-forcing` 笔记的实测结论**方向相反**——Avatar Forcing 用 block-causal diffusion forcing 训运动隐变量，且在我们的消融里比普通自回归扩散稳定得多。这一处必须写进第 8 节，并标注为我们的推断。

本篇没有我们的接入实测（CyberVerse 无对应模型目录），属**纯论文层笔记 + 机制对照**。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `causal-forcing.md` + sidecar，讲清一条理论主线：**architectural gap 只能由 ODE 初始化来补 → ODE 初始化要求 frame-level injectivity → 双向教师必然违反 → 必须换成 AR 教师**。
- 讲清三阶段方法（teacher forcing 训 AR 扩散 → causal ODE 蒸馏 → asymmetric DMD）与 causal CD 扩展，含关键公式与符号表。
- 如实登记评测口径陷阱：基线吞吐/延迟取自 Self Forcing 论文；Dynamic/IF 用自建 100-prompt 集而 VBench Total/Quality/Semantic 走官方 prompt。
- 第 8 节承担「与 `avatar-forcing` 的 diffusion forcing 张力」对照，并做「论文结论 vs 我们结论」的分层写法。
- 保留 6 张原图（论文 Fig 1–6），每图配图题与正文解读。

**Non-Goals：**

- 不复现、不做本地性能对比（我们没有该模型的接入与实测）。
- 不修改 `avatar-forcing.md`（其「后续工作」表已含本篇），不重写其 DF 结论。
- 不与 APT2 做数字对比（论文未比较，且 APT2 未开源）；只在第 7 节写算法/架构层面的三点区别。
- 不把 VisionReward 的负分当成"错误值"处理，也不按数值大小做跨指标直觉比较。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation |
| 作者 | Hongzhou Zhu\*、Min Zhao\*、Guande He、Hang Su、Chongxuan Li、Jun Zhu†（\* 同等贡献，† 通讯 Jun Zhu） |
| 单位 | 清华大学（计算机系 / BNRist / THU-Bosch ML Center）、ShengShu、UT Austin、中国人民大学高瓴人工智能学院、北京市重点实验室、教育部工程研究中心 |
| venue / 年份 | **ICML 2026**（`\usepackage[accepted]{icml2026}`） |
| arXiv | `2602.02214`（v1 2026-02-02；v5 2026-06-01 为最新版） |
| 项目页 | https://thu-ml.github.io/CausalForcing.github.io/ |
| 代码仓库 | **开源**：https://github.com/thu-ml/Causal-Forcing |
| papers 库 | **未入库**（131 条里无 `2602.02214`）⇒ frontmatter 只写 `arxiv_id` |
| 素材 | `.cache/article-note/causal-forcing/`（`example_paper.tex` 834 行、HTML 派生正文、17 张候选图 PDF、`synthesis.md`） |

## 2. 一句话价值主张（≤100 字）

指出把预训练**双向**视频扩散蒸成 **few-step 自回归**学生时，SOTA 的 ODE 初始化**在理论上就错**——双向教师只在 video level 单射，不满足 AR 学生所需的 **frame level** 单射，最优解塌成条件期望（模糊）；改用 **teacher forcing 训出的自回归教师**做 causal ODE 蒸馏再上 asymmetric DMD，在**同等训练预算**下把 Self Forcing 的 Dynamic Degree 提升 19.3%、VisionReward 8.7%、Instruction Following 16.7%。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/causal-forcing.md`，沿用 10 节骨架，`order: 80`（撰写期间 70 被同时段新增的 `omnimate` 占用，故顺延到下一空位）：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「papers 库未入库」说明 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（诊断 / 换教师 / 三阶段 / causal CD） | 列表 | 250 |
| 2 | 问题与动机 | 实时交互需要 few-step AR；除 sampling-step gap 还有 **architectural gap**；SOTA Self Forcing 仍显著弱于 standard DMD | 图 1 + 两层 gap 对照 | 600 |
| 3 | 方法精析 | 3.1 现有方法两阶段与其局限（DMD 补不上架构差，图 2）；3.2 理论分析：frame-level injectivity、条件期望塌陷、Lemma 与 Proposition；3.3 三阶段（TF 训 AR 扩散 → causal ODE 蒸馏 → asymmetric DMD，图 3–5）；3.4 causal CD 扩展 | 图 2–5 + Mermaid ×2 + 式 (1)–(5) | ≥1600 |
| 4 | 训练与实现细节 | 三阶段步数/数据/超参、DMD 教师配置、评测口径、未披露项 | 10 项配置披露表 | 700 |
| 5 | 推理与系统链路 | chunk-wise（3 latent frames）与 frame-wise 两种设定、4 步采样与时间步、temporal KV cache、17.0 FPS / 0.69 s 的口径来源 | Mermaid 时序 + 4 步时间步表 | 600 |
| 6 | 实验与结果 | 主表（三类基线）、消融表（TF vs DF / causal ODE vs SF ODE ×2 设定 / CD）、用户研究、定性图 | 图 6 + 两张表 | 1200 |
| 7 | 相关工作与定位 | 双向扩散基座 / AR 视频扩散 / 蒸馏（consistency、ODE、score distillation）；与 APT2 的三点区别；长视频适配是正交问题 | 谱系表 | 500 |
| 8 | 局限与启发 | 论文自述局限；**与 `avatar-forcing` 的 DF 张力**（分层写：论文结论 / 我们结论 / 推断）；可操作启发 | 「论文局限 vs 我们结论」表 | 900 |
| 9 | 术语与符号表 | 术语表 + 符号表 + 易错命名 | 两张表 | — |
| 10 | 相关文档 | 既有笔记 + 数字人概述 + knowledge | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 清单里 `causal-forcing.md` 状态改「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 两层 gap 的原文表述；Self Forcing 弱于 standard DMD 的对照组设计（同基座、同双向教师） | `tex` L219–250；图 1（`Figs/Fig2.pdf`） | 无缺口 |
| 3.1 | Self Forcing 两阶段回顾 + 式 (1) ODE 目标；用"标准 DMD 蒸出的 few-step 双向模型"做初始化以**隔离** architectural gap，仍显著更差（图 2） | `tex` L233–250；`Figs/Fig3.pdf` | 无缺口 |
| 3.2 | Def. frame-level injectivity（式 4）与 `φ^AR` 记号；违反即塌到 `E[x_0|x_t^i,x_t^{<i},t]`（式 5）；Lemma（非单射，非形式化 + 附录严格化）；Prop.（最优解 `≁ p_data`）；直觉句：双向模型去噪第 i 帧用了全部帧，AR 学生没有未来帧 ⇒ 信息丢失 | `tex` L251–345；图 3（`Figs/Fig4.pdf`，a/b/c 三面板）；附录 `sec:appendix_proof_asy_ode_is_wrong` | 证明细节只写结论，不复述附录推导 |
| 3.3 | Stage 1：TF vs DF 的取舍 + Prop.（DF 的 KL>0 训练-推理失配），图 4；**"反直觉"要如实写**：论文发现 TF 更好。Stage 2：从 AR 教师采 PF-ODE 轨迹（`D_Causal`），学生回归 clean target、条件在 GT clean 历史；因教师是 AR，单射天然成立。Stage 3：asymmetric DMD 沿用 Self Forcing 的 self-rollout；图 5 | `tex` §3.3 + 附录 §8.2；`Figs/Fig5.pdf`、`Figs/Fig6.pdf` | 无缺口 |
| 3.4 | causal CD：用原生 AR 教师 + teacher forcing；`x0`-预测形式 `G_θ=x^i−t·v_θ` 直接满足边界条件，省掉 `c_skip/c_out`；优于 asymmetric CD；论文自述这只是 vanilla LCM 初步实例 | `tex` §3.4 + 附录 §8.3.4；`Figs/appendix_CD/img.tex` | 附录图不发布，只在正文引用其结论 |
| 4 | `D_Bi`≈3K（Wan 双向 + VidProM prompt 合成）、`D_Causal`=3K、Stage1 2K 步、Stage2 1K 步、Stage3 DMD 750 步收敛于 VidProM；batch 64、Adam lr 2e-6（β1=0，β2=0.999）；DMD 的 `s_real`=Wan2.1-14B、`s_fake`=1.3B；chunk=3 latent frames；CD 用 LCM（48 离散步、UniPC、EMA 0.99、3K 步）；训练硬件与随机种子**未披露** | `tex` §4.1 + 附录 §8.4 | 硬件/种子写「未披露」 |
| 5 | 推理 4 步、时间步 `1 / 0.9375 / 0.8333 / 0.625`；chunk-wise 与 frame-wise 共用同一套公式；声称支持 temporal KV cache；17.0 FPS / 0.69 s（与 Self Forcing 相同，因为同协议同实现） | `tex` §4.1/§4.3 + 附录 §8.4；Tab. 1 | 基线的吞吐/延迟来自 Self Forcing 论文 ⇒ 单列一句警告 |
| 6 | 主表逐格数字 + 三类基线分组读法；自洽校验（57→68 = +19.3%、5.820→6.326 = +8.7%、48→56 = +16.7%）；消融四组；用户研究 10 人 × 10 prompt 只做排序、无置信区间；100-prompt 自建运动集 | `tex` Tab. 1/2 + §4.2 + 附录 §8.4「Evaluation details」 | 用户研究样本量小 ⇒ 记缺口 |
| 7 | 三条脉络；与 APT2 的三点区别（本文首次给出 forward-KL 蒸馏需 AR 教师的理论分析 / 本文沿用 asymmetric DMD + 双向 DMD 教师 + 支持 temporal KV cache，APT2 是 GAN 派且无 KV cache / 本文开源首个 causal-ODE 初始化的 few-step AR 模型）；长视频需 LongLive、Rolling Forcing、Infinity-RoPE、Deep Forcing 等正交方法 | `tex` §4.3 + §2 | 这些引用文献只点名，不给数字 |
| 8 | 论文自述：5s/5s attention 直接外推有训练-推理差；CD 初版弱于 score distillation；未与 APT2 比较。**我们的对照**：`avatar-forcing.md` 的「DF vs 普通自回归扩散」消融与本文 Prop. 3.1 方向相反；三处可能的设定差异（模态：512 维运动隐空间 vs 像素/latent 视频；判据：长时运动漂移 vs 像素质量与 VisionReward；前提：本文的失败路径叠加了"双向教师 + 因果学生"）；结论写"张力存在、原因未验证" | `tex` §4.3/§5 + `avatar-forcing.md` 的 `## 消融` 与 §3.3 | 不做本地实验 ⇒ 只作机制对照 |
| 9 | 术语/符号两表 + 易错点（ODE distillation vs consistency distillation vs score distillation；teacher forcing vs diffusion forcing；chunk-wise vs frame-wise；architectural gap vs sampling-step gap；Dynamic Degree 是 VBench 指标而非"动态能力"泛称） | `tex` §2/§3 + 附录 | 无缺口 |

## 4. 口径与取舍

- **D1 diffusion forcing 的张力必须分层写**：先写论文结论（DF 有 KL>0 的训练-推理失配、消融中 VisionReward 1.583 低于 TF 3.343，且 DF 更高的 Dynamic Degree 被论文判为"塌陷导致指标虚高"）；再写我们结论（Avatar Forcing 用 DF、消融里比普通自回归扩散稳定）；最后写我们的推断（模态与判据不同），并显式标注**未验证**。
- **D2 吞吐/延迟的口径**：Causal Forcing 与 Self Forcing 同为 17.0 FPS / 0.69 s；论文附录明确"基线的吞吐与延迟直接取自 Self Forcing 论文"，本笔记必须原样标注，不能写成"本文实测所有基线"。
- **D3 评测集合不可混读**：Dynamic Degree / VisionReward / Instruction Following 用自建 100-prompt 运动集；VBench 的 Total/Quality/Semantic 仍走官方 prompt（连其 Dynamic 项也来自官方 prompt）。两者不能拼成"全面领先"。
- **D4 VisionReward 的取值域**：子分与总分位于 `[−1,1]`，可负；负值不代表缺失数据。主表里 `--` 前缀是负号，不是"未测"。
- **D5 公平性口径要写出来**：两个 ODE 变体总步数都是 3K（2K + 1K），两个 CD 变体都是 3K，作者以此主张"同等训练预算"。
- **D6 用户研究不做显著性声称**：10 人 × 10 prompt、只做整体质量排序；只写"论文报告排名最优"，不写"显著优于"。
- **可选省略**：附录的 proof 细节与 appendix 图不发布，只在第 3、6 节引用其结论各一句。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/causal-forcing/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件（`raw/figures/`） | 用在哪 | 论文图 | 发布前处理 |
|---|---|---|---|---|
| 图 1 | `Fig2.pdf`（`bi_dmd_vs_sf`） | §2 问题与动机 | Fig 1 | `pdftoppm` 150 DPI → Pillow 转 WebP、最长边 ≤1600 |
| 图 2 | `Fig3.pdf`（`no_init_and_bi_dmd_init`） | §3.1 DMD 补不上架构差 | Fig 2 | 同上 |
| 图 3 | `Fig4.pdf`（`injectivity_of_ode_distill`） | §3.2 理论核心（a/b/c 三面板） | Fig 3 | 同上；三面板小字最多，需目视确认 |
| 图 4 | `Fig5.pdf`（`tf_vs_df`） | §3.3 Stage 1 | Fig 4 | 同上 |
| 图 5 | `Fig6.pdf`（`asymmetric_ode_vs_casual_ode`） | §3.3 Stage 3 | Fig 5 | 同上 |
| 图 6 | `qualitive.pdf`（`performance_comparison`） | §6 定性对比 | Fig 6 | 同上；多面板，需目视确认 |

> 论文源码里主图文件名是 `Fig2.pdf`–`Fig6.pdf` + `qualitive.pdf`，对应论文 Fig 1–6；不要按文件名误判图号。附录图（`appendix_*`、`cd_*`、`causODEbiInit`）不发布。

**公式**（KaTeX `$$...$$` + 符号表）

1. Self Forcing 的 ODE 蒸馏目标 `θ* = min_θ E[‖G_θ(x_t^i, x_t^{<i}, t) − x_0^i‖²]`（式 3）
2. frame-level injectivity 定义 `∀i, x_t^i = y_t^i ⇒ φ^AR(x_t^i,t) = φ^AR(y_t^i,t)`（式 4）
3. 违反后的条件期望塌陷 `G_θ*(x_t^i, x_t^{<i}, t) = E[x_0 | x_t^i, x_t^{<i}, t]`（式 5）
4. causal ODE 蒸馏目标 `θ* = min_θ E[‖G_θ(x_t^i, x_gt^{<i}, t) − x_0^i‖²]`（条件在 GT clean 历史）
5. DMD 梯度 `∇_θ E_t[KL(p_{θ,t}‖p_data,t)] = −E[(s_real − s_fake)·∂x̃/∂θ]`（式 1，含 `s_fake` 在线可训）
6. causal CD 目标 `θ* = min_θ E[w(t)·d(G_θ(x_t^i, x_gt^{<i}, t), G_{θ⁻}(x̂^i_{t−Δt}, x_gt^{<i}, t−Δt))]` 与 `x0`-预测形式 `G_θ = x^i − t·v_θ`

**Mermaid**：两张——① 三阶段数据/教师流（TF 训 AR 扩散 → 从 AR 教师采 `D_Causal` → causal ODE 蒸馏 → asymmetric DMD），节点上标出"教师是双向还是 AR"；② 两条路径对照（双向教师 → 非单射 → 条件期望 → 模糊 ↔ AR 教师 → 单射成立 → 学回 flow map）。

**表格**：三阶段配置披露表（10 项）、与 Self Forcing 的机制差异表、主结果表、消融表、用户研究与评测口径表、术语表、符号表。

## 6. 引用关系

- `[[论文笔记/avatar-forcing|Avatar Forcing 模型笔记]]`（引用来源；第 8 节的 DF 张力对照）
- `[[论文笔记/vorch-streamer|Vorch-Streamer 模型笔记]]`（同为目的后训练因果流式，对象是 T2AV 长时自强制）
- `[[论文笔记/liveact|SoulX-LiveAct 模型笔记]]`、`[[论文笔记/ditto|Ditto 模型笔记]]`
- `[[数字人概述/数字人加速|数字人加速]]`、`[[数字人概述/数字人领域问题|数字人领域问题]]`
- `[[knowledge/视频生成训练与推理加速专题|视频生成训练与推理加速专题]]`
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

- [把 DF 张力写成我们的结论] → D1 强制三段式（论文结论 / 我们结论 / 推断+未验证）。
- [把基线吞吐写成本文实测] → D2；只在表脚注与正文各标一次。
- [评测集混读导致"全面领先"] → D3；主表下方固定一句口径说明。
- [把 VisionReward 的负值当缺失] → D4；表头保留 `--` 原样并解释。
- [图 3 三面板小字不可读] → 发布后需你目视；本机模型不支持读图，我无法自检。
- [过度展开证明细节] → Non-Goal；附录推导只在第 3.2 节引用结论，不复制。
- [order 选择] → 实施时 `order: 70` 与并行会话新增的 `omnimate` 碰撞，已顺延为 **`order: 80`**（`docs_order.py list` 已确认无重复）；若你希望与 `avatar-forcing` 相邻，改到 15 需要重排既有顺序，会触及 7 篇。
- [papers 库未入库] → frontmatter 只写 `arxiv_id`；如需入库，另开一个小改动用 `scripts/import_papers.py`。

## Migration Plan

1. 用户审核本 design（尤其第 3.2 节理论主线、第 4 节 D1–D5 口径、第 5 节 6 张图与 6 条公式、第 7 节 order 选择）。
2. apply 阶段：`pdftoppm` 转 PNG → `figures.py convert/publish` 或 Pillow 转 WebP 发布 6 张图 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`check-delivery.py`、浏览器实测（6 图解码 / 公式 / 2 张 Mermaid）、`docs_order.py list management/docs/论文笔记`、FastAPI 详情接口、`openspec validate docs-note-causal-forcing --strict`；任一不过则回退本次改动。
