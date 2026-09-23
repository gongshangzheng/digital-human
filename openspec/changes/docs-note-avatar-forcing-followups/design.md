## Context

用户提问："Avatar Forcing 的优点（低维运动隐变量换来的实时、DPO 换来的灵动）有没有后续工作继承并做得更好？" 首轮我用 OpenAlex 查得 `cited_by_count: 0` 并据此回答"没有引用验证的后继"，**该结论是错的**——OpenAlex 对 2026 年论文的引文回溯滞后严重；改用 Semantic Scholar 的 `/paper/arXiv:<id>/citations` 后得到：

- `2601.00664`（本篇，KAIST / CVPR 2026）：**16 篇引用**，influential 4，references 69；
- `2603.14331`（同名易混的另一篇，ZJU + 快手）：7 篇引用。

本仓库 `arxiv.org` 实际可直连（此前 skill 记为被墙），因此除引用列表外还读取了其中 6 篇的摘要原文用于核实继承关系。

此外核对出笔记里两处事实问题：`arXiv` 行把 v2 日期写成 2026-01-02（arXiv 页为 v1 2026-01-02、last revised 2026-05-30）；"代码仓库未公开"缺少当前的开放替代（AVTR-1 开放栈）。

## Goals / Non-Goals

**Goals:**

- 补齐「后续工作」：把 16 篇按"继承哪个优点"分组，给出 arXiv 编号与该工作相对本篇的推进点。
- 给出两条**仍然空着**的方向（低维运动隐变量的显式控制接口；低维运动子空间上的偏好优化），并写明判断依据是"16 篇里没有一篇做这件事"。
- 把 DynaForcing 的 **dynamic collapse** 与本篇的递归自条件做机制对照，并**显式标注设定差异**（DMD 蒸馏 vs diffusion forcing），避免读成等价结论。
- 修正「论文信息」的版本日期与代码仓库两行，补被引数。
- 把 Causal Forcing 与 Wan-Streamer 登记进待读清单。

**Non-Goals:**

- 不改 `## 方法精析`、`## 训练与实现细节`、`## 实验与结果` 的任何数据、公式、配图。
- 不为这 16 篇逐一写笔记；只在本篇做"后续工作"定位表。
- 不新增 `论文笔记/*.md` 正文文件（待读只登记在 README 清单）。
- 不因为发现了 16 篇引用就去改「局限与启发」里我们自己的实测结论。

## Decisions

### 1. 「后续工作」放在第 7 节，按"继承的优点"分组

放在 `## 相关工作与定位` 内（该节已承担定位职责），追加一个小节；不新开 `##` 级章节（10 节骨架固定）。分组口径与用户的三个优点对齐：

| 分组 | 工作（arXiv） | 相对本篇的推进 |
|---|---|---|
| 流式 / 实时架构 | Causal Forcing `2602.02214`、Causal Forcing++ `2605.15141` | 指出双向教师→因果学生的 ODE 蒸馏需要"帧级单射性"，违反后只能得条件期望解；给出修正并推进到逐帧自回归 + 1–2 步采样 |
| 流式 / 实时架构（失效分析） | DynaForcing `2608.17707`、Decoupled Self-Forcing Distillation `2609.10317`、Q-ARVD `2605.21072` | 把 self-forcing 蒸馏的 dynamic collapse 形式化；分别用解耦蒸馏、量化应对 |
| 双向交互 + 实时 | InterDyad `2603.23132`、ECHO `2603.17427`、Listener Nodding `2607.12329` | 把"会回应"细化为情绪恰当性与听者非语言动作的实时生成 |
| 偏好 / 强化学习提表达力 | GDPO-Listener `2603.25020`、Facial Expression Generation Aligned with Human Preference `2603.07093` | 前者用 Group reward-Decoupled Policy Optimization 在参数空间做解耦奖励（治 Regression-to-the-Mean）；后者把表情生成当 action learning 做人类反馈对齐 |
| 长时身份一致 | AsymTalker `2605.02948`、TaoMate `2607.24359` | 前者点名"跨块自生成连续性参考造成的级联身份漂移"；后者用 anchor-guided memory |
| 外推 | CausalCine `2605.12496`、LPM 1.0 `2604.07823`、Wan-Streamer `2606.25041`、AVTR-1 `2609.22913` | 多镜头叙事、角色表现基座、实时交互基座与开放栈 |

表中同时给出被引量级（Causal Forcing 134、Causal Forcing++ 30、LPM 1.0 9、CausalCine 8、Wan-Streamer 5），并注明口径为 Semantic Scholar、查询日期 2026-09-23。

### 2. 「仍然空着的两点」要写成可检验的判断

- **低维运动隐变量的显式控制接口**：16 篇引用中没有一篇回到"给运动自由度挂关键点/系数指令"；
- **低维运动子空间上的偏好优化**：偏好/RL 都发生在 FLAME 参数空间（GDPO-Listener）或像素/整帧层，没人回到本篇的 20 维运动子空间。

两条都要写成"截至 2026-09-23 的 16 篇引用范围内未见"，而不是"不存在"。

### 3. DynaForcing 的对照写法（防止过度推广）

在「局限与启发」加一段，措辞必须包含三件事：DynaForcing 研究的对象是 **self-forcing + DMD 蒸馏**；本篇用的是 **diffusion forcing**（非 DMD）；两者的共同点是"自条件反馈环会压低运动"，因此只作**机制对照**，不宣称 DynaForcing 的结论直接解释本篇。这段的用途是提示：DPO 是在对抗内生塌陷，而不是一个独立增益。

### 4. 「论文信息」的两处事实更正

| 行 | 现状 | 改为 |
|---|---|---|
| arXiv | `` `2601.00664`（v2，2026-01-02） `` | `` `2601.00664`（v1 2026-01-02；v2 2026-05-30） `` |
| 代码仓库 | `未公开；我们接入的是 CyberVerse ...` | 保留原内容，追加"开放替代可参考 `AVTR-1`（arXiv:2609.22913）" |
| 新增 | — | `被引`：16（Semantic Scholar，2026-09-23；influential 4），细节见「相关工作与定位」 |

### 5. 待读清单登记格式

在 `论文笔记/README.md` 的「现有清单」表末尾追加两行，沿用既有格式（第二列写定位 + `｜论文 [arXiv:xxxx](链接) 标题`，第三列写状态）：

| 文件 | 定位 |
|---|---|
| `causal-forcing.md` | 深读（自回归扩散蒸馏：帧级单射性、条件期望解、1–2 步逐帧自回归） |
| `wan-streamer.md` | 深读（端到端实时交互基座） |

不在本次创建这两个 `.md` 文件。

## Risks / Trade-offs

- [把引用数当结论] → 表中标注来源为 Semantic Scholar 与查询日期；不写"排名"，只写被引量级。
- [只有标题没有内容就写"推进点"] → 推进点只写进读过摘要的条目（Causal Forcing、Causal Forcing++、GDPO-Listener、AsymTalker、Human-Preference Expression、DynaForcing 共 6 篇）；其余条目只写"继承哪个优点"这一层。
- [DynaForcing 被读成本篇的直接解释] → Decision 3 强制写明设定差异。
- [待读条目与将来的笔记冲突] → 只登记队列，不预写正文；将来写笔记时按 article-note 流程另开 change。
- [漏掉同名易混那篇的引用] → 一并记录 `2603.14331` 的 7 篇引用作为附注，避免读者混淆归属。

## Migration Plan

1. 用户审核本 design（分组口径、6 篇"推进点"的证据边界、DynaForcing 措辞、待读两行）并确认。
2. 修改三个文件：`avatar-forcing.md`（§0 / §7 / §8）、`README.md`（清单）、`avatar-forcing.json`（changelog）。
3. 校验：Markdown / JSON 合法、站内链接目标存在、无 `##` 级新增、表格列数一致、`openspec validate --strict`、经 FastAPI 接口确认两篇文档可读。
4. 回滚：还原三处文件即可。

## Resolved Decisions

| # | 事项 | 结论 |
|---|---|---|
| 1 | 是否更新笔记 | **更新**（用户已确认"好的，更新"） |
| 2 | 待读登记对象 | **Causal Forcing（`2602.02214`）与 Wan-Streamer（`2606.25041`）** 两篇，登记在 `论文笔记/README.md` 的「现有清单」，状态 `待写` |
| 3 | 是否同时修正笔记里的版本日期 | 默认**修正**（v1 2026-01-02 / v2 2026-05-30），因 arXiv 页明确 |
