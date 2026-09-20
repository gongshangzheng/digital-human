# Design: docs-intern-identity

## Context

- 伞 change：`internship-work-review-docs`（登记表 #1，结构契约六节：问题/定位方法/模长实验/夹角实验/治理方案/汇报要点与后续推进）。
- 目标读者与用途：自己；工作汇报 + 后续推进素材 + 发文候选 A 证据源。
- 双层流程（D0）：先「资料整理」并在对话中提交证据与口径供确认，通过后才进入「动笔写作」（素材不落仓库）。

## Goals / Non-Goals

**Goals:**
- 整理产物：全部实验数据表（原始数字）、术语与变量定义（z_S/r_d/模长/方向）、证据强度说明
- 正文：按结构契约六节成文，每个数字可溯源到整理产物

**Non-Goals:**
- 不写音频微调（蒸馏桥/geom/georkd 属于音唇同步线，另篇或扩展）
- 不下"漂移成因已定论"的结论（夹角仅单身份支持）

## 整理清单（动笔前必须完成）

| 来源 | 提取物 |
|------|--------|
| knowledge/《Avatar Forcing 微调实践》§三 | 模长实验三段测量表（GT/noguide/A1 × 首/中/末 + 斜率）、夹角实验数据、参考条件化 v2 描述与状态 |
| knowledge/《Avatar Forcing 模型精读》 | z_S/r_d 变量定义、FLOAT 显式分解、blockwise 流式与漂移的关系 |
| knowledge/《Avatar Forcing Motion Latent AutoEncoder》 | motion latent 空间性质（模长/方向的几何含义是否有原文支撑） |
| 博客复制 digital-human-identity-consistency.md | 博客侧重述的身份一致性内容（与 InternWiki 版对勘，取更准确版本） |
| CyberVerse @4968280 `models/avatarforcing/` | 相关注释/常量（如 flow suppression 与身份保持的关系，仅作代码证据） |
| 微调类身份提升尝试（ArcFace / ID loss） | 回捞实验记录（口述线索：用 ArcFace 系特征/loss 提升身份）；**知识库现无记录，须先找证据，找不到则标"口述待补"** |
| knowledge/《微调策略专题》《digital-human-identity-consistency》 | 身份相关微调结论与度量口径（CSIM/ArcFace 的适用边界） |

## Decisions

- **D1 素材不落仓库**：资料整理结果只在对话中提交审核，不写入仓库；仓库只保留正文
- **D2 数字以 InternWiki 表格为准**：两源冲突时以更接近实验记录的版本为准，冲突记录进整理产物的"对勘"节

## Risks / Trade-offs

- [夹角实验仅单身份，正文若写成普适结论会过头] → 整理产物显式列"适用边界"栏，正文措辞与边界对齐

## Open Questions

（整理时若发现参考条件化 v2 已有新进展记录，回填状态即可，不阻塞）
