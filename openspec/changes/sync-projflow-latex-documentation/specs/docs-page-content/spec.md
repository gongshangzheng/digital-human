## ADDED Requirements

### Requirement: 数学渲染能力由独立契约维护

文档页内容能力 SHALL 将正文与 Mermaid 的 LaTeX 数学渲染契约委托给 `docs-math` capability；本能力 SHALL 继续负责详情数据、元数据、章节与链接等非数学正文行为，且 MUST NOT 重复定义数学定界符、渲染或降级规则。

#### Scenario: 查找公式行为契约
- **WHEN** 维护者需要确认文档正文或 Mermaid 图中的公式渲染、失败降级或美元符号边界
- **THEN** 可在 `docs-math` capability 中找到该契约，而非在 `docs-page-content` 中找到重复定义

#### Scenario: 既有非数学内容行为不变
- **WHEN** 文档正文包含链接、图片、章节、sidecar 元数据或普通文本
- **THEN** 它们继续遵循 `docs-page-content` 的既有契约，不因数学契约拆分而改变
