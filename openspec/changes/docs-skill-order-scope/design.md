## Context

`docs-skill-order-convention`（已归档）把「每个内容文件夹都必须有显式排序键」写进 `documentation` skill 与主 spec。实施后核对存量发现该规则在 `knowledge/` 不成立：52 篇无 `order`、30 篇无 `id`，且 51 篇缺 `author`、24 篇缺 `summary`（来源侧本就没有）。第一方三个文件夹（9 + 3 + 2 篇）则完全合规。用户口径已定：`knowledge/` 不需要，第一方需要。

## Goals / Non-Goals

**Goals：**

- 把 skill 的规则改写为「第一方内容文件夹强制 `order`／外部复制件文件夹不强制」，并写明豁免范围与不要求回填来源缺失字段。
- 修订主 spec 中对应 requirement 的作用域，并补一条豁免场景。

**Non-Goals：**

- 不给 `knowledge/` 补 `id`、`order`、`author` 或 `summary`；不改动其中任何文档（`knowledge/README.md` 的 frontmatter 已在上一处修好）。
- 不改后端排序实现、前端、`docs-page-content` 契约（其「未写 order 时按 id 排序」场景与新口径一致）。
- 不引入「按文件夹类型配置」的新机制，只在 skill 文字上区分类型。

## Decisions

### D1：skill §2 改为按文件夹类型区分

替换现在的四行（排序键按文件夹选择／每个内容文件夹都必须有显式排序键／索引 README／排序链）为：

```markdown
- frontmatter 必填 `title`、`author`、`date`、`tags`、`summary`；排序键按文件夹类型选择：
  - **第一方内容文件夹**（`数字人概述/`、`论文笔记/`、`技术介绍/` 及以后新建的第一方主题目录）用 `order`（数字，10 为步长，如 `10, 20, 30`）表达阅读顺序；插入新篇优先占用相邻空位，不为插入一篇而重排既有文档。
  - **外部复制件文件夹**（`knowledge/` 这类从博客/InternWiki 复制的素材）不强制排序键，沿用来源元数据即可；也不要为它回填来源侧本就没有的作者或摘要。
- 第一方文件夹必须每篇都有 `order`：未写 `order` 的文档会落到该目录内的 `date` 降序（越新越靠前），所以新建文档不得依赖日期隐式决定阅读顺序。
- 文件夹索引 `README.md`（第一方或复制件都一样）也要带最小 frontmatter（`title`/`author`/`date`/`tags`/`summary`）；否则顺序工具在该目录直接报错，且列表标题会退化成裸 slug。
- 排序链为文件夹优先级 → `order` → `id` → `date` 降序 → slug。
```

备选方案是不改 skill、只在主 spec 里加备注。否决原因是 agent 读的是 skill，规则留在 spec 里等于不生效；且上一版的绝对措辞会让 agent 试图给 `knowledge/` 回填作者。

### D2：skill §6 交付检查限定第一方

「同目录 `order` 无缺失、无重复且与既定阅读顺序一致」改为「**第一方**目录 `order` 无缺失、无重复且与既定阅读顺序一致」。

### D3：主 spec 用 MODIFIED 覆盖已同步的 requirement

`openspec/specs/repository-agent-skills/spec.md` 里的 `Documentation skill states explicit ordering conventions per folder` 由「每个含说明性文档的文件夹」改为「第一方强制／复制件豁免」，保留原有 4 个场景并更新措辞（「Agent 新建一篇文档」→「Agent 在第一方文件夹新建一篇文档」、「目录缺少显式排序键」→「第一方目录缺少显式排序键」、「交付前的顺序校验」加「第一方」限定），新增「外部复制件文件夹豁免排序键」场景，共 5 个场景。

**不删除任何既有场景**：MODIFIED 的 delta 必须携带保留下来的全部场景，否则校验会失败。

## Risks / Trade-offs

- [豁免写得太宽，以后新建的复制件文件夹也被默认放过] → D1 明确列举「`knowledge/` 这类从博客/InternWiki 复制的素材」，并要求第一方**主题目录**一律强制。
- [豁免被误读成「复制件 README 也不用 frontmatter」] → D1 第 3 条明确 README 要求对两类文件夹一视同仁（`knowledge/README.md` 已在上一提交补齐）。
- [`knowledge/` 30 篇无 id 的排序看起来像缺陷] → 保持现状是本次决定的一部分；`docs-page-content` 的排序链仍保证顺序确定（id → date 降序 → slug），不需要额外机制。

## 待确认项

1. 「第一方」的判定口径按**目录列举 + 未来新建主题目录**理解；若你希望改成别的判据（例如「作者为本仓库成员的文档」），说一声我改 D1。
2. 是否顺手把 `项目` 里其余含 README 的文件夹（目前只有 `论文笔记/` 与 `knowledge/`，都已有 frontmatter）纳入同一检查，我默认不做额外动作。
