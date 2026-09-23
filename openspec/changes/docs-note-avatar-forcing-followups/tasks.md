## 1. 设计与素材确认

- [x] 1.1 用 Semantic Scholar 取回 `2601.00664` 的 16 篇引用与 `2603.14331` 的 7 篇引用（含 arXiv 编号、年份、被引量级、第一作者）。
- [x] 1.2 读取其中 6 篇 arXiv 摘要原文用于核实推进点：Causal Forcing `2602.02214`、Causal Forcing++ `2605.15141`、GDPO-Listener `2603.25020`、AsymTalker `2605.02948`、Human-Preference Expression `2603.07093`、DynaForcing `2608.17707`。
- [x] 1.3 核对 `arxiv.org/abs/2601.00664` 的版本信息（v1 2026-01-02、last revised 2026-05-30）与被引数口径。

## 2. avatar-forcing.md 更新

- [x] 2.1 §0 论文信息：arXiv 行改为 `v1 2026-01-02；v2 2026-05-30`；代码仓库行补 `AVTR-1`（`arXiv:2609.22913`）开放替代；新增「被引」行（16 / influential 4，Semantic Scholar，2026-09-23）。
- [x] 2.2 §7 新增「后续工作（16 篇引用，截至 2026-09）」：按六个分组写引用表（流式架构 / 失效分析 / 双向交互 / 偏好与强化学习 / 长时身份一致 / 外推），含 arXiv 编号、被引量级与推进点，并注明 OpenAlex 同期显示 0 属回溯滞后。
- [x] 2.3 §7 写明「仍然空着的两点」（低维运动隐变量的显式控制接口、低维运动子空间上的偏好优化），措辞限定为"截至上述 16 篇的范围内未见"。
- [x] 2.4 §7 附注同名易混那篇 `2603.14331` 的 7 篇引用，避免归属混淆。
- [x] 2.5 §8 新增 `### 后续文献的补充：运动塌陷被形式化`，写明 DynaForcing 的设定为 self-forcing + DMD 蒸馏、与本篇 diffusion forcing 不同，只作机制对照。
- [x] 2.6 未触碰 §3 方法精析、§4 训练细节、§6 实验数据与配图。

## 3. 待读清单与 sidecar

- [x] 3.1 `论文笔记/README.md`「现有清单」追加 `causal-forcing.md`（`arXiv:2602.02214`）与 `wan-streamer.md`（`arXiv:2606.25041`）两行，状态 `待写`，格式与既有行一致。
- [x] 3.2 未创建这两个 `.md` 正文文件。
- [x] 3.3 `avatar-forcing.json` 追加 changelog 条目（后续工作、两处事实更正、DynaForcing 对照），现共 3 条。

## 4. 验证与交付

- [x] 4.1 校验两个 Markdown 表格列数一致、`##` 级标题数未增（11 / 4）、笔误复查通过、`avatar-forcing.json` 合法。
- [x] 4.2 核对新写入的 17 个 arXiv 编号与 S2 返回清单逐条一致（正文出现 17 个 + 本篇自身 `2601.00664`，无漏、无多、无错）。
- [x] 4.3 `openspec validate docs-note-avatar-forcing-followups --strict` 通过；经 FastAPI 详情接口确认 `论文笔记/avatar-forcing` 与 `论文笔记/README` 可读。
- [x] 4.4 提交 `docs(note): ...`，仅包含预期文件。
