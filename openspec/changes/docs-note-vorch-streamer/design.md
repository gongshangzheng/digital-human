## Context

`论文笔记/` 已有三篇流式/实时路线笔记（`avatar-forcing` 块因果 + 历史 offset、`ditto` 参考锚定、`liveact` ARPP/ConvKV），三篇都在「潜空间 + 流式」这一族里。`vorch-streamer` 是**第四条路线**，且设定不同：原生 **T2AV**（文本直接生成语音 + 视频），不是音驱动头像；它的核心贡献是**后训练**把预训练双向基座转成因果长时流式，并把「暴露偏差导致漂移累积」写成首要困境——正是我们 `avatar-forcing` 漂移实验处理过的同一问题，只是解法与判据不同。

本篇没有我们的接入实测（知识库里没有任何 Vorch 素材，CyberVerse 也没有对应模型目录），因此属于**纯论文层笔记 + 与既有路线的对照**，工程层不写「接入状态」。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `vorch-streamer.md` + sidecar，讲清两个困境、三阶段后训练（合成数据 / 因果流式 / 长时自强制 + DMD）与 LLM 语音规划。
- 让第 8 节承担「与我们三篇笔记的对照」：同一漂移问题在 T2AV/全双工设定下的第四种解法与判据（Drift / Identity / ArcFace / CLIP 时序指标）。
- 如实登记三处口径问题：合成数据理由单一、Table 1 跨组比较、打断能力无量化。

**Non-Goals：**

- 不写接入与部署（无本地实测、无对应代码仓库）。
- 不把 TIA2V 基线的数字当成与本文同任务的比较结果。
- 不补跑实验；不把「支持打断」写成已验证的交互能力。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Vorch-Streamer: Extending Human Audio-Visual Generation to Real-Time Long-Form Streaming |
| 作者 | Menglin Han\*、Yang Ding\*、Yulei Lu、Haoran Yu、Xin Ma、Junyi Chen、Zhangkai Ni†、Lin Ma†、Yaohui Wang†（\* 同等贡献，† 通讯） |
| 单位 | Vorch Team、Tongji University、Harbin Institute of Technology (Shenzhen)、Shanghai Jiao Tong University |
| venue / 年份 | arXiv `v2`（2026-08-07）；该版本未声明 venue |
| arXiv | `2608.05663v2` |
| 项目页 | https://vorch-project.github.io/Vorch-Streamer-project/ |
| 代码仓库 | 论文未给出代码仓库（项目页存在，代码未声明开源） |
| papers 库 | **未入库**（frontmatter 只写 `arxiv_id`，不写 `papers_id`） |
| 素材 | `.cache/article-note/vorch-streamer/`（paper.txt 派生自 HTML v2、PDF、4 张原图含 1 张 SVG、5 lane 分析） |

## 2. 一句话价值主张（≤100 字）

在预训练**双向**音视频基座（LTX2.3，22B）上做**三阶段后训练**——合成语料、TF/DF 混合的因果流式、再到**长时自强制 + DMD 蒸馏**——把「用自己生成的块当上下文」的暴露偏差压住，同时用 **LLM 语音规划**解决「因果生成器该说哪一段」；单张 H200 上 **27.12 FPS**，是唯一超过 24 FPS 播放速率的原生 T2AV 方法。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/vorch-streamer.md`，沿用 10 节骨架：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「papers 库未入库」说明 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（合成语料 / 因果流式 / 长时自强制 / LLM 语音规划） | 列表 | 250 |
| 2 | 问题与动机 | 论文自述的两个困境：**暴露偏差导致的漂移累积**、**全局语音条件 vs 因果局部窗口的错配** | 图 1（teaser）+ 困境对照 | 700 |
| 3 | 方法精析 | 3.1 合成阿凡达语料（80K / 12–21s / model-consistent）；3.2 因果音视频流式（同步块≈1s、窗口 $P{+}R$、TF 10% / DF 90%，式 1–4）；3.3 长时自强制与 DMD（式 5–10）；3.4 LLM 语音规划（式 11–13） | 图 2（框架，SVG 栅格化）+ Mermaid + 式 1–4 | 1500 |
| 4 | 训练与实现细节 | 三阶段训练量（Stage 2 = 6,000 steps / 64×H200；Stage 3 = 1,000 iters / 32×H200 / 6:1）、基座与初始化、22B vs 22.8B 两个口径、未披露项 | 配置披露表 | 700 |
| 5 | 推理与系统链路 | 每块 4 步去噪、约 1 秒块、推理默认窗口 3+1、windowed KV cache + cache eviction、单张 H200 27.12 FPS 的口径 | 式 5–10 摘要 + Mermaid 时序 | 700 |
| 6 | 实验与结果 | Table 1（FPS/Sync/WER，含 T2AV 与 TIA2V 两组）、Table 2（FID/FVD/Dynamic/Drift/Anatomy/Identity/ArcFace/CLIP）、Table 3（最后 10 秒窗口）、Table 4（speech condition 消融）、Table 6（$P{+}R$） | 图 3、图 4 + 四张表 | 1200 |
| 7 | 相关工作与定位 | 三条脉络（联合音视频生成 / 实时长时视频 / 以人为中心）＋ OmniForcing 最近前作 ＋ Wan-Streamer 互补 | 谱系表 | 600 |
| 8 | 局限与启发 | 三处口径问题；与我们三篇笔记的漂移问题对照；可操作启发 | 「论文缺口 vs 我们结论」表 | 900 |
| 9 | 术语与符号表 | 术语表 + 符号表 + 六条命名易错 | 两张表 | — |
| 10 | 相关文档 | 三篇对照笔记 + knowledge 中相关专题 | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 清单里 `vorch-streamer.md` 状态改「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 两个困境的原文表述（exposure bias 与因果注意力下的 compounding artifacts / temporal drift；全局转写 vs 每块只有有限已生成窗口）；LTX-2 自述「超出支持时长后出现 temporal drift」 | `methodology.md` §3.3/§3.4 引文；图 `teaser` | 无缺口 |
| 3 | 式(1) 同步块切分与 ≈1s 口径（3 视频 latent frame + 25 音频 token）、首块 +1 帧 +1 token；式(2) 窗口；式(3)(4) TF 10%/DF 90% 双序列与掩码禁止读当前块；式(5)–(10) DMD 三网络；式(11)–(13) planning token（25 Hz / 40 ms）、Fun-CosyVoice LUT + silence token、speech cross-attn + gate | `methodology.md` §3.1–§3.4 | 合成数据的「为什么」只有一句 ⇒ 明写论文未给其他理由 |
| 4 | Stage 2：10% TF + 90% DF、6,000 steps、64×H200、batch 64、lr 1e-4；Stage 3：1,000 iters、32×H200、batch 32、critic:generator 6:1、lr 1e-5；基座 LTX2.3 = 22B，管线 22.8B | `experiment.md` §4.1；`methodology.md` §1 | 训练总机时/种子/数据清洗未披露 ⇒ 写「未披露」 |
| 5 | 每块 4 步去噪；推理默认 $3{+}1$；训练默认 $3{+}3$；windowed KV cache + eviction 使内存与长度无关；FPS = 生成帧数 ÷ 端到端 wall-clock（单张 H200） | `experiment.md` §4.1/§4.5.4；`methodology.md` §2 | 无缺口 |
| 6 | Table 1/2/3/4/6 逐格数字与加粗/下划线读法；Table 1 的 T2AV/TIA2V 口径警告；Table 3 的「最后 10 秒 vs 最初 10 秒」；Table 4 的 WER 184% / 62.77%；§4.3 名义两分钟与 OOM 30 秒 | `experiment.md` 全文 | Table 2 粗体约定未声明 ⇒ 标注为推断 |
| 7 | 三条脉络与差异（「双向改因果不是减步数就能做到」）；OmniForcing 是最近前作且本文沿用了它的首块做法；Wan-Streamer 互补（一个训新基座、一个后训练现成基座） | `citation.md` 全文 | 部分文献条目未核实 ⇒ 只点名不给数字 |
| 8 | 三处口径问题；与我们四篇的对照：`avatar-forcing`（方向游走 + 静音放大，判据是 latent 夹角）、`liveact`（ARPP/ConvKV，用机制而非指标处理长时）、`ditto`（参考锚定；其长时稳定靠逐帧参考注册而非自强制）、本篇（用 DMD + 自 rollout 缩小 exposure gap，并用 Drift/Identity/ArcFace/CLIP 时序指标判据）；可操作启发 | `methodology.md` §3.3；三篇既有笔记的结论 | 无本地实测 ⇒ 不做性能对比，只做机制对照 |
| 9 | 术语/符号两表 + 六条命名易错（T2AV vs TIA2V、LTX-2 vs LTX2.3、22B vs 22.8B、3+3 vs 3+1、Table 1/2 加粗约定、hour-scale 类说法） | `terminology.md` | 无缺口 |

## 4. 口径与取舍

- **D1 T2AV 与 TIA2V 必须分开**：带 `†` 的两条基线拿到 Qwen3-TTS 音频与生成首帧，WER 由共享 TTS 决定、不衡量 avatar 生成器；引用其 Sync/ArcFace/CLIP 数字时必须带图注的「不可直接比较」警告。
- **D2 Table 1 的跨组加粗如实写出**：粗体/下划线是跨 T2AV 与 TIA2V 统一比较的结果，与图注警告并存；不把它简化成「本文全面最优」。
- **D3 合成数据只写论文给的理由**：80K 语料唯一的动机句是 `model-consistent`；不做「数据规模/多样性」方面的补写，改为在第 8 节记为缺口。
- **D4 打断能力按论文口径**：写「论文称支持打断或切换语音」，并注明**没有量化协议**。
- **D5 不做与本地性能的横比**：本篇无我们的实测；第 8 节只做机制层面的对照（同一漂移问题、不同解法与判据），不并列 FPS。
- **D6 参数口径分开写**：基座 22B、本文管线 22.8B。
- **可选省略**：§3.1 合成数据管线的实现细节压成一段；Appendix/补充材料若有更细的消融，只在对应小节一句带过。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/vorch-streamer/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件 | 用在哪 | 论文图 | 发布前处理 |
|---|---|---|---|---|
| 图 1 | `teaser.png` | §2 问题与动机（27 FPS 全程展示） | Fig 1 | 转 WebP 压到 ≤500KB |
| 图 2 | `VorchStreamer_framework.svg` | §3 方法精析 · 总览 | Fig 2 | **先栅格化**（`rsvg-convert`，已确认可用）再转 WebP，最长边 ≤1600px |
| 图 3 | `temporal_consistency.png` | §6 长时一致性 | Fig 3 | 仅转 WebP（已合规） |
| 图 4 | `qualitative.png` | §6 定性对比 | Fig 4 | 转 WebP 压到 ≤500KB |

注意：Figure 2 在 HTML 里用 `<object data=...>` 引用，按 `<img src>` 扫描会漏抓——本 change 已在素材阶段补抓并登记，实施时不要退回「只有 3 张图」的状态。

**公式**（KaTeX `$$...$$` + 符号表）

1. 同步块切分 $\mathcal{B}_b=(\mathbf{x}^v_0[s^v_b:e^v_b],\ \mathbf{x}^a_0[s^a_b:e^a_b])$（式 1）
2. 因果窗口 $\mathcal{H}_b=\{0,1,2\}\cup\{\max(0,b-3),\dots,b-1\}$（式 2；说明训练 3+3 与推理 3+1 的区别）
3. flow-matching 加噪 $\mathbf{x}^m_\sigma=(1-\sigma)\mathbf{x}^m_0+\sigma\bm{\epsilon}^m$（式 3，TF/DF 混合的实现基础）
4. DMD 引导方向 $\overline{\mathbf{g}}^m\propto\mathbf{p}^m_{\mathrm{fake}}-\mathbf{p}^m_{\mathrm{real}}$ 与损失（式 8–9，含 stop-gradient）
5. speech planning 注入 $\mathbf{h}^a_\ell\leftarrow\mathbf{h}^a_\ell+\operatorname{sigmoid}(g_\ell)\operatorname{Attn}^\ell_{\mathrm{speech}}(\mathbf{h}^a_\ell,\mathbf{e}^s)$（式 13）

**Mermaid**：两张——① 三阶段后训练数据流（合成语料 → 因果流式 → 长时自强制 + DMD）；② 流式推理时序（块切分、窗口 KV cache、每块 4 步去噪、speech planning 与音频分支的融合）。

**表格**：三阶段训练配置表、同步块与窗口口径表、Table 1（FPS/Sync/WER）、Table 2（视觉与人类保真）、Table 3（长时窗口）、Table 4（speech condition）、Table 6（$P{+}R$）、四篇笔记的漂移路线对照表、术语表、符号表。

## 6. 引用关系

- `[[论文笔记/avatar-forcing|Avatar Forcing 模型笔记]]`（漂移诊断：方向游走 + 静音放大）
- `[[论文笔记/liveact|SoulX-LiveAct 模型笔记]]`（ARPP / ConvKV：用机制处理长时）
- `[[论文笔记/ditto|Ditto 模型笔记]]`（参考锚定）
- `[[knowledge/digital-human-realtime-gpu-comparison|实时数字人 GPU 横评]]`、`[[knowledge/视频生成训练与推理加速专题|视频生成训练与推理加速专题]]`
- `[[数字人概述/数字人领域问题|数字人领域问题]]`（长时漂移与分段边界的既有讨论）
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

**现状风险与处理**

- [把 TIA2V 基线当成同任务比较] → D1，两条 `†` 基线的每处数字都带口径警告。
- [写成「本文全面最优」] → D2；Table 2 里 SoulX-FlashTalk 的 ArcFace/CLIP 更高、解剖合理性持平，都要写出来。
- [为合成数据补写动机] → D3，只写 `model-consistent` 一条，并把缺失记进第 8 节。
- [打断能力被写成语义已验证] → D4。
- [Figure 2 漏抓导致方法节无框架图] → 图表清单已写明 SVG 来源与栅格化步骤；实施时核对 `_assets` 里确实有 4 张。
- [图内小字可读性未验证] → 本机模型不支持读图；`qualitative.png`（1467×1037 多面板）与栅格化后的框架图需你在发布前目视确认。
- [无 papers 库条目] → frontmatter 只写 `arxiv_id`；若你希望入库，我另开一个小改动。

## Migration Plan

1. 用户审核本 design（尤其第 3 节架构、第 5 节配图与公式、第 7 节风险项）。
2. apply 阶段：`rsvg-convert` 栅格化 SVG → `figures.py convert/publish` 发布 4 张图 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`check-delivery.py`、浏览器实测（4 图解码 / 公式 / Mermaid）、`docs_order.py list management/docs/论文笔记`、`openspec validate docs-note-vorch-streamer --strict`；任一不过则回退本次改动。
