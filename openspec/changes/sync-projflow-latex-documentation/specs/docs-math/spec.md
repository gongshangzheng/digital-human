## Purpose

定义文档正文与 Mermaid 图中 LaTeX 数学公式的渲染契约：支持的定界符、渲染结果、失败降级，以及不误吞普通美元符号的边界。

## ADDED Requirements

### Requirement: 文档正文支持 LaTeX 数学公式

文档正文 SHALL 支持以 `$...$` 书写的行内公式与 `$$...$$` 书写的块级公式，并渲染为 KaTeX 排版结果；渲染 MUST 保持 Markdown 渲染器的既有安全约束（不放开原始 HTML）。

#### Scenario: 行内公式
- **WHEN** 正文含 `质能关系 $E = mc^2$ 成立`
- **THEN** 该片段渲染为 KaTeX 行内公式（存在 `.katex` 节点），不显示 `$` 字面量

#### Scenario: 块级公式
- **WHEN** 正文含独占一行的 `$$ ... $$` 公式块
- **THEN** 渲染为 KaTeX 块级公式（存在 `.katex-display` 节点），居中成块

#### Scenario: 公式出现在表格中
- **WHEN** 表格单元格内含 `$...$`
- **THEN** 该单元格内渲染为行内公式，表格结构不受破坏

#### Scenario: 不放开原始 HTML
- **WHEN** 正文包含原始 HTML 字符串（如 `<img onerror=...>`）
- **THEN** 仍按文本转义输出，不执行；本能力仅新增数学渲染，不改变 `html: false`

### Requirement: 公式解析失败可降级

当公式语法非法时，渲染 SHALL 不抛异常、不导致整篇文档渲染失败；SHALL 以可辨识的方式呈现原式或错误提示。

#### Scenario: 非法公式
- **WHEN** 正文含 `$\frac{1}{$`（括号不闭合）
- **THEN** 页面其余内容正常渲染，该处不出现未捕获异常导致的空白页

### Requirement: 不误吞普通美元符号

数学解析 SHALL NOT 把普通文本中的美元符号误判为公式定界符；一段文本中若 `$` 不构成合法公式（如内容首尾空白或紧邻数字），SHALL 保持字面显示。

#### Scenario: 金额文本
- **WHEN** 正文含 `价格从 $5 到 $10 不等`
- **THEN** 该句按普通文本显示，不渲染为公式

#### Scenario: 代码块内不解析
- **WHEN** 代码块内含 `$` 或 `$$`
- **THEN** 代码块内容原样保留，不做数学解析

### Requirement: Mermaid 图中的公式正确显示

Mermaid 图节点标签中的 `$$...$$` SHALL 渲染为 KaTeX，且 KaTeX 样式表 SHALL 已加载，使公式的尺寸、间距与字体正确。

#### Scenario: 图内公式
- **WHEN** Mermaid 图中某节点标签写作 `输入 $$x_t$$`
- **THEN** 该标签渲染出 KaTeX 公式（图内存在 `.katex` 节点），不显示 `$$` 字面量

#### Scenario: 样式已就绪
- **WHEN** 检查图内 `.katex` 节点的计算样式
- **THEN** 字体族为 KaTeX 自带字体（如 `KaTeX_Main`），而非站点的默认字体

#### Scenario: 图内不支持单美元
- **WHEN** 图节点标签写作 `输出 $\hat{y}$`（单个 `$`）
- **THEN** 按 Mermaid 自身规则处理（不渲染为公式），属已知边界，不作为缺陷
