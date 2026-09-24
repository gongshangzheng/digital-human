## 1. 设计与素材确认

- [x] 1.1 用 Semantic Scholar 取回 `2601.00664` 的 16 篇引用与 `2603.14331` 的 7 篇引用（含 arXiv 编号、年份、被引量级、第一作者）。
- [x] 1.2 读取其中 6 篇 arXiv 摘要原文用于核实推进点：Causal Forcing `2602.02214`、Causal Forcing++ `2605.15141`、GDPO-Listener `2603.25020`、AsymTalker `2605.02948`、Human-Preference Expression `2603.07093`、DynaForcing `2608.17707`。
- [x] 1.3 核对 `arxiv.org/abs/2601.00664` 的版本信息（v1 2026-01-02、last revised 2026-05-30）与被引数口径。

## 2. avatar-forcing.md 更新

- [x] 2.1 §0 论文信息：arXiv 行改为 `v1 2026-01-02；v2 2026-05-30`；代码仓库行补 `AVTR-1`（`arXiv:2609.22913`）开放替代；新增「被引」行（16 / influential 4，Semantic Scholar，2026-09-23）。
- [x] 2.2 §7 新增「后续工作（16 篇引用，截至 2026-09）」：按六个分组写引用表（流式架构 / 失效分析 / 双向交互 / 偏好与强化学习 / 长时身份一致 / 外推），含 arXiv 编号、被引量级与推进点，并注明 OpenAlex 同期显示 0 属回溯滞后。
- [x] 2.3 §7 写明「仍然空着的两点」（低维运动隐变量的显式控制接口、低维运动子空间上的偏好优化），措辞限定为"截至上述 16 篇的范围内未见"。
- [x] 2.4 §7 附注同名易混那篇 `2603.14331` 的 7 篇引用，避免归属混淆。
- [x] 2.5 §8 新增 `### 后续文献的补充：运动塌陷被形式化`，写明 DynaForcing 的设定为 self-forcing + DMD 蒸馏、与本篇 diffusion forcing 不同，只作机制对照。
- [x] 2.6 未触碰 §3 方法精析、§4 训练细节、§6 实验数据与配图。

## 3. 待读清单与 sidecar

- [x] 3.1 `论文笔记/README.md`「现有清单」追加 `causal-forcing.md`（`arXiv:2602.02214`）与 `wan-streamer.md`（`arXiv:2606.25041`）两行，状态 `待写`，格式与既有行一致。
- [x] 3.2 未创建这两个 `.md` 正文文件。
- [x] 3.3 `avatar-forcing.json` 追加 changelog 条目（后续工作、两处事实更正、DynaForcing 对照），现共 3 条。

## 4. 验证与交付

- [x] 4.1 校验两个 Markdown 表格列数一致、`##` 级标题数未增（11 / 4）、笔误复查通过、`avatar-forcing.json` 合法。
- [x] 4.2 核对新写入的 17 个 arXiv 编号与 S2 返回清单逐条一致（正文出现 17 个 + 本篇自身 `2601.00664`，无漏、无多、无错）。
- [x] 4.3 `openspec validate docs-note-avatar-forcing-followups --strict` 通过；经 FastAPI 详情接口确认 `论文笔记/avatar-forcing` 与 `论文笔记/README` 可读。
- [x] 4.4 提交 `docs(note): ...`，仅包含预期文件。

## 4. 后续工作复查（2026-09-24，用户指令）

- [x] 4.1 Semantic Scholar 复查：仍 16 篇，构成有变——**+MindFlow（2606.27779）−TaoMate（2607.24359）**；被引数更新（Causal Forcing 135、CF++ 31）。
- [x] 4.2 补读剩余 11 篇 arXiv 摘要（一手），精读笔记落 `research/followups-refresh-2026-09-24.md`。
- [x] 4.3 TaoMate 归属修正：按摘要（few-step joint audio-video、anchor-guided memory）移入同名篇 2603.14331 附注；其「不可变视觉锚点」与我们锚帧库平行，标为跨篇对照。
- [x] 4.4 笔记「后续工作」小节重写：推进列全部填实、加 MindFlow 行、「仍然空着的两点」复查后保留（DSFD 也只到 motion captions）。
- [x] 4.5 avatar-forcing.json changelog 追加。
- [x] 4.6 校验（表格列数 / 链接 / 引号风格）与提交。

## 5. 概念澄清（用户提问派生，2026-09-24）

- [x] 5.1 「forcing」的命名来源：论文 Background 原文 "Diffusion forcing reformulates conventional **teacher forcing** in terms of diffusion models"——链条为 teacher forcing（RNN）→ diffusion forcing（每 token 独立噪声水平 $t_n$）→ Avatar Forcing；术语表「扩散强制」行补 lineage。
- [x] 5.2 「有没有蒸馏」：**没有**。Stage 1 用 DF 目标回归向量场、监督来自真实运动；Stage 2 DPO 的 $\pi_{\text{ref}}$ 是 Stage 1 自己的权重（正则锚点）；motion AE 从 FLOAT 权重**初始化后重训**（初始化≠蒸馏）。已在「训练与实现细节」表后补一条 blockquote 说明，并点明 Causal Forcing 批评的「双向教师蒸馏」是另一条路线。
- [x] 5.3 逐篇「问题→方案」清单落 `research/followups-problem-solution.md`（16 篇 + 三条横向规律）。
- [x] 5.4 校验（引号风格 / 表格列数 / 链接 / API）与提交。

## 6. 四处截断摘要补全（2026-09-24 续）

- [x] 6.1 DynaForcing：三层互补方案（Hybrid Forcing / Dynamics-Aware Reward Regularization / Reference Perturbation）+ 计算图剪枝与梯度回放降显存一个数量级 + Dyn-Deg 0.31→0.73、Sync-C 7.03→7.68。
- [x] 6.2 Q-ARVD：S1 最终质量感知帧加权、S2 离群感知自适应双尺度量化。
- [x] 6.3 ECHO：LCU + **SDCM**（只对非唇区域融合用户行为线索）。
- [x] 6.4 AVTR-1：补 **R-DGG** 度量（扣除听者历史与说话人动作后，说话人语音的额外预测信息；无配对音频的 talking head 与错配对不成立）与组件分别许可。
- [x] 6.5 research/followups-problem-solution.md 加「与本仓库的交叉点」三条（Reference Perturbation ↔ 我们参考条件化失败；DSFD 无双向教师 = 我主线处境；R-DGG = 可借用的交互评测工具）。
- [x] 6.6 笔记后续工作表四处同步 + 校验 + 提交。
