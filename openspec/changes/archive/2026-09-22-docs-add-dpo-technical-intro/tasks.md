## 1. 资料整理与审核

- [x] 1.1 核对 RLHF / InstructGPT、原始 DPO、DiffusionDPO 及 IPO / KTO / ORPO / SimPO 的书目信息（arXiv / DOI）与本文不展开的边界；未核实的编号不得写入正文。
- [x] 1.2 提取通用 DPO 目标、隐式奖励推导要点、扩散改写关键步骤与变量定义，标注来源版本。
- [x] 1.3 逐行核对 Avatar Forcing 原论文中偏好判别、逐帧向量场损失、联合目标、训练配置与消融全量数值，附 TeX 行段。
- [x] 1.4 在对话中提交两组素材摘要（通用 DPO 组 + Avatar Forcing 组）供审核。
- [x] 1.5 获得用户对素材口径的明确确认后，再进入正文撰写。

## 2. 技术介绍文档（通用 DPO）

- [x] 2.1 创建 `management/docs/技术介绍/dpo-直接偏好优化.md`，按 design 的六节结构写通用 DPO：问题、通用目标、隐含奖励与边界、扩散模型扩展、变体、术语表。
- [x] 2.2 确保正文不出现任何具体论文的应用取值（不写 Avatar Forcing 的 `m^w` / `m^l`、`L_ft`、`λ`、`β`、步数或消融数值）。
- [x] 2.3 在延展阅读中定位 IPO / KTO / ORPO / SimPO 的问题边界，不扩写为偏好优化综述。
- [x] 2.4 创建同名 sidecar JSON，登记技术介绍的相关文档与必要元数据。
- [x] 2.5 复核公式、术语、Mermaid 与跨文档链接。

## 3. Avatar Forcing 笔记扩写与校验

- [x] 3.1 将 `management/docs/论文笔记/avatar-forcing.md` 首次 DPO 改为带全称的站内链接。
- [x] 3.2 扩写该论文专属的 DPO 内容：两阶段训练与 `v_ref`、偏好判别来源、逐帧向量场比较、`L_ft` 联合目标、配置、消融收益与 CSIM / LSE-C 小幅取舍；通用推导压缩为链接。
- [x] 3.3 更新 Avatar Forcing sidecar 的相关文档信息。
- [x] 3.4 校验 Markdown、JSON、文档列表 / 详情接口与站内链接；确保不将无人工偏好标注误述为无偏好信号，也不将消融结果误述为全指标提升。
- [x] 3.5 运行 `openspec validate --change docs-add-dpo-technical-intro`。
