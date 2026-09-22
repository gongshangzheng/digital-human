# Proposal: docs-note-avatar-forcing-rewrite（按 article-note 重写 Avatar Forcing 笔记）

## Why

现有 `management/docs/论文笔记/avatar-forcing.md` 把**两篇不同论文缝在了一起**：

- frontmatter 与正文两处「论文：」都引 **`arXiv:2603.14331`**（AvatarForcing: One-Step Streaming Talking Avatars via Local-Future Sliding-Window Denoising，浙大 + 快手 Kling）
- 正文全部技术内容与指标（`z = z_S + m_S`、Dual Motion Encoder、DPO 丢用户条件、500ms / 6.8× / >80%）属于 **`arXiv:2601.00664`**（Avatar Forcing: Real-Time Interactive Head Avatar Generation for Natural Conversation，KAIST / NTU / DeepAuto.ai，CVPR 2026）
- 小标题「一步式流式说话头像」来自 2603.14331 的标题，被嫁接到了 2601.00664 的内容上
- 该笔记也没有 sidecar、没有配图，且 `论文笔记/README.md` 仍标「待写」

我们已经决定**只保留 2601.00664 这一篇**。按 `article-note` 流水线重写，可以在流程上强制解决论文身份错配，并补齐配图与 sidecar。

## What Changes

- **重写** `management/docs/论文笔记/avatar-forcing.md`：按 `article-note` 的 10 节骨架组织，论文层以 2601.00664 的真实元信息为准；工程层（流式改造 / 中文适配 / 漂移诊断）压缩进「在我们体系中的角色」与「局限与启发」，细节继续链到 `实习复盘/`。
- **修正引用**：frontmatter 与正文的 arXiv ID、标题、机构全部改为 2601.00664；在「论文信息」表里显式与 2603.14331 区分，避免再次混淆。
- **补配图**：从论文 source 抽取原图，转 WebP 后发布到 `management/docs/_assets/avatar-forcing/`，正文用绝对 URL 引用（≥3 张，依赖 `sync-projflow-round3` 的图片端点）。
- **补 sidecar**：`management/docs/论文笔记/avatar-forcing.json`，`changelog` 记录本次重写与旧笔记错引。
- **修 README**：`论文笔记/README.md` 中该篇状态由「待写」改为已完成。
- **不做**：不为 2603.14331 另开笔记（用户已明确只需要 2601.00664）。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

（无）

> 说明：纯文档重写，不改变任何行为契约，`.openspec.yaml` 设 `skip_specs: true`。

## Impact

- 文档：`management/docs/论文笔记/avatar-forcing.md`（重写）、新增 `avatar-forcing.json`、更新 `论文笔记/README.md`
- 资产：新增 `management/docs/_assets/avatar-forcing/`（WebP 图片）
- 素材工作区：`.cache/article-note/avatar-forcing/`（gitignored）
- 不涉及后端/前端代码、API、端口与业务数据；不动其它笔记
