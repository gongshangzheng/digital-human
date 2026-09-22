# Design: docs-note-avatar-forcing-rewrite

> 按 `article-note` Phase 4 要求的七个字段组织；本文件即结构审批对象。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Avatar Forcing: Real-Time Interactive Head Avatar Generation for Natural Conversation |
| 作者 | Taekyung Ki\*、Sangwon Jang\*、Jaehyeong Jo、Jaehong Yoon、Sung Ju Hwang |
| 单位 | KAIST、NTU Singapore、DeepAuto.ai |
| venue / 年份 | CVPR 2026（论文 TeX 头部为 `cvpr`） |
| arXiv | `2601.00664v2`（2026-01-02） |
| 项目页 | https://taekyungki.github.io/AvatarForcing |
| 代码仓库 | 未公开；我们接入的是 CyberVerse `models/avatarforcing/` @`4968280` |
| 素材 | `.cache/article-note/avatar-forcing/`（source tarball + HTML + PDF，16 张候选图） |

**易混提示（写入正文论文信息表）**：另有 `arXiv:2603.14331`「AvatarForcing: One-Step Streaming Talking Avatars via Local-Future Sliding-Window Denoising」（浙大 + 快手 Kling，DiT + 双锚 KV cache）与本篇同名易混，**不是**本篇；旧笔记误引的是它。

## 2. 一句话价值主张（≤100 字）

在 FLOAT motion latent 空间用块因果 Diffusion Forcing 逐块滚动生成头像运动，配合双路条件编码与「丢掉用户条件」构造的 DPO，把双向对话头像做到约 500ms 延迟且反应更生动。

## 3. 笔记结构大纲（10 节）

| 节 | 标题 | 要点 | 素材来源 | 必备元素 | 字数 |
|---|---|---|---|---|---|
| 0 | 论文信息 | 标题/作者/单位/venue/arXiv/项目页/代码仓库；与 2603.14331 的区分说明 | 1. 论文速览 | Markdown 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 3–5 条贡献（因果实时、双路条件、DPO 免标注、听态覆盖） | tex L102–L117 | 列表 | 200 |
| 2 | 问题与动机 | 两个挑战：① 因果约束下实时（INFP 需 >3s 未来上下文）② 表达力标注缺失（倾听数据偏单调） | tex L102–L117、L238–L250；`exp_l2_var_exp-pasted` | 数据点 + 图 3 | 500 |
| 3 | 方法精析 | `z=z_S+m_S` 显式分解；条件三元组 `c=(a_u,m_u,a)`；Dual Motion Encoder 两级 cross-attn；Causal DFoT（块内共享噪声步、块间因果）；look-ahead mask | tex L151–L237；`analysis/methodology.md` | Mermaid 主链路 + 图 1 总架构 + 图 2 `v_θ` 结构 + ≥2 公式 | 1300 |
| 4 | 训练与实现细节 | 数据（RealTalk+ViCo、切场景/裁脸/IIANet 语音分离、25fps/16kHz）；实现（Adam 1e-4、batch 8、d=512、8 heads/h=1024、N=50/B=5/l=2、Wav2Vec2 12 特征、10 NFE、H100）；两阶段（DF 2000k → DPO 5k，λ=0.1/β=1000） | tex L274–L295、L491–L514；`analysis/experiment.md` | 10 项配置披露表 | 600 |
| 5 | 推理与系统链路 | 块滚动 + rolling KV cache；offset `O^{i+1}`（上一块末 l 帧+条件）；独立 CFG 三路 KV 缓存；缓存上限 `M=38`；与双向 DiT 的结构对比 | tex L183–L237、L455–L490；`analysis/methodology.md` | 图 4 `cache4` + 图 5 `mask_compare` + Mermaid 时序 | 500 |
| 6 | 实验与结果 | 交互头像（延迟 0.5s vs INFP\* 3.4s、Reactiveness/Richness 指标、人类偏好 >80%）；talking head（HDTF，FID 20.332/FVD 149.798 最好）；listening（ViCo，rPCC 最好，基线取自 DIM）；消融（去 `m_u` → 静态；去 DPO → 多样性下降；DF vs 自回归扩散 → 后者漂移；block size 权衡） | tex L296–L366、L497–L556；`analysis/experiment.md` | 配置表 + 主结果表 + 消融表 + 图 6 `human_eval_3col_final` | 900 |
| 7 | 相关工作与定位 | 三线：talking / listening / dyadic；DIM（需人工角色切换）、INFP（双向 DiT 需全上下文）、ARIG（仅表情、时序差）；本文位置 | tex L118–L134；`analysis/citation.md` | 对比表 | 400 |
| 8 | 局限与启发 | 论文局限（仅头动、显式可控性不足、exposure bias 未完全解决）+ **我们的实测**（模长否证/方向游走、锚点引导有效、训练期条件化失败、学习式锚力终止、CSIM-as-loss 放弃）+ 可操作启发 | tex L567+；`analysis/code-analysis.md`；`实习复盘/数字人身份`、`数字人动作` | 分层列表 + 「论文局限 vs 我们结论」对照表 | 600 |
| 9 | 术语与符号表 | 中英术语表 + 变量表 | `analysis/terminology.md` | 两张表 | — |
| 10 | 相关文档 | knowledge 三篇 + 微调策略专题；实习复盘 三篇；papers 库条目；2603.14331 的博客精读（作为对照） | `synthesis.md` | 链接列表 | — |

补充：工程层不单列大节，只占第 8 节的一半与第 5 节的落点说明，细节全部外链到 `实习复盘/`（与旧笔记的「在我们体系中的角色」对应）。

## 4. 口径与取舍

- **不写 2603.14331 的技术内容**：只作为「易混提示」出现在第 0 节与第 10 节的对照链接里。
- **不复制 `实习复盘/数字人身份` 的实验矩阵**：本篇只保留结论，数字与表格留在原篇（旧笔记已确立此分工）。
- **不展开流式改造的工程细节**（生产者/消费者、上游超时坑）到正文，压成第 8 节一行并链 `实习复盘/工程设计`。
- **依赖历史素材**：`knowledge/` 与 `实习复盘/` 是从博客/InternWiki 复制的整理稿，正文引用时以论文原文为准，工程结论标注为「我们的实测」。

## 5. 图表公式清单

**图（计划发布到 `management/docs/_assets/avatar-forcing/`，WebP）**

| 编号 | 源文件 | 用途 | 放置 |
|---|---|---|---|
| 图 1 | `architecture1-4.pdf` | 总架构（Dual Motion Encoder → Causal DFoT → decoder） | 第 3 节 |
| 图 2 | `architecture2-2.pdf` | `v_θ` 结构 + look-ahead mask | 第 3 节 |
| 图 3 | `exp_l2_var_exp-pasted.pdf` | 说话/倾听表达力方差 | 第 2 节 |
| 图 4 | `cache4.pdf` | 双向 DiT vs 块因果 DFoT | 第 5 节 |
| 图 5 | `mask_compare.pdf` | 三种 attention mask | 第 5 节 |
| 图 6 | `human_eval_3col_final.pdf` | 人类偏好五项指标 | 第 6 节 |

（备选：`ablation-dpo-3.pdf` 若第 6 节消融需要配图）

**公式（fenced code block + 符号表）**

1. 自回归分解 `p_θ(m^{1:N}) = Π_i p_θ(m^i | m^{<i}, c^i)`
2. blockwise look-ahead mask `M_{i,j} = 1 if ⌊j/B⌋ ≤ ⌊i/B⌋ + l else 0`
3. DF 训练目标 `L_DF(θ) = E‖v_θ(m^n_{t_n}, t_n, c^n) − (m^n_1 − m^n_0)‖`
4. 总目标 `L_ft(θ) = L_DF(θ) + λ·L_DPO(θ)`

**表格**：10 项训练配置披露表、交互头像主结果表、talking head 对比表、listening 对比表、消融表、相关工作定位表、「论文局限 vs 我们结论」表。

**Mermaid**：方法主链路 1 张 + 块滚动推理时序 1 张。

## 6. 引用关系

- `[[knowledge/Avatar Forcing 模型精读|Avatar Forcing 模型精读]]`
- `[[knowledge/Avatar Forcing Motion Latent AutoEncoder|Avatar Forcing Motion Latent AutoEncoder]]`
- `[[knowledge/Avatar Forcing 微调实践|Avatar Forcing 微调实践]]`、`[[knowledge/微调策略专题|微调策略专题]]`、`[[knowledge/数字人基础|数字人基础]]`
- `[[实习复盘/数字人身份|数字人身份]]`、`[[实习复盘/数字人动作|数字人动作]]`、`[[实习复盘/工程设计|工程设计]]`
- `[[实习复盘/数字人介绍与技术路线|数字人介绍与技术路线]]`
- sidecar `related` 计划：`papers/arxiv-2601.00664`（若补录）、`论文笔记/ditto`（未写则留空）

## 7. 风险与待确认项

**需用户裁决**

1. **模板冲突**：`论文笔记/README.md` 定义的是 4 节模板（`## 是什么` / `## 架构核心` / `## 在我们体系中的角色` / `## 与复盘各线的关联`），`article-note` 用的是 10 节骨架。本设计采用 **10 节骨架**（按你的要求走 article-note），并**同步更新 README 的统一模板**。若你希望保留仓库原 4 节模板，请说。
2. **`papers_id` 怎么办**：papers 库只有 `arxiv-2603.14331`，**没有** 2601.00664 条目。三选一：(a) 补录 2601.00664 到 `data/papers.db` 后 `papers_id: arxiv-2601.00664`（推荐，papers.db 是 gitignored 本地数据）；(b) 只写 `arxiv_id: 2601.00664`、省略 `papers_id`；(c) 保留指向 2603.14331（不推荐，会继续错）。

**风险**

- [主结果表数值需从 PDF 抄] → 用 `pdftotext`/人工核对 PDF 表格，不用摘要数字；6.8× 若找不到口径就只写「论文称 6.8×，未给细口径」。
- [图是矢量 PDF] → 用 `pdftoppm` 转 PNG 再转 WebP（Pillow 12 已就位），控制在 1600px / ≤500KB。
- [工程结论取自整理稿] → 标注来源为 `knowledge/` 与 change 记录；不在本篇写具体代码行号。
- [旧笔记被覆盖不可回滚] → Git 保留历史；sidecar `changelog` 记录旧版错引，便于回溯。
