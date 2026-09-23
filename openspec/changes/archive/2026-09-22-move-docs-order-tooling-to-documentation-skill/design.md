## Context

`documentation` 是本仓库说明性文档的唯一项目级 skill，已经规定 frontmatter 的 `order` 采用十步空档。现有的 `scripts/docs_order.py` 是依赖 Python 标准库的行级 frontmatter 工具，具备 `list`、`insert`、`--shift` 与 `renumber`，但其路径没有作为文档写作 skill 的资源暴露。详见 proposal.md 的动机。

## Goals / Non-Goals

**Goals:**

- 让文档作者通过读取一个 skill 即可发现排序规则和安全操作工具。
- 保持命令参数、dry-run、重复值拒绝、局部后缀重排和写后校验的已有行为。
- 将 active 文档和运行说明中的调用路径统一到 skill 内工具。

**Non-Goals:**

- 不修改 FastAPI 的排序链或文档内容接口。
- 不引入 YAML 解析器、测试框架或其他第三方依赖。
- 不维护根 `scripts/` 与 skill 目录两份工具副本，也不为旧路径保留包装器。

## Decisions

### 工具作为 skill 的随附脚本

将唯一实现放在 `.agents/skills/documentation/scripts/docs_order.py`。这种目录布局与 skill 的 `references/` 一致，工具、规范和使用说明一起版本化；根目录旧文件移除。

替代方案是在根目录保留实现、skill 只给链接。该做法会继续要求使用者跨目录猜测工具位置，不满足“skill 支持该脚本”的发现需求。

### 显式重排与默认插入分离

默认 `insert` 继续只使用现有整数空位；仅传入 `--shift` 才重排插入点与后缀。这样把“尽量不改既有 order”和“需要连续 10、20、30 的读序”区分为两个可审计操作。`renumber` 仍用于用户明确要求的全目录规范化。

替代方案是每次插入自动全量重排。它会造成不必要 diff，并使已有 order 引用不稳定。

### 文档说明包含可复制的调用

`SKILL.md` 增加排序工具小节，说明脚本路径、dry-run、`--apply`、`--shift` 以及四条可复制命令。本文档的其他 workflow 文本不承担命令手册角色。

## Risks / Trade-offs

- [旧命令路径失效] → active 引用统一迁移，且在 AGENTS.md 与 skill 中给出唯一路径；归档历史不改写。
- [Agent 忽略 dry-run] → 工具继续要求 `--apply`，skill 首先展示预览命令。
- [强制后缀顺延产生较大 diff] → `--shift` 必须显式传入，并在 dry-run 中逐文件列出更新。

## Migration Plan

1. 移动唯一脚本实现到 documentation skill 的 `scripts/`。
2. 将 skill 说明、AGENTS.md、active OpenSpec artifacts 和 active Markdown 中的命令切换为新路径；不修改 archive 内容。
3. 执行语法、临时目录 dry-run/apply、重复值和顺延行为校验，并以新路径列出真实目录顺序。
4. 回滚时将脚本移回 `scripts/` 并恢复所有 active 路径引用；不影响已有 Markdown 的 order 值。