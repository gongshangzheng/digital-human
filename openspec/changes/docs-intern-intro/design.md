# Design: docs-intern-intro

## Context

- 伞 change：`internship-work-review-docs`（登记表 #1，结构契约见其 design）。
- 统一写作骨架（D1）：为什么重要 → 现行做法 → 我们的工作/选择 → 改进方向。
- 本文定位：**数字人领域入门与路线总览**（教科书视角）；与《数字人行业全景》分工——后者写产业/产品/我们实测，本文写原理与流派，相互引用不重复展开。

## Goals / Non-Goals

**Goals:**
- 整理产物：三路线各代表模型清单（挂 papers 库 slug）、优缺点对比表、NeRF→3DGS 成本演进表、术语表、事实分级
- 正文：可支撑其余各篇引用的路线总览

**Non-Goals:**
- 不写我们的工程/实验细节（链各专题）
- 不重复《数字人行业全景》的竞品与实测横评

## 整理清单（动笔前必须完成）

| 来源 | 提取物 |
|------|--------|
| knowledge/《数字人基础》 | 两层划分（数字人 vs 系统）、三轴/两轴分析框架、生成方式三分类表、NeRF→3DGS 演进表、级联/端到端/混合架构、评价口径 |
| knowledge/《5分钟认识数字人》 | 一句话定义、三条轴的用户友好讲法、常见误解 |
| knowledge/《3dgs-methods-research》 | FlexAvatar/HyperGaussians/MATCH/AniGS 的方法与 VFHQ-Test 指标表、A10 可行性结论 |
| knowledge/ 三篇 survey（survey-map / avatar-survey / realtime-survey） | 综述分类体系差异、领域级挑战（唇+头+手势统一框架缺位、扩散实时化困难）、模型线索 |
| papers 库（data/papers.db） | 按六类抽代表模型清单（2d-talking-head 30 / 3d-avatar 21 / audio-driven-animation 14），每模型带 slug 与一句话 |
| project-README 时间线 | 选型结论（GAGAvatar/UIKA 前馈式路线）与依据 |

## Decisions

- **D1 路线框架的对勘**：用户给出"三条路线"（视频基座 / 动作空间扩散 / 3D GS）；knowledge《数字人基础》强调"两条轴"（生成方式 × 渲染后端）且指出动作空间模型可配 2D 或 3DGS。整理产物必须把这个张力摆出来，正文采用哪种框架由用户定（建议：以三路线为主叙述、用两条轴说明其非互斥性）
- **D2 整理产物放 change 目录**：`整理-数字人介绍与技术路线.md`，正文写完后作为证据附件保留

## Risks / Trade-offs

- [三路线叙述被误读为互斥] → 正文显式说明"生成方式与渲染后端可自由组合"
- [路线优缺点缺一手证据] → 优缺点优先引 knowledge 表格与 papers 库指标，缺的标"待补"

## Open Questions

（路线框架最终取舍待用户确认，见 D1）
