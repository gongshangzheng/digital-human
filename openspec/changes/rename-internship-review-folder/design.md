## Context

- 目标目录：`management/docs/实习复盘/`，8 篇：`数字人介绍与技术路线.md`、`数字人身份.md`、`数字人动作.md`、`CyberVerse框架.md`、`工程设计.md`、`数字人加速.md`、`数字人行业全景.md`、`总结.md`。
- 该目录是文档列表的第一分组，顺序由 `server/config.py` 的 `DOCS_FOLDER_ORDER`（值为 `['实习复盘', '论文笔记', 'knowledge']`）决定，不是文件系统顺序。
- 文档正文用 wiki 链接 `[[实习复盘/<slug>|<label>]]` 交叉引用，MarkdownRenderer 会把 `[[slug]]` 转成 `/management/docs/<slug>` 路由。
- 主 specs 有两处把 `实习复盘` 当示例/默认值写进了契约文本（`docs-page-content`、`docs-page-layout`）。
- `openspec/changes/archive/**` 与已完成 change 里也有大量 `实习复盘` 字样，属**历史记录**。

## Goals / Non-Goals

**Goals：**

- 目录名与内容定位一致（长期概述性文档，不绑「实习」身份）。
- 重命名后文档列表分组名、顺序、站内链接全部正确，且 specs 不再残留旧目录名。
- 可回滚，且不篡改历史记录。

**Non-Goals：**

- 不改任何文档的**文件名**与**正文内容**（除链接命名空间）。
- 不改写 `openspec/changes/archive/**` 与已完成 change 的历史表述。
- 不新增 `/management/docs/实习复盘/...` → 新路径的重定向（旧链接 404 属预期）。
- 不改前端代码（分组名与顺序都由后端数据驱动）。

## Decisions

### D1：用 `git mv` 重命名目录，不用「新建目录 + 逐个复制」

保留文件与目录的 Git 历史；重命名在 diff 中表现为 rename，便于复核。

- 备选：`cp -r` + `rm -rf` —— 丢失历史且 diff 噪音大，不采用。

### D2：`DOCS_FOLDER_ORDER` 只替换首项，位置不变

`['数字人概述', '论文笔记', 'knowledge']`。顺序决策（概述在前）不变，本次只改名字，避免把「重命名」和「调顺序」两件事混在一个 change 里。

- 备选：顺便调整分组顺序 —— 需单独的理由与验收，另开 change。

### D3：只改「在用」引用，不动历史 change

判定标准：会**影响当前渲染或当前执行**的才改。

| 类别 | 处置 |
|---|---|
| 目录内交叉链接、论文笔记、article-note skill 示例、`server/config.py` | 改 |
| 主 specs 的示例与默认值 | 改（走 delta → 归档时同步） |
| `openspec/changes/archive/**`、已完成 change | 不改（历史事实） |
| 活跃 change 的已勾选任务 | 不改（记录当时事实）；经核对无未完成任务引用该路径 |

- 理由：change 记录是「当时做了什么」的证据链，事后改写会让历史与当时的仓库状态不符。

### D4：不加重定向

旧 slug `/management/docs/实习复盘/数字人介绍与技术路线` 重命名后 404。

- 理由：这是单人研发库的内部文档系统，没有外部深链；为旧路径长期保留重定向会引入一张需要维护的别名表，收益远低于成本。
- 若未来确需，可单独加「文档别名」能力（另开 change）。

### D5：`数字人概述` 与个别文件的定位偏差，记录但不阻塞

该目录含深挖篇（身份/动作/加速/工程设计）而不只是「概述」。`概述` 更贴近 `数字人介绍与技术路线` 与 `总结`。本次按用户指定执行；若后续觉得名字与实际不符，再单独改名。

## Risks / Trade-offs

- [旧链接 404] → 已声明为预期；仓库内所有在用 `[[...]]` 链接在同一次提交内全部改完，并由内链校验兜底。
- [漏改造成站内死链] → 缓解：改完后全仓 `rg "实习复盘"` 只应命中 `openspec/changes/**`（历史），并用 article-note 的 `validate-note.py` 校验论文笔记内链、浏览器抽查文档页。
- [spec 与实现再次脱节] → 缓解：本次把 specs 里的示例/默认值同步进 delta，归档时写入主 specs。
- [文档列表分组名变化影响使用者习惯] → 一次性变化，分组仍在第一位置。

## Migration Plan

1. `git mv management/docs/实习复盘 management/docs/数字人概述`
2. 改 `server/config.py` 的 `DOCS_FOLDER_ORDER`
3. 改目录内 6 篇的交叉链接；改 `论文笔记/` 3 个文件；改 `article-note` 2 个示例
4. 起后端，验证 `GET /api/management/docs` 顺序为 数字人概述 → 论文笔记 → knowledge，且新路径可访问、旧路径 404
5. 浏览器抽查文档页与分组折叠
6. 归档时同步两个 delta 进主 specs

回滚：反向 `git mv` + 恢复 `DOCS_FOLDER_ORDER` + 反向替换链接即可；无数据迁移。

## Open Questions

- 目录内的深挖篇（身份/动作/加速/工程设计）未来是否拆到别的分组？（不影响本变更的 specs、方案与任务拆分。）
