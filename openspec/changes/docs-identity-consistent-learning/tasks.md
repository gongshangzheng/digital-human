# Tasks: docs-identity-consistent-learning

> 门禁同 `documentation` skill：探索 → 创建 change + design → **用户审核 design** → 素材 → 正文 → 校验。
> **用户确认 design（含 D1–D8）前不得写入 `management/docs/`。**

## 1. 设计门禁

- [x] 1.1 定位本仓库已有记载：`数字人领域问题` §一 四节 + §五 三节 + §四 路线五 + §六
- [x] 1.2 确认与 `docs-motion-space-modeling` 的边界问题（`### 说话风格` 明确"两者容易纠缠"）
- [x] 1.3 创建 change `docs-identity-consistent-learning`，`.openspec.yaml` 置 `skip_specs: true`
- [x] 1.4 写 `proposal.md` / `design.md`（新命题、落点候选、调研范围 R1–R4、四个边界问题、待调研 8 项、D1–D8、DC1–DC7、Risks）
- [x] 1.6 **共享上游命题落地**：与 `docs-motion-space-modeling` 共同持有「身份 = 轨迹里不变的部分 / 风格 = 轨迹里变化的部分」（DC12–DC15）；本 change 只负责【不变分量】；**双向必须同步**
- [ ] 1.7 **用户审核 design 与 D1–D8 裁决**

## 2. 素材与调研（设计通过后）

- [x] 2.0 **第一份调研产出**：`research/identity-consistent-learning.md`（单帧之谜 + 多帧/视频尝试 + 两个核心判断 + 6 项待核实）——⚠ 网络故障下产出，已标证据等级
- [ ] 2.1 盘点本仓库第一手素材（`数字人身份` 漂移证据、`digital-human-identity-consistency` 裂缝分析、`face-verification-models`）
- [ ] 2.2 **R1 多参考聚合**：检索 2024–2026 路线（聚合顺序 / 冲突处理 / 无位姿 / 参考数变化鲁棒性）
- [ ] 2.3 **R2 跨视角一致**：核实"跨机位一致性协议"是否仍空白；现有度量为何测不了外观连续性
- [ ] 2.4 **R3 跨动态一致**：条件 / 资产 / 约束三条路线的实测差异
- [ ] 2.5 **R4 度量现状**：三通道判别器（身份 / 质量 / 时序漂移）是否已有实现；跨编码器方差与反循环性检查
- [ ] 2.6 **边界问题①②③④** 逐个给出可操作答案（尤其"身份 vs 风格可分性判据"）
- [ ] 2.7 待 VPN 恢复后补 §5 的 6 项核实（含 `BlendFace` 原文、VFR 聚合近年进展、**身份/运动分离判据**），并升级该调研文件（按 `docs-motion-space-modeling` 的写法：覆盖局限 + 结论速览 + 直接邻居 + 待补）
- [ ] 2.8 与用户确认素材口径：哪些升为结论、哪些保留为推断

## 3. 落点与结构（按 D1/D2/D3 裁决）

- [ ] 3.1 若建 `management/docs/身份建模/`：登记 `DOCS_FOLDER_ORDER` + 写 README（最小 frontmatter + 与 `动作空间建模/` 的边界）
- [ ] 3.2 定文章清单与契约（建议不超 5 篇，沿用大块切分）
- [ ] 3.3 `docs_order.py list` 复看 `order` 无缺失/重复

## 4. 校验与提交

- [ ] 4.1 与 `数字人身份` / `digital-human-identity-consistency` **不重复**（DC2）
- [ ] 4.2 与 `docs-motion-space-modeling` **互引 + 边界说清**（DC1/DC4）
- [ ] 4.3 外部工作标"已核实 / 未核实"；禁止穷尽性断言（DC3）
- [ ] 4.4 任何一致性宣称带**随机基线 + 真实上界**（DC6）
- [ ] 4.5 `openspec validate docs-identity-consistent-learning --strict`
- [ ] 4.6 聚焦提交
