## 1. 口径定义

- [x] 1.1 定义三句话口径（现象在运动输出 / CSIM 是读数 / 归属未分离）。
- [x] 1.2 确认锚点 slug 仅在本文件内被引用（仓库其他位置无引用）。

## 2. 第一方文档修正

- [x] 2.1 `论文笔记/avatar-forcing.md`：小节标题改"长时运动漂移…"，同步 3 处内部锚点。
- [x] 2.2 `论文笔记/avatar-forcing.md`：正文凡把该现象写成"身份漂移"处改为"运动输出漂移"，首段补"分量归属未分离"。
- [x] 2.3 `论文笔记/avatar-forcing.md`：「推理与系统链路」末尾"身份漂移的入口"→"运动漂移的入口"。
- [x] 2.4 `论文笔记/avatar-forcing.json`：changelog 追加更正条目。
- [x] 2.5 `数字人概述/数字人身份.md`：章首加口径声明（漂移在运动隐变量上；CSIM 是读数；归属未分离）。
- [x] 2.6 `数字人概述/总结.md`：候选 A 改名"运动漂移的诊断与治理" + 主张句加限定。
- [x] 2.7 `数字人概述/数字人关键技术地图.md`：在长时漂移条目里加"分量分离"区分句（条目名不改）。
- [x] 2.8 `knowledge/Avatar Forcing 微调实践.md`：§三加一行 scope note（外部快照正文不动）。

## 3. 待用户确认的同步

- [x] 3.1 `docs-motion-space-modeling/design.md:75` 措辞（并行会话）。
- [x] 3.2 `docs-identity-consistent-learning/design.md:51` 措辞（并行会话）。
- [x] 3.3 `docs-intern-report/design.md` ③ 3.3 统一用词（本仓库）。

## 4. 验证

- [x] 4.1 锚点自检：旧 slug 残留 0；新 slug 的 3 处引用一致。
- [x] 4.2 站内链接目标存在；表格列数一致；`$` 无奇数行。
- [x] 4.3 `openspec validate docs-avatar-forcing-motion-drift --strict`；API 抽查两篇文档。
- [x] 4.4 提交 `docs(avatar-forcing): 口径修正为"运动输出漂移"（非身份漂移）`。
