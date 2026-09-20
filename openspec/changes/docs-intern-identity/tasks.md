# Tasks: docs-intern-identity

## 1. 资料整理（先于动笔，产物需确认）

- [x] 1.1 研读《Avatar Forcing 微调实践》§三/§四/§五，抄录模长表、夹角表、A1 结果与 v1/v2/LAF 三条裁决
- [x] 1.2 研读《Avatar Forcing 模型精读》+《Motion Latent AutoEncoder》，提取 z_S/r_d/模长/方向的定义链与原文措辞
- [x] 1.3 对勘身份一致性文档版本 → **修正前提：该文档只有博客版（InternWiki 无此篇）；知识库副本即博客原文的 html2text 转换，关键句逐条比对一致，无版本冲突**（副本内 mermaid 为 Hugo shortcode 形式）
- [x] 1.4 查 CyberVerse @4968280 models/avatarforcing/ 相关代码证据（flow suppression ratio=0.7、anchor_guide、身份编码 s_r / 方向基准 r_s），列路径
- [x] 1.4b 回捞"用 ArcFace/ID loss 提升身份"的微调实验记录 → **已核查：知识库 / 博客 / CyberVerse 代码三处均无记录，记为"口述待补"，不编造数字**
- [x] 1.5 汇总数据表 + 术语表 + 证据强度说明 + 适用边界 + 待补数字清单，**已在对话中提交审核（不写入仓库）**

## 2. 动笔写作（1.x 全部确认后启动）

- [ ] 2.1 写 `management/docs/实习复盘/数字人身份.md` 正文（7 节：为什么重要 / 身份表示与渲染后端 / 身份注入与保持 / 一致性度量 / Avatar Forcing 上的身份改进〔5 子节〕/ 可能的改进方向 / 汇报要点），数字全部溯源整理产物
- [ ] 2.2 自查：结构契约对齐、无编造数字、无越界结论；openspec validate 通过并提交
