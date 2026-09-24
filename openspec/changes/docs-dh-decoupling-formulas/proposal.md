## Why

用户在整理汇报稿时指出：`z = z_S + m_S` 只是 **FLOAT 这一支**的"可分解"写法；**LivePortrait/Ditto 那一支的分解落在"关键点变换的次序"上**，而 PerformRecast 的核心改动正是把次序改成与 FLAME 一致。现在两份文档都缺这条对比：

- `数字人概述/数字人身份` 的「动作空间 + 快速渲染器」三支里，第二支（隐式关键点 + warping renderer）只写了 Ditto 的 `x̂ = c_ref·R̂ + δ̂ + t̂`，**没有指出这个"加法"里先后次序的差异及其后果**；
- `数字人概述/数字人动作` 的「动作空间谱系」列了各表示的维度与语义，**没有讲"运动怎么施加到关键点上"（变换次序）这一层**。

缺了这条对比，读者会把"可分解"理解成"分成两项就完了"，而实际上**两项以什么方式组合（加法 / 乘法 / 先加后转）决定了分解是否名存实亡**。

## What Changes

- `数字人身份.md`：在「隐式关键点 + warping renderer」支的 Ditto 段之后，补一段**变换次序对比**（LivePortrait 式 `x = s·(x_c·R + δ) + t` vs PerformRecast 式 `x = s·((x_c + δ)·R) + t`），并与之上的「appearance code + 加法解耦」（`z = z_S + m_S`）形成**两种"可分解"形式的对照**。
- `数字人动作.md`：在「动作空间谱系 / 显式这一族」里补一段**变换次序**（运动如何施加到关键点上），说明它是"能不能只改表情、不动头"的关键。
- 两处均引用 `论文笔记/performrecast`（已完成）与 `论文笔记/liveportrait`、`论文笔记/ditto`，不新造数字。
- 同步把这条对比写进汇报稿 ③ 3.2（属 `docs-intern-report`）。

## Capabilities

### New Capabilities

无。纯文档内容补充。

### Modified Capabilities

无。变更声明 `skip_specs: true`。

## Impact

- 修改：`management/docs/数字人概述/数字人身份.md`、`数字人概述/数字人动作.md`（各补一段 + 一处交叉引用）；`openspec/changes/docs-intern-report/design.md`（③ 3.2 补对比）。
- 依据：`论文笔记/performrecast`、`论文笔记/liveportrait`、`论文笔记/ditto`、`论文笔记/float`。
- 不改代码、API、依赖与既有小节结构。
