## Context

- **素材**（`.cache/article-note/omnimate/`，已通过 `validate-analysis.py`）：**source tarball 成功** → `raw/source-tar/Arxiv.tex`（单文件 LaTeX，公式/图题权威）+ `raw/source-tar/Figures/{teaser,method,train_GPC,result,ablation}.pdf`（5 张矢量原图，tex 里带 `trim/clip`）；`raw/sources/omnimate.pdf` 取页码。
- **元信息**：arXiv `2607.23023`（2026-07-25，v2 2026-07-28）；标题 *OmniMate: Open-Ended Real-Time Streaming Audio-Visual Generation for Interactive Avatars*；作者 Quanyue Song、Yishan He、Yanbo Ding、Zhixiang He、Yongxiang Li、Caigui Jiang、Zhizhi Guo；单位 西安交通大学（人机混合增强智能全国重点实验室 / 人工智能与机器人研究所）、中国电信人工智能科技（北京）、中科院深圳先进技术研究院；模板为 AAAI 2027，**首页未见录用标注 → 不声明会议**。
- **我方关联**：未接入；本篇为谱系/定位层，价值在「开放时长与长时身份漂移」这两个问题的机制解法，与《数字人领域问题》《数字人身份》的叙述互相印证。

## Goals / Non-Goals

**Goals:**
- 按 10 节骨架成文；采用 5 张论文原图并逐图配中文图题与解读
- 讲清两个核心机制：**GPC**（把 progress 显式编码为连续条件加到 latent 上，1–1000 表示 execution、0 表示 listening；Sinusoidal PE + MLP 后逐元素相加）与 **MRCM**（视觉身份条件需训练、说话人身份条件 training-free）
- 讲清四阶段训练（微调视觉身份 → DMD 蒸馏双向教师 + 构造状态切换 ODE 轨迹 → ODE 初始化联合优化 GPC 与学生（因果掩码）→ self-forcing DMD 再蒸馏）

**Non-Goals:**
- 不写我们的实测（未接入）
- 不把未公开定义的指标（FPS/TTFF/Speech/IB-Score 的实现口径）当作可复现结论；主结果表照录并标注
- 不改其它笔记与概述正文（仅 1 处链接替换）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位 / venue（不声明会议）/ arXiv（`2607.23023`）/ papers 库条目（`arxiv-2607.23023`）/ 历史博客精读（`omnimate-2026.html`） |
| 1 | 一句话总结 | 开放时长 + 实时流式交互头像：LLM 产出「回复内容 / 动作指令 / 预估执行时长」→ GPC 把时长转成 progress 条件控制 execution↔listening 切换；MRCM 提供持久视觉与说话人身份线索；骨干为 LTX2.3 轻量适配（§Introduction；§Method-Overview；Figure 1/2） |
| 2 | 问题与动机 | ① 开放时长下无法确定「生成地平线」（固定时长会截断/冗余，显式完成检测引入延迟）；② 长时跨模态身份漂移（视觉上下文有限 → 视觉漂移；语音上下文有限 → 音色不一致）（§Introduction p1–p2） |
| 3 | 方法精析 | 统一音视频骨干（LTX2.3）+ 双注入：GPC 进度条件（值域 1–1000/0，Sinusoidal PE + MLP，**latent addition**，式 3）；MRCM 两条件（视觉身份：多参考图拼到时间维 + 负 RoPE，需训练；说话人身份：推理期替换音频 latent，training-free）；图 1（论文 Figure 2）、图 3（论文 Figure 1） |
| 4 | 训练与实现细节 | 四阶段：① 微调 LTX2.3 视觉身份条件 → ② DMD 蒸馏少步双向教师 + 构造状态切换 ODE 轨迹 → ③ ODE 初始化，联合优化 GPC 与学生（因果掩码）→ ④ self-forcing DMD 再蒸馏；**弃用原始多步 diffusion teacher**；图 2（论文 Figure 3）；未披露项照写 |
| 5 | 推理与系统链路 | 流式推理管线（音频/视频分块生成与状态切换）；GPC 的 progress 如何驱动 execution→listening；Mermaid 时序图 |
| 6 | 实验与结果 | VerseBench：**FPS 27.64 / TTFF 3.49s**（论文自报实时）；A-ID/V-ID、Speech 0.097、IB-Score 0.356 最优或次优；VQ 与 LSE-C 具竞争力；**但 AQ/VQ/Sync-D/LSE-C 并非第一**，且多数胜出指标（FPS/TTFF/Speech/IB-Score）**依赖未公开定义的实现**，正文须标注该风险；消融：`w/o GPC`(Speech 0.239)、`w/o DistillTeacher`(0.489)、`w/o DataConstruct`(0.382)、`w/o MRCM`(A-ID 0.462 / V-ID 0.94…)；30s–240s 长时无显著退化；图 4（论文 Figure 4）、图 5（论文 Figure 5） |
| 7 | 相关工作与定位 | 流式视频生成（StreamChar、WanStream）依赖大规模训练/大量参数 → 本篇为 **lightweight adaptation**；与 dual-DiT 联合生成、级联 ASR→LLM→TTS→Avatar 的差别 |
| 8 | 局限与启发 | 论文自陈与实测缺口：指标实现未公开、部分指标非最优；「论文局限 vs 我们结论」对照表（我方未接入）；可操作启发（把「还要说多久」显式参数化为连续条件；用 training-free 的说话人条件替换对抗音色漂移） |
| 9 | 术语与符号表 | GPC / progress conditioning / execution & listening / MRCM / reference speech / negative RoPE / DMD 蒸馏 / self-forcing / TTFF |
| 10 | 相关文档 | `[[数字人概述/数字人领域问题]]`、`[[数字人概述/数字人身份]]`、`[[数字人概述/数字人动作]]`、`[[论文笔记/avatar-forcing]]`、`[[论文笔记/liveact]]`、博客精读条目 |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | Figure 1（`teaser.pdf`，`trim=20 290 20 30`） | 1 一句话总结 | 任务定义与交互态切换能力 |
| 图 2 | Figure 2（`method.pdf`，`trim=20 250 20 30`） | 3 方法精析 | 流式推理管线 + GPC 的角色 |
| 图 3 | Figure 3（`train_GPC.pdf`，`trim=40 300 40 20`） | 4 训练与实现细节 | GPC 训练：DMD 教师 → ODE 轨迹 → 训练目标 |
| 图 4 | Figure 4（`result.pdf`，`trim=15 270 15 30`） | 6 实验与结果 | 与 SOTA 定性对比 |
| 图 5 | Figure 5（`ablation.pdf`，`trim=15 130 15 30`） | 6 实验与结果（消融） | 完整模型在交互自然度/视觉锚定上的必要性 |

- **公式**：3–4 个（progress 条件注入式、AR/流式生成目标、DMD 蒸馏目标、训练损失），LaTeX 取自 `Arxiv.tex`。
- **Mermaid**：1 张（流式推理与状态切换时序）。

## 缺料项与处理

- 矢量图 `trim` 参数需等效处理 → 栅格化后用 Pillow 去白边；若误伤内容再按参数手裁。
- 指标实现未公开（FPS/TTFF/Speech/IB-Score）→ 正文标注「口径未公开，不可复现验证」。
- venue 未见录用标注 → 不声明会议；AAAI 2027 模板仅作为排版事实记录在 sidecar。

## Decisions

- **D1 采用 10 节深读骨架**，图号按论文顺序（Fig 1 放 §1、Fig 2 放 §3、Fig 3 放 §4、Fig 4/5 放 §6）。
- **D2 指标风险显式化**：主结果表照录，但必须同段标注「多数胜出指标依赖未公开实现」。
- **D3 定位层**：第 8 节写未接入 + 两个可复用机制（显式进度条件、training-free 说话人条件）。
- **D4 链接回补 1 处**：《数字人领域问题》250 行。

## Risks / Trade-offs

- **指标口径不可验证** → 只用论文自报值并标注，不与其它论文横比。
- **与《数字人领域问题》已有段落重叠** → 本篇只写机制与训练细节，问题叙事仍归《领域问题》。
