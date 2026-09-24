## Context

- **素材**（`.cache/article-note/talker-t2av/`，已通过 `validate-analysis.py`）：`raw/sources/talker-t2av.html`（LaTeXML 全文，主源）+ `talker-t2av.pdf`（15 页）；source tarball 406 失败。我方材料（仅用于接入/工程事实，须标注「我方材料」）：`management/docs/knowledge/Talker-T2AV 模型精读.md`、`Talker-T2AV 接入与验证.md`（固定上游版本 `6712f62`）。
- **元信息**：arXiv `2604.23586v2`（v1 2026-04-26，v2 2026-08-04）；标题 *Talker-T2AV: Joint Talking Audio-Video Generation with Autoregressive Diffusion Modeling*；作者 Zhen Ye、Xu Tan、Aoxiong Yin、Hongzhan Lin、Guangyan Zhang、Peiwen Sun、Yiming Li、Chi-Min Chan、Wei Ye、Shikun Zhang、Wei Xue；单位含 HKUST、Zhejiang University、National University of Singapore、Independent Researcher 等（写作时按 HTML 首页逐项核对，不臆测）；**arXiv 无 venue comment → 不声明会议**。
- **图源限制（重要）**：论文**只有 1 张正文图**（Figure 1 Overview），另有 6 张表。HTML 仅含 `fig1.png`；PDF p4 的缩略图仅 242px，不适合发布。因此本篇**无法满足「≥3 张原图」的常规要求**，改用「1 张原图 + 2 张 Mermaid + 表格承载证据」，并在正文/design 中说明原因。

## Goals / Non-Goals

**Goals:**
- 按 10 节骨架成文；讲清「两级解耦 + 自回归」的机制链：共享因果 LM 做高层规划 → 两个模态专属轻量 DiT 头做低层渲染
- 讲清「对齐免费」的来源：冻结、同帧率（25Hz）的 1-D 编码器（视频 LIA-X 40 维 motion code、音频 WhisperX-VAE 32 维），逐位置相加融合（Eq. 2）→ 同一模型零改动支持 A2V 与配音
- 用 2 张 Mermaid 补结构表达；证据以论文表格为主（Table 1–6）

**Non-Goals:**
- 不用低分辨率缩略图凑图
- 不把跨来源的 SyncNet C/D 数字与外部论文横比（论文未说明变体/后处理）
- 不改其它笔记与概述正文（仅 2 处 knowledge 前向链接）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位 / venue（不声明会议）/ arXiv（`2604.23586v2`）/ papers 库条目（`arxiv-2604.23586`，**本地库未入库**）/ 上游固定版本（知识库 `6712f62`） |
| 1 | 一句话总结 | 两级解耦 + 自回归：共享因果 LM 在短 1-D patch 序列上做跨模态规划，两个模态专属 DiT 头解码同一 hidden state；冻结同帧率编码器让对齐免费；单卡 H20 上 24 FPS（T2AV）/30 FPS（A2V），参数量 1B/0.8B（§3.1–3.3；Table 2） |
| 2 | 问题与动机 | dual-DiT 联合模型的三点结构性局限：语义规划与信号渲染在整条去噪轨迹上纠缠、天生非因果/固定长度、推理极慢（§1 p1；§2.1 p2–3） |
| 3 | 方法精析 | Stage 1 共享因果 LM（1-D patch token，$P{=}4$）；Stage 2 两个模态专属轻量 DiT 头；**冻结同帧率编码器**（LIA-X 40D motion @25Hz / WhisperX-VAE 32D @25Hz）与逐位置相加融合（Eq. 2）；stop predictor（$p_{stop}(i)=\mathrm{sigmoid}(\mathrm{MLP}(h_i))$，BCE，正类权重 = continue:stop）；**图 1（论文 Figure 1）+ Mermaid（统一因果序列排布）** |
| 4 | 训练与实现细节 | 多任务单阶段：音频 CFM + 视频 CFM + stop 损失（Eq. 4）；T2AV 与 TTS 样本 1:1 混批 + task tag embedding；TTS-only 时运动分支换 learnable padding 且置零运动损失；关键配置表（未披露项照写） |
| 5 | 推理与系统链路 | 自回归步进 → 双头解码 → 输出；视频侧依赖外部 LIA-X 解码器与源身份图（模型只生成 40 维 motion，不生成像素）；音频头 global condition = speaker embedding，视频头 = 首帧 motion vector；**Mermaid（流式推理管线）**；与我方接入的关系（knowledge 两篇，标注「我方材料」） |
| 6 | 实验与结果 | Table 1（T2AV 主结果：CER/WER、FVD、SyncNet C/D 全面优于 5 个 dual-DiT 基线；**英文 UTMOS 3.458 略低于 UniAVGen 3.459，正文把音频优势写成 naturalness 提升与数字存在张力 → 照录 + 事实核对注**）；Table 2 效率（H20、5s 片段、24/30 FPS，比 UniVerse-1 快约 59×、UniAVGen 约 75×、MoVA 三个数量级）；Table 3 音频驱动说话头（中/英）；Table 4 Chem 配音基准；Table 5 token 排布消融（T2AV→Add 最优、Delay 掉点；A2V→Delay-3 最好）；Table 6 音频 codec 重建 |
| 7 | 相关工作与定位 | dual-DiT 联合生成、级联式 TTS→动画、以及「用冻结 1-D 编码器把对齐问题消掉」这一路线选择；与本仓库谱系：视频侧表示正是 **LIA-X**（链 `[[论文笔记/lia-x]]`） |
| 8 | 局限与启发 | 论文自陈（不声称可迁移到通用场景级音视频生成；长序列误差累积；LIA-X 视频保真上界）；SyncNet C/D 量纲可疑（未说明变体/后处理）；「论文局限 vs 我们结论」对照表（我方未接入；已用知识库固定上游版本做接入验证 → 标注「我方材料」）；可操作启发（同帧率 1-D token + 逐位置相加是「免对齐」的工程杠杆） |
| 9 | 术语与符号表 | Stage-1/Stage-2、1-D patch token、$P$、stop predictor、CFM、task tag、speaker embedding、negative… |
| 10 | 相关文档 | `[[论文笔记/lia-x]]`（视频侧 tokenizer）、`[[论文笔记/avatar-forcing]]`、`[[论文笔记/ditto]]`、`[[数字人概述/数字人领域问题]]`、`[[数字人概述/数字人加速]]`、`[[knowledge/Talker-T2AV 模型精读]]`、`[[knowledge/Talker-T2AV 接入与验证]]` |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | Figure 1（HTML `2604.23586v2/fig1.png`，939×720） | 3 方法精析 | 统一因果序列（完整文本 token + 交织音视频 token）与生成/解码管线 |
| Mermaid 1 | 自绘（据 §3.2 描述） | 3 方法精析 | token 排布：文本 / 音频 / 视频 patch 的交织与 AR 顺序 |
| Mermaid 2 | 自绘（据 §3.1–3.3 描述） | 5 推理与系统链路 | 流式推理管线：AR 步进 → 双头解码 → 音频波形 / 运动 latent → 外部 LIA-X 渲染 |

- **公式**：3–4 个（逐位置相加融合 Eq. 2、stop predictor、CFM 目标、总损失 Eq. 4），LaTeX 取自 HTML 的 `annotation`。
- **表格承载证据**：Table 1–6 的关键数值按原文照录（含中/英双列）。
- **不采用**：PDF p4 的 242px 缩略图（发布后必糊）。

## 缺料项与处理

- **论文图少**（仅 1 张）→ 用 2 张 Mermaid 补结构，并在正文说明「本篇配图受论文限制」，不硬凑。
- **未入本地 papers 库** → 正文条目写 `arxiv-2604.23586`，sidecar `notes` 记明。
- SyncNet C/D 量纲与 UTMOS 张力 → 照录 + 事实核对注，不做跨来源横比。
- speaker embedding 抽取模型、CFG 随机丢弃概率、训练硬件等未披露 → 写「未披露」。

## Decisions

- **D1 采用 10 节深读骨架**，但配图策略按论文实况调整为「1 原图 + 2 Mermaid」。
- **D2 与知识库的分工**：论文机制归本篇；我方上游固定版本（`6712f62`）的接入状态与验证细节仍归 knowledge 两篇，本篇只做前向链接。
- **D3 数字风险显式化**：UTMOS 张力与 SyncNet 量纲必须在同段标注。
- **D4 链接回补 2 处**：`knowledge/Talker-T2AV 模型精读.md`、`knowledge/Talker-T2AV 接入与验证.md`。

## Risks / Trade-offs

- **配图不足可能被误读为资料不全** → 在正文与 sidecar 明确「论文仅 1 图，其余为表」，并把 6 张表的关键结论写进正文。
- **视频侧依赖 LIA-X** → 与 `lia-x` 笔记互链，避免重复解释该编码器。
