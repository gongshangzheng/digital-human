## Why

用户指出：我们把 Avatar Forcing 的实测现象写成了**"身份漂移"**，但**实测漂的是运动输出**——逐帧运动隐变量 `r_d` 的**方向**以 +2.1°/min 持续偏移（模长几乎不变）。而"身份"那一侧的读数（CSIM 0.645 → 锚点引导后 0.935）是**度量读数**，其分量归属（是外观/身份真变了，还是姿态/视角偏移让度量掉分）**尚未分离**。

这个口径错误已经扩散到多份文档与小节标题里（含 `### 长时身份漂移：…`），会让读者把这套工作读成"身份侧方法"，也会误导出"解耦不彻底"的因果结论。

## What Changes

- **口径统一为三句话**：
  1. 实测现象：Avatar Forcing 在**长程生成 / 静音条件**下，**运动输出**出现漂移（运动隐变量方向持续偏移）；
  2. 度量读数：同期输出帧的身份度量 CSIM 下降；推理期锚点引导（**约束运动方向**）把它拉回；
  3. 未分离：CSIM 下降**是否等于外观/身份变化**尚未验证（现有度量对姿态敏感）——因此**不写成"身份漂移"**。
- 逐文件修正**第一方文档**（见 design 清单）：`论文笔记/avatar-forcing.md`（含小节标题与 3 处内部锚点）、`数字人概述/数字人身份.md`（加口径声明）、`数字人概述/总结.md`（候选 A 改名）、`数字人概述/数字人关键技术地图.md`（加区分句）。
- 为**外部知识快照**加一行 scope note（`knowledge/Avatar Forcing 微调实践.md`），不改其正文。
- **不改**：所有 `archive/**`（历史记录）；`liveact.md` 与 `omnimate.md` 里的"身份漂移"是**各自论文自己的术语**，不是我们对 AF 的描述。

## Capabilities

### New Capabilities

无。纯文档口径修正。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 修改：`论文笔记/avatar-forcing.md` + sidecar、`数字人概述/数字人身份.md`、`数字人概述/总结.md`、`数字人概述/数字人关键技术地图.md`、`knowledge/Avatar Forcing 微调实践.md`（加 scope note）。
- 同步（待用户同意）：`docs-motion-space-modeling/design.md`、`docs-identity-consistent-learning/design.md`、`docs-intern-report/design.md` 里的同一表述。
- 不改代码、API、依赖与归档 change。
