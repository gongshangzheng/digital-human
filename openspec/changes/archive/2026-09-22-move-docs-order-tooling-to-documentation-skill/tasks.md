## 1. 工具归属

- [x] 1.1 将唯一的 `docs_order.py` 实现迁入 `.agents/skills/documentation/scripts/`，删除根 `scripts/` 旧副本
- [x] 1.2 保持 `list`、`insert`、`--shift`、`renumber`、dry-run、`--apply`、重复 order 检测和写后校验的既有行为

## 2. Skill 与调用迁移

- [x] 2.1 在 `documentation/SKILL.md` 记录工具路径、排序规则、默认安全行为和可复制命令
- [x] 2.2 更新 active 的仓库说明、OpenSpec artifacts 与 Markdown 中的脚本路径；不改写 archive 历史

## 3. 验证

- [x] 3.1 用新路径执行 `py_compile`、真实目录 `list`，以及临时目录的 insert dry-run/apply、`--shift` 后缀顺延、`renumber` 和重复值拒绝检查
- [x] 3.2 执行 `openspec validate move-docs-order-tooling-to-documentation-skill --strict` 与 `openspec validate --specs --strict`
