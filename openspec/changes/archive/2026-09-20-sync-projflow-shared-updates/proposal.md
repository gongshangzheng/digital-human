# Proposal: sync-projflow-shared-updates（同步上游 ProjFlow 的 [shared] 特性 + 修复中文 slug）

## Why

本仓库脚手架拷贝点**早于**上游 ProjFlow 若干 `[shared]` 提交，导致：
1. **Bug**：文档详情接口的 slug 正则只允许 `[a-zA-Z0-9_/-]`，**中文文件名文档打不开**（`GET /api/management/docs/knowledge/数字人基础` → 400 Invalid slug）。上游同样存在此 bug，属待回灌项。
2. 上游已有但我们缺失的共享特性：菜单隐藏配置（HIDDEN_KEYS）、文档页 sidecar json 元数据、TOC 符号处理、文档页侧栏收起、文档侧栏子目录折叠等。我们目前用自己手写的 `web/src/config/menu.js` 代替了上游的 `hidden.js`，机制重复。

## What Changes

- **修复中文 slug**：`_SLUG_RE` 支持 Unicode（中文、空格等），并正确解码 URL；标 `[shared]` 作为回灌上游候选。
- **同步上游 [shared] 特性**（逐文件对照移植，非 git cherry-pick——我们已改名/改端口/改菜单逻辑，直接 cherry-pick 会冲突）：
  - `ff49e31` 引入 `web/src/config/hidden.js`（HIDDEN_KEYS，含分组级隐藏），MainLayout 按其过滤；**退役我们的 `menu.js`**，把隐藏集合迁入 hidden.js；ReportPage 报告类型隐藏一并取
  - `bd91ac2` sidecar json：`server/routers/management.py` 读取 `<slug>.json` 并在详情返回 `sidecar`；`web/src/utils/markdown.js` TOC 去 `**`；`DocPage.vue` sidecar 区块（演进记录/进度/相关文档/附录）
  - `aacb342` DocPage 左右侧栏收起至边缘
  - `8db8272` 文档侧栏子目录折叠展开
  - `fe60681`/`690be30` 文档约定（docs/ 与 notes/ 区分、documentation skill 双层流程）按需取
- **保留我们的既有定制**：端口 8812/3212、digital-human 身份改名、localStorage 键改名、`实习复盘/` 与 `论文笔记/` 目录约定。

## Capabilities

### New Capabilities
- `docs-page`: 文档页行为（中文 slug 可访问、sidecar 元数据渲染、侧栏收起、子目录折叠、TOC 符号处理）
- `menu-visibility`: 菜单/报告类型隐藏的配置化机制（HIDDEN_KEYS 唯一控制点）

### Modified Capabilities
（无——本仓库尚无 specs/）

## Impact
- 代码：`server/routers/management.py`、`web/src/config/hidden.js`（新增）、`web/src/layouts/MainLayout.vue`、`web/src/utils/markdown.js`、`web/src/views/management/DocPage.vue`、`web/src/views/management/ReportPage.vue`、`web/src/views/Home.vue`；删除 `web/src/config/menu.js`
- 文档：可选为现有 docs 增加 sidecar json（本期只落机制，内容按需）
- 上游：中文 slug 修复与 hidden.js 相关经验按 upstream-sync `[shared]` 回灌 ProjFlow（本 change 记录待办）
- 不影响：papers / evaluation / 端口 / 目录结构
