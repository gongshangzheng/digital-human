## 1. 设计（待用户审核）

- [x] 1.1 提案与现状核对：确认现有校验只覆盖 `\(...\)`、`\[...\]`、`\begin{equation}` 三类 WARNING；确认两类新错误曾真实漏过（face-vid2vid 补图时）
- [x] 1.2 存量扫描：`management/docs/论文笔记/` 13 篇用新规则扫过，零违规 → 可安全取 ERROR 级
- [x] 1.3 **用户审核 design**（D1 跳过规则、D2 级别依据、D4 Mermaid 差异）

## 2. 实现（.agents/skills/article-note/scripts/validate-note.py）

- [x] 2.1 新增纯函数 `check_math_delimiters(body) -> list[str]`：按 D1 的逐行规则实现，带 fence 状态与行内代码剥离
- [x] 2.2 在 main 中于既有三条定界符警告之后调用并 `errors.extend(...)`
- [x] 2.3 更新既有注释（原「warn about unsupported delimiters」）以说明两类新 ERROR 检查与合法写法豁免
- [x] 2.4 确认无新依赖、CLI/输出前缀/退出码语义未变

## 3. 回归与验证

- [x] 3.1 负例 A：临时笔记正文注入行内 `$$f_s$$` → 以 ERROR 报出行号与修法，退出码 1
- [x] 3.2 负例 B：注入 `\\delta`（正文）与 `\\times`（Mermaid 块内）→ 各以 ERROR 报出，退出码 1
- [x] 3.3 正例：跨行块级公式 `$$` … `$$`、单行块级公式 `$$ x $$`、Mermaid 内 `$$x_t$$`、反引号内 `` `$$...$$` `` 均不报错
- [x] 3.4 `management/docs/论文笔记/` 全部 13 篇跑 `validate-note.py` 仍为 `note validation: OK`
- [x] 3.5 `openspec validate docs-validator-inline-math --strict` 通过
- [x] 3.6 提交（`chore(article-note): 校验器新增行内 $$ 与双反斜杠检查`）

## 4. 归档（可选，用户裁决）

- [x] 4.1 走 sync 流程把 MODIFIED requirement 合并进主 spec `openspec/specs/repository-agent-skills/spec.md`（保留原 2 个场景 + 新增 3 个场景），再归档 change
