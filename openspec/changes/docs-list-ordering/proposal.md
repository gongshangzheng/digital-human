# Proposal: docs-list-ordering（文档列表可显式排序）

## Why

文档页左侧列表的排序链是「`date` 降序 → `id` 升序」，存在两个问题：

1. **`id` 兼作"文档编号"与"排序键"**：知识库 22 篇外部复制件已占用 `1..22`，我们自己的文档要么跟它们抢编号，要么没有 `id`。
2. **没有 `id` 时排序链断裂**：两篇同 `date` 且都无 `id` 的文档（如 `实习复盘/数字人介绍与技术路线` 与 `实习复盘/CyberVerse框架`）最终落到 `os.walk` 的**文件系统遍历顺序**——APFS 不保证有序，导致先后随机、换机器可能变化。当前列表里 CyberVerse 反而排在入门篇前面就是这个原因。
3. **文件夹顺序也不可控**：树形结构按"首次出现顺序"生成，文件夹先后被文档排序间接决定，无法表达「实习复盘 → 论文笔记 → knowledge」这样的阅读顺序。

## What Changes

- 新增 **`order`** frontmatter 字段（数字，越小越前），与 `id` 解耦：`order` 表达**阅读顺序**，`id` 保留**文档编号**语义
- 文档列表排序链改为：**文件夹优先级 → `order` → `id` → `date` 降序**；三者都缺时保持现状（不与现有行为冲突）
- 文件夹优先级用服务端常量列表表达（默认 `实习复盘 → 论文笔记 → knowledge`，未列出的排在已知之后）
- 给现有 `实习复盘/` 文档补 `order`，使列表按登记表顺序显示（入门篇在最前）
- 该改动是脚手架共享能力，标为 `[shared]` 回灌候选

## Capabilities

### Modified Capabilities
- `docs-page-content`：新增「文档列表可显式排序」要求（`order` 字段与排序链、文件夹优先级、缺省兼容）

## Impact

- 代码：`server/routers/management.py`（`get_docs` 排序 + 文件夹优先级常量）；前端无需改动（列表顺序驱动树构建）
- 文档：`management/docs/实习复盘/*.md` 补 `order`；`doc-writing` skill 的 frontmatter 表更新
- 上游：标 `[shared]` 回灌 ProjFlow（该排序逻辑为脚手架共享部分）
- 兼容性：现有 `id` 排序行为在未写 `order` 时保持不变；知识库文档不受影响
