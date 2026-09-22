# Tasks: docs-note-avatar-forcing

## 1. 资料整理（先于动笔，产物需确认）

- [x] 1.1 论文层：从 papers 库取条目信息（标题 / arXiv id / 年份 / 链接），核对机构与一句话定位
- [x] 1.2 论文层：从《Avatar Forcing 模型精读》提取三模块架构链路（驱动信号 → 表示 → 生成 → 渲染）与关键设计取舍
- [x] 1.3 论文层：整理"与同类差异"一表（对比 FLOAT / Ditto / LivePortrait 等：表示、身份处理、生成范式、流式能力）
- [x] 1.4 工程层：接入形态与插件契约（`AvatarPlugin` / `BidirectionalAvatarPlugin`、`SetAvatar` / `GenerateStream`）、流式改造要点
- [x] 1.5 工程层：微调与治理（桥系列、注入点、漂移诊断与四种治理裁决、CSIM 当损失的放弃）——全部结论标注证据强度
- [x] 1.6 汇总上述五项的表格与要点，**在对话中提交审核，不写入仓库**

## 2. 动笔写作（1.x 全部确认后启动）

- [x] 2.1 写 `management/docs/论文笔记/avatar-forcing.md`（模板：是什么 → 架构核心 → 在我们体系中的角色 → 与复盘各线的关联 → 参考与延伸）
- [x] 2.2 自查：模板齐备、数字与结论溯源、无编造、链接有效（指向已存在的文档）；openspec validate 通过并提交
