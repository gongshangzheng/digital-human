## 1. skill 改写（.agents/skills/documentation/SKILL.md）

- [x] 1.1 §2 按 design D1 把四行排序键规则替换为按文件夹类型区分（第一方强制 `order`／外部复制件不强制、不回填来源缺失字段／README 一视同仁／排序链）
- [x] 1.2 §6 按 design D2 把顺序校验限定为「第一方」目录
- [x] 1.3 通读 §2、§3、§6，确认没有残留「每个内容文件夹都必须有显式排序键」这类绝对措辞

## 2. 内容侧复核（不改文档）

- [x] 2.1 复核三个第一方文件夹（`数字人概述/`、`论文笔记/`、`技术介绍/`）的 `order` 完整、无重复
- [x] 2.2 确认 `knowledge/` 未被改动（`git diff` 不含该目录）

## 3. 校验与提交

- [x] 3.1 重跑 `docs_order.py list` 于三个第一方目录，输出与既有阅读顺序一致
- [x] 3.2 `openspec validate docs-skill-order-scope --strict` 通过
- [x] 3.3 提交（`docs(skill): 排序键规则限定第一方文件夹，knowledge 复制件豁免`），只包含 skill 与 openspec 相关文件
- [x] 3.4 归档：sync 本 change 的 delta 到主 spec 后移入 `openspec/changes/archive/`
