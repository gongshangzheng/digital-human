## Why

给 `face-vid2vid` 补架构图时，我们真实犯过两类错并**全部漏过校验**：

1. **正文里把行内公式写成了块级定界符**（`$$f_s$$`）。`$$` 在渲染器里是块级公式，于是"行内引用"在页面上变成整行居中的大公式——读者一眼就能看出错，但校验器一声不响。
2. **写了双反斜杠命令**（`\\delta`、`\\Delta`、`\\times`）。KaTeX 里 `\\` 是换行符，结果 δ 渲染成字面 "delta"。

现有 `validate-note.py` 只覆盖 `\(...\)`、`\[...\]`、`\begin{equation}` 三种"不受支持定界符"，对上面两类**零覆盖**；而这两类不是风格偏好，是**当前渲染器下的确定错误**——只要有检查就一定能抓到。

## What Changes

- 在 `.agents/skills/article-note/scripts/validate-note.py` 增加两条 **ERROR 级**检查：
  - 行内误用块级定界符：正文出现 `$$...$$` 但该行不是独占一行的块级公式；
  - 双反斜杠命令：正文或 Mermaid 内出现 `\\命令`（KaTeX 中 `\\` 是换行符）。
- 保留跳过规则以避免误报：代码围栏内不检查（Mermaid 块单独规则）、行内代码（反引号）剥离后再判、独占一行的 `$$` 与单行块级公式 `$$ ... $$` 合法、**Mermaid 内的 `$$...$$` 合法**（该检查只查 Mermaid 里的双反斜杠）。
- 保留原有三条警告（`\(...\)`、`\[...\]`、`\begin{equation}`）与其余校验行为不变。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `repository-agent-skills`: `Article-note formula guidance matches rendered Markdown` 这条 requirement 增加两条校验行为——行内误用 `$$` 与双反斜杠命令以 ERROR 报出。

## Impact

- 修改 `.agents/skills/article-note/scripts/validate-note.py`（新增一个检查函数并在 main 中调用）。
- 不改 CLI 参数、退出码语义、frontmatter/图片/图号/sidecar 等既有校验；不改 `documentation` skill。
- 存量回归：`management/docs/论文笔记/` 13 篇已确认零违规，因此提升为 ERROR 不会让任何现有笔记失败。
- 不涉及 `knowledge/`（那些文档不由该校验器覆盖）。
