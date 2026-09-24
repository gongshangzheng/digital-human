## Context

- 这十篇的共同素材来源：`management/docs/knowledge/视频生成训练与推理加速专题.md`（含每个工作的核心做法、训练要求、报告口径与**证据等级**）+ 博客 `video-gen-acceleration`。证据等级的分档（论文已验证 / 代码或 README 证据 / 仓库 benchmark / 待自测）必须原样带进各笔记的「证据状态」，不得升格为「同协议可横比」。
- 八篇有 arXiv 论文（HTML 已抓取，部分含 PDF）：
  > **范围变更**：`fpsattention`（arXiv 2506.04648）已由另一会话完成并归档（`openspec/changes/archive/2026-09-24-docs-note-fpsattention`，笔记与资产 `x1/x2/x3.webp` 均已入库），**不再属于本 change 范围**；本 change 实际覆盖 9 篇（blade、latent-spatial-memory、zipar、nar、flashar、turbodiffusion、inferix + 仓库类 worldattention、dax）。

  | slug | arXiv | 论文标题 | HTML 大图数 |
  |---|---|---|---|
  | `blade` | 2508.10774 | BLADE: Block-Sparse Attention Meets Step Distillation for Efficient Video Generation | 5 |
  | `latent-spatial-memory` | 2606.09828 | Latent Spatial Memory for Video World Models | 6 |
  | `zipar` | 2412.04062 | ZipAR: Parallel Auto-regressive Image Generation through Spatial Locality | 5 |
  | `nar` | 2503.10696 | Neighboring Autoregressive Modeling for Efficient Visual Generation | 8 |
  | `flashar` | 2605.09430 | FlashAR: Efficient Post-Training Acceleration for Autoregressive Image Generation | 10 |
  | `turbodiffusion` | 2512.16093 | TurboDiffusion: Accelerating Video Diffusion Models by 100-200 Times | 0 |
  | `inferix` | 2511.20714 | Inferix: A Block-Diffusion based Next-Generation Inference Engine for World Simulation | 2 |
- 两篇**没有论文**（知识库的证据等级即「代码/README」「仓库 benchmark」）：`worldattention`（HSA 混合稀疏注意力 + 分层 KV cache）、`dax`（算子/系统侧组合优化）。这两篇按**仓库/技术报告类笔记**处理：不用 10 节论文骨架，改用「能力与边界」骨架（见 D2），素材以仓库 README/代码与知识库整理为准，且必须写明「无同行评议论文」。
- 与《数字人加速》的关系：该篇「生成侧加速」四方向（内核与稀疏 / 步数变少 / 缓存复用 / 并行与推理引擎）里点名了这十个工作但未加链接；笔记建成后回补链接。

## Goals / Non-Goals

**Goals:**
- 十篇笔记齐备，每篇能让读者回答三件事：它优化哪一段成本、需要什么训练前提、证据到什么等级
- 论文类笔记按 10 节骨架（受素材限制的条目允许精简，缺口写明）；仓库类笔记按 D2 骨架
- 回补《数字人加速》的十个链接；同步 README 与伞 change 状态

**Non-Goals:**
- 不做十篇之间的统一速度排行榜（论文/仓库口径不同，知识库已明确禁止拼接）
- 不把「仓库 benchmark」（DAX 的 8 卡 36.4×）写成单卡或可比数字
- 不为没有图的论文凑图（turbodiffusion 的 HTML 无大图 → 用 Mermaid/表）

## 结构契约

### D1 论文类笔记（8 篇）——10 节骨架，按素材实况精简
沿用 `论文笔记/README.md` 的 10 节骨架；每篇必须写清：
1. **它加速的是哪一段**（注意力/步数/缓存/系统），对应《数字人加速》的哪个方向；
2. **训练前提**（是否需要 QAT / 蒸馏 / 后训练 / 从头训练 / 零训练）——这是知识库表格的核心列；
3. **证据状态**：论文已验证 / 代码或 README 证据 / 仓库 benchmark / 待自测（原样带等级，不升格）；
4. **报告口径与边界**（模型规模、分辨率、硬件、是否 8 卡等），并注明不可与其它论文直接横比。

未披露项写「未披露」；无原图时用 Mermaid + 表格承载。

### D2 仓库/报告类笔记（2 篇）——能力与边界骨架（不套论文 10 节）
1. `## 是什么`：它是什么形态（内核/引擎/工具链），上游在哪（仓库/报告）
2. `## 机制与依赖`：核心做法 + 训练/工程前提（WorldAttention：HSA + 分层 KV，三阶段训练；DAX：序列并行 + SageAttention + compile + INT8 线性层 + TeaCache）
3. `## 报告口径与证据等级`：知识库里的数字与硬件口径（WorldAttention：单 H100 kernel 14.02× / E2E 2.21× / 22fps；DAX：8×H20 6836s→188s、36.4×），**标注无同行评议论文**
4. `## 能否落到我们的管线`：与《数字人加速》《工程设计》的关系与前置条件
5. `## 参考与延伸`：仓库/报告链接、相关笔记

### D3 统一来源标注
每篇第 0 节（或 D2 的第 1 节）必须写明素材来源性质：论文/仓库/知识库整理，并标注「本仓库知识库整理」这类二手性质。

## 图表与公式清单（按篇）

- `blade`：块稀疏 + 步数蒸馏联合训练框架图（采用论文 Figure 1 + Figure 4 掩码可视化），公式 1–2 个
- `latent-spatial-memory`：latent 3D 记忆与消融图（6 张中选 1–2），Mermaid 1 张（记忆读写路径）
- `zipar`：并行解码示意（5 张中选 1），公式 1 个（并行窗口）
- `nar`：next-neighbor 目标示意（8 张中选 1–2），公式 1–2 个
- `flashar`：双头并行示意（10 张中选 1），公式 1 个
- `turbodiffusion`：无大图 → Mermaid 1–2 张（rCM 蒸馏 + 系统优化栈）+ 表
- `inferix`：block-diffusion 引擎架构（2 张中选 1），Mermaid 1 张（跨块状态/KV 管理）
- `worldattention` / `dax`：无原图 → 各 1 张 Mermaid（架构/优化栈）+ 表

## 缺料项与处理

- 部分论文只有 HTML、无 PDF → 页码类引用改写为「章节号 + 图/表号」，不编造页码。
- `turbodiffusion` HTML 无大图 → 不配原图，用 Mermaid + 表格（正文说明）。
- `worldattention` / `dax` 无论文 → 按 D2 骨架，且明确「无同行评议论文」。
- 十篇均未入本地 papers 库（`data/papers.db`）→ `papers_id` 按命名规范写，sidecar `notes` 记明。

## Decisions

- **D1** 论文类沿用 10 节骨架（受素材限制允许精简并写明）。
- **D2** 仓库类用「能力与边界」骨架，不冒充论文笔记。
- **D3** 证据等级原样带出，禁止跨口径横比（知识库已声明过的边界）。
- **D4** 分批实施：先「注意力/内核 + 缓存」组（fpsattention、blade、latent-spatial-memory），再「自回归并行」组（zipar、nar、flashar），最后「端到端系统 + 仓库类」（turbodiffusion、inferix、worldattention、dax）；每批完成即校验并提交。
- **D5** 全部建成后一次性回补《数字人加速》的十个链接（避免分批改动同一段落）。

## Risks / Trade-offs

- **十篇同类笔记容易写成目录式重复** → 每篇强制写「它加速哪一段 + 训练前提 + 证据等级 + 能否落到我们管线」四问，避免同质化。
- **仓库类证据弱** → 用 D2 骨架显式标注，不给出「可用于生产」的推论。
- **批次多、跨度长** → 每批独立提交，README 状态随批次更新，最终统一回补链接。
