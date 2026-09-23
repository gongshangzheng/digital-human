## 1. 盘点与判定

- [x] 1.1 生成 `formula-audit.md`，逐项审阅两篇目标文档的公式候选，并标记迁移或字面保留的理由
- [x] 1.2 核对候选中没有把金额、代码围栏、模型名、路径、配置字段和普通数值误列为数学；明确 `management/docs/knowledge/` 不在本次审核范围

## 2. 优先迁移：DPO 与 Avatar Forcing

- [x] 2.1 将 `技术介绍/dpo-直接偏好优化.md` 的通用 DPO、KL、闭式策略、隐式奖励、Bradley–Terry 与 DiffusionDPO 公式迁为 KaTeX，并保留/补齐符号解释
- [x] 2.2 将 `论文笔记/avatar-forcing.md` 的 latent 分解、因果分解、掩码、训练目标、DPO 目标和 offset 关系迁为 KaTeX，并核对其与通用 DPO 文档的职责边界

## 3. 验证

- [x] 3.1 扫描两篇目标文档，确认不再存在不受支持的数学定界符，且迁移文档中的公式与 audit 一致
- [x] 3.2 以 renderer 检查覆盖行内、块级、表格、金额、代码围栏、非法公式和 HTML 安全边界
- [x] 3.3 执行 `npm run build`、`openspec validate migrate-document-formulas-to-katex --strict` 与 `openspec validate --specs --strict`
