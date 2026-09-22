## Context

`management/docs/论文笔记/avatar-forcing.md` 已多处使用 DPO，却只给出偏好对和联合损失，既没有解释 DPO 的通用机制，也没有讲清该论文自己的偏好判别、逐帧损失、配置和消融结果。项目 wiki 中也没有任何一篇可复用的 DPO 说明，其他模型笔记遇到同一术语时无处可链。

本变更拆成两件互不越界的事：

1. 新增一篇**通用 DPO 技术介绍**，作为可被任意模型笔记复用的术语入口。
2. 让 `论文笔记/avatar-forcing.md` 承担**该论文如何使用 DPO** 的全部细节，并链接到技术介绍。

已有可核查素材位于 `.cache/article-note/avatar-forcing/`（Avatar Forcing 论文自带背景与附录）：

- `raw/source-tar/sec/3_background.tex`：通用 DPO 目标、条件 / 偏好对 / 冻结参考模型 / `β` 的定义，以及 DiffusionDPO 的定位。
- `raw/source-tar/sec/4_method.tex`：该论文的问题动机、`m^w` / `m^l` 构造、联合目标。
- `raw/source-tar/sec/X_suppl.tex`：逐帧独立加噪、以向量场预测误差改写的 DPO 目标、`v_ref` 与训练配置。
- `raw/source-tar/sec/5_experiments.tex`、`table/ablation_full.tex`：DPO 消融的定性与数值结论。
- 既有 `analysis/terminology.md`、`analysis/experiment.md`：来源指针与结论摘要。

通用 DPO 部分还需要外部一手资料（原始 DPO 论文、DiffusionDPO 论文及后续变体），当前机器网络探测为 `PROXY_OFF`，仅 OpenAlex 直连可用；书目核实安排在素材阶段完成。

`management/docs/` 当前没有技术介绍目录。文档接口递归扫描非下划线目录，接受中文子目录 slug，因此拟新增 `management/docs/技术介绍/`，不需要代码改动。该目录未被显式排序，按当前约定会排在「数字人概述 / 论文笔记 / knowledge」之后。

## Goals / Non-Goals

**Goals:**

- 新建一篇通用 DPO 技术介绍：给出中英文全称、适用问题、通用目标与推导直觉、参考模型与 `β` 的作用、边界与常见变体。
- 在通用范围内介绍 DPO 向扩散模型的扩展（DiffusionDPO），说明「序列概率比较 → 扩散似然 / 向量场误差比较」这一步，使该概念可被任何扩散类模型笔记复用。
- 以简短方法谱系和延展阅读定位 IPO、KTO、ORPO、SimPO 所处理的问题，不展开为偏好优化算法综述。
- 让 `论文笔记/avatar-forcing.md` 完整承担该论文的 DPO 应用：偏好判别怎么来、逐帧损失怎么算、与原 DF 目标怎么联合、配置是什么、消融取得了什么收益与取舍。
- 文档职责单一：技术介绍只讲通用机制，论文笔记只讲该论文的选择与结果，两者用站内链接相连。

**Non-Goals:**

- 技术介绍中**不写 Avatar Forcing 的内容**：不出现该论文的偏好对构造、`m^w` / `m^l`、`L_ft`、`λ=0.1`、`β=1000`、5k 步或消融数值；这些全部属于论文笔记。
- 不修改论文笔记中与 DPO 无关的章节、配图、实验表格或工程实测内容。
- 不扩展为 RLHF / 奖励模型训练或其他偏好优化算法的综述；变体只在延展阅读中标注职责。
- 不新增前后端功能、目录排序配置或外部依赖。

## Decisions

### 1. 目录与文档边界

在 `management/docs/技术介绍/` 新建 `dpo-直接偏好优化.md` 及同名 sidecar `dpo-直接偏好优化.json`。文件 frontmatter 含 `title`、`date`、`tags`、`summary`、`order`；sidecar 的 `related` 登记到 `论文笔记/avatar-forcing`。正文的跨文档引用使用 `[[技术介绍/dpo-直接偏好优化|直接偏好优化（DPO）]]` 形态。

选择独立「技术介绍」目录而非放进 `knowledge/` 或继续塞入论文笔记：用户要求建立可复用的技术介绍子文件夹；独立文档才能让通用原理与论文特例各自保持单一职责，并允许后续同类内容复用。新目录暂不改服务端排序常量，避免为一篇文档改变全站导航语义。

### 2. 技术介绍的完整章节结构

目标读者是需要在项目内理解或复用 DPO 的研发读者；用途是项目 wiki 的术语入口，与具体论文解耦。正文只使用 `##` / `###` 标题，不出现素材路径、出处或任何具体论文的应用细节。

| 节 | 标题 | 内容、论证与结论 | 必备元素 |
|---|---|---|---|
| 1 | `## DPO 解决什么问题` | 从「同一条件下可有多个合理输出」切入：常规监督只拟合单个示例，无法表达更倾向哪一个；经典 RLHF / InstructGPT 路线需要偏好数据、显式奖励模型和后续优化三段；DPO 一步吃下 winner / loser 对。结论：DPO 省掉的是显式奖励模型，不是偏好数据本身。 | 谱系 Mermaid 图：RLHF / InstructGPT → DPO → DiffusionDPO；术语小表：条件 `c`、winner `x^w`、loser `x^l`、当前模型、参考模型、`β`。 |
| 2 | `## 通用 DPO 目标如何比较偏好对` | 给出原始 DPO 目标；逐项拆解 sigmoid 内的「winner 相对参考模型的对数概率变化」减去「loser 的相对变化」，说明被优化的是**相对冻结参考模型的偏移**，`β` 控制允许偏离参考模型的程度。 | 一条 fenced `text` 公式；变量表；winner / loser → 当前模型与参考模型 → 偏好损失的 Mermaid 流程图。 |
| 3 | `## DPO 为什么不需要奖励模型` | 说明 DPO 的推导直觉：在 KL 约束的最优解下，奖励可由当前策略与参考策略的对数比值隐式表达，代回偏好损失即消掉奖励项。同时给出边界：依赖 Bradley-Terry 式偏好假设、需要成对数据、可能过拟合偏好数据或受长度等偏置影响。结论：省去奖励模型不等于没有隐含奖励，也不等于偏好信号自动可得。 | 隐式奖励表达式的 `text` 公式；「DPO 解决 / 未解决」对照表。 |
| 4 | `## 从序列概率到扩散模型` | 扩散 / 流匹配模型不直接以离散 token 概率作为训练接口，因此 DPO 的「概率比」需要改写。介绍 DiffusionDPO 的思路：用扩散似然（ELBO 近似）替换序列对数概率，最终落到对加噪样本的**去噪向量场预测误差**比较；保留 motion latent 无关的通用符号说明（噪声时间、噪声样本、目标向量场）。结论：这是 DPO 在扩散模型上的通用改写，与具体模态无关。 | 扩散前向加噪公式与目标向量场公式（fenced `text`）；「clean sample → noise mix → vector-field prediction → 偏好比较」Mermaid 图。 |
| 5 | `## 常见变体与适用边界` | 按职责简述后续变体：IPO 针对偏好数据过拟合 / 稳定性，KTO 使用二元好坏反馈而非成对偏好，ORPO / SimPO 尝试减少或去掉参考模型依赖；并说明 DPO 之外仍有 RLHF、奖励模型等其他路线。结论：选择哪种取决于偏好数据形态与算力约束，本文不展开推导。 | 变体表（方法、所处理问题、相对 DPO 的改变）+ 谱系补全图。 |
| 6 | `## 术语与符号表` | 汇总全文中英文术语与符号，使读者无需回前文查找。 | 术语表 + 符号表。 |

不需要为通用机制新做实验或推断：第 1–3、5 节依据原始 DPO 论文及其公开变体论文，第 4 节依据 DiffusionDPO 论文；素材阶段须逐篇核实书目信息与公式符号，不凭记忆书写公式。

### 3. 论文笔记中的改动

`论文笔记/avatar-forcing.md` 承担该论文使用 DPO 的全部细节，改动范围：

- 「一句话总结」中首次出现的 DPO 改为带全称的站内链接：`[[技术介绍/dpo-直接偏好优化|直接偏好优化（DPO）]]`。
- 「表达力：把 DPO 用在运动隐变量上」一节扩写为该论文专属内容：
  - 两阶段训练：Stage 1 训练基础 motion generator，Stage 2 以 Stage 1 权重初始化并冻结 `v_ref` 后做偏好微调；
  - 偏好判别来源：winner `m^w` 为真实视频运动 latent，loser `m^l` 为仅给 avatar 音频的 FLOAT 生成结果，「丢弃用户条件」只发生在**生成 loser** 时，DPO 训练仍用完整条件 `c=(a_u,m_u,a)`；
  - 逐帧损失：winner / loser 共用同一噪声序列、按帧独立 `t_n` 加噪，比较 `v_θ` 与 `v_ref` 的向量场预测误差相对变化；
  - 联合目标 `L_ft = L_DF + λL_DPO`，以及保留 `L_DF` 的意义；
  - 配置：`λ=0.1`、`β=1000`、5k 步、继续训练无额外增益；
  - 消融收益与取舍：反应性 rPCC-Exp / rPCC-Pose 与动作丰富度 SID / Var 明显改善，FID / FVD 改善，CSIM 与 LSE-C 小幅回落——如实写明，不写成全指标提升；结合论文可视化说明去 DPO 后表情 / 头动多样性下降、对微笑反应变弱。
- 通用 DPO 推导（目标函数、`β` 语义、免奖励模型原理）在笔记中压缩为链接，不在两篇中重复。
- 训练表、实验表格与其余章节不做非必要改写。

同步将新文档加入 Avatar Forcing sidecar 的 `related`；新文档 sidecar 以对象形式登记可点击 slug、标题和职责说明，供页面「相关文档」块使用。

### 4. 素材审核与事实口径

在用户审核结构后、写正文前，按 Article Note 流程在对话中提交素材摘要，不把素材整理产物写入仓库。摘要分两组逐项列出：

- **通用 DPO 组**：原始 DPO 论文、DiffusionDPO 论文及 IPO / KTO / ORPO / SimPO 的书目信息与核实状态、通用目标公式与变量定义、隐式奖励推导要点、扩散改写的关键步骤。
- **Avatar Forcing 组**：`m^w` / `m^l` 来源与完整条件、附录的逐帧加噪与损失公式、`λ/β/v_ref/steps` 配置、消融全量数值及其取舍，每项附原始 TeX 行段。

用户确认素材口径后，才进入写作阶段。

## Risks / Trade-offs

- [公式在 Markdown / TeX 抽取中丢失符号或正负号] → 撰写前直接核对原始论文的 LaTeX 源码（Avatar Forcing 用 `sec/3_background.tex`、`sec/X_suppl.tex`；通用 DPO / DiffusionDPO 用其官方版本），公式以 fenced `text` 呈现并配中文变量表。
- [书目信息凭记忆写错] → 当前为 `PROXY_OFF`，仅 OpenAlex 直连可核实；素材阶段逐篇核实 arXiv / DOI，未核实的编号不得写入正文。
- [技术介绍被写成某篇论文的附录] → design 明确 Non-Goals：技术介绍不出现 Avatar Forcing 的任何具体取值；审核时以此为准。
- [两篇内容重复或链接失效] → 技术介绍负责通用机制，笔记负责论文选择与结果；完成后核验目标 slug 存在且链接可由文档接口解析。
- [把「无人工标注」误写成「没有偏好信号」] → 论文笔记中明确偏好信号由真实运动 latent 与仅音频 loser 的构造提供，只是不额外收集人工标注。
- [新目录在导航中排在较后] → 保持现有不改动排序的非侵入方案；后续出现多篇技术介绍时再单独提 change 决定目录顺序。

## Migration Plan

1. 用户确认本大纲后，整理并提交素材摘要（通用 DPO 组 + Avatar Forcing 组）供第二次审核。
2. 用户确认素材后，创建技术介绍正文与 sidecar，并按计划扩写 Avatar Forcing 笔记的 DPO 相关表述、更新其 sidecar。
3. 运行 Markdown / JSON 格式检查、`openspec validate --change docs-add-dpo-technical-intro`，并调用文档列表与详情接口检查新 slug 与跨文档链接。
4. 若需回滚，删除技术介绍的 `.md` / `.json`，并还原 Avatar Forcing 的链接、扩写段落与 sidecar；不涉及数据库迁移或服务端状态。
