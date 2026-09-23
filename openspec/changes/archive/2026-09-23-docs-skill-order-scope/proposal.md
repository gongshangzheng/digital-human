## Why

上一版规则要求「`management/docs/` 下每个含说明性文档的文件夹都必须有显式排序键」，但存量事实是：第一方文件夹（`数字人概述/` 9 篇、`论文笔记/` 3 篇、`技术介绍/` 2 篇）全部合规，而 `knowledge/` 的 52 篇**没有一篇有 `order`，其中 30 篇连 `id` 都没有**，另有 51 篇缺 `author`、24 篇缺 `summary`、3 篇缺 `date`——这些字段在来源侧本来就没有，回填等于编造作者与摘要。

用户口径已定：**`knowledge/` 不需要显式排序键，其他（第一方）文件夹需要**。本 change 把这条口径写进 `documentation` skill，并修订主 spec 中对应的 requirement，使规则与存量现实一致。

## What Changes

- `.agents/skills/documentation/SKILL.md`：
  - §2 把「每个内容文件夹」改为**按文件夹类型区分**：第一方内容文件夹（`数字人概述/`、`论文笔记/`、`技术介绍/` 及以后新建的第一方主题目录）必须用 `order`；外部复制件文件夹（`knowledge/` 这类从博客/InternWiki 复制的素材）不强制排序键，沿用来源元数据即可，但其索引 README 仍应带最小 frontmatter。
  - §6 交付检查里的顺序校验限定为「**第一方**目录的 `order` 无缺失、无重复」。
- 修订主 spec `repository-agent-skills` 里已同步的 requirement `Documentation skill states explicit ordering conventions per folder`：把「每个文件夹」改为第一方强制／复制件豁免，并新增一个「外部复制件文件夹」场景。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `repository-agent-skills`: 修改 requirement `Documentation skill states explicit ordering conventions per folder` 的作用域——由「每个含说明性文档的文件夹」改为「第一方内容文件夹强制、外部复制件不强制」，并补一条豁免场景。

## Impact

- 修改 `.agents/skills/documentation/SKILL.md`（§2、§6）。
- 同步后再修改 `openspec/specs/repository-agent-skills/spec.md`（该 requirement 的正文与场景）。
- 不改任何 `management/docs/` 文档：本次不补 `id`、不补作者/摘要，`knowledge/` 维持现状。
- 不改后端排序实现与 `docs-page-content` 契约；该 spec 里「未写 order 时按 id 排序、知识库 22 篇顺序不变」的场景与新口径一致，无需改动。
