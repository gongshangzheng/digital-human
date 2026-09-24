## 1. 核对

- [x] 1.1 读 `论文笔记/performrecast` 的式 1–3（LivePortrait 式与 PerformRecast 式的并列写法）与结论（先加后转 ⇒ 继承 3DMM 解耦）。
- [x] 1.2 读 `数字人身份.md` 三支与 `数字人动作.md` 动作空间谱系，确认落点与既有内容边界。
- [x] 1.3 确认 `z = z_S + m_S` 属 FLOAT/AF 支（`数字人身份.md` 既有段落）。

## 2. 补写

- [x] 2.1 `数字人身份.md`：「隐式关键点 + warping renderer」支的 Ditto 段之后补一段**变换次序对比**（两式并列 + 与加法解耦的两种形式对照 + 结论）。
- [x] 2.2 `数字人动作.md`：「显式这一族要多说几句」之后补一段**运动的施加次序**（先加表情再旋头姿 vs 先旋再加），点明它是"只改表情不动头"的关键。
- [x] 2.3 `docs-intern-report/design.md` ③ 3.2 补三式对照表（隐空间加法 / 关键点变换 / 改次序）。

## 3. 验证

- [x] 3.1 公式用 `$$...$$`；符号表或中文解释齐备；表格列数一致。
- [x] 3.2 站内链接目标存在（`论文笔记/performrecast`、`论文笔记/liveportrait`、`论文笔记/ditto`、`论文笔记/float`）。
- [x] 3.3 `openspec validate docs-dh-decoupling-formulas --strict`；FastAPI 详情接口确认两篇文档可读。
- [x] 3.4 提交 `docs(dh): 补"可分解"的第二种形式（关键点变换次序）并交叉引用`。
