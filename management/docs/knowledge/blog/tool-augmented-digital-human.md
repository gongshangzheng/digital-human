---
title: "工具增强型数字人 Agent：当数字人学会调用工具"
description: "调研工具增强型数字人 Agent 领域：从 LLM Agent 工具使用方法学、MCP 标准化协议、VLM Agent 验证循环到人作为可调用工具的前沿范式，梳理已有系统、论文和开放问题。"
created_at: 2026-07-10T15:04:11
updated_at: 2026-07-10T16:20:00
mathjax: true
tags: [数字人, LLM Agent, Tool Use, MCP, VLM Agent]
aliases: ["categories/AI/数字人"]
sub_id: 160
papers: ["https://arxiv.org/abs/2503.21460", "https://arxiv.org/abs/2505.02279", "https://arxiv.org/abs/2506.22355", "https://arxiv.org/abs/2602.12953", "https://arxiv.org/abs/2506.04606", "https://arxiv.org/abs/2406.11200"]
repos: ["https://github.com/zou-group/avatar"]
hero_title: "工具增强型数字人 Agent"
hero_sub: "当数字人学会调用工具"
hero_tagline: "从 MCP 协议到 VLM 验证循环，从人作为工具到工具使用优化"
---

> 来源：博客 gongshangzheng.github.io `src/pages/tool-augmented-digital-human.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/tool-augmented-digital-human.html

8篇核心论文

5系统/产品

7技术路线

8开放问题

引言

数字人为什么需要工具？

如果你问一个从事数字人开发的人——"你的数字人能帮我订一张明天去上海的机票吗？"——大概率得到的回答是沉默，或者"它主要会说话和做表情"。这恰恰是当前数字人技术的一个核心局限：==大多数数字人只是一个会动的嘴==，而非一个能办事的助手。

但如果我们换一个角度思考：数字人的后端是一个 LLM（大语言模型），而 LLM 已经在 ChatGPT、Claude 等系统中展示了强大的工具调用能力——搜索网页、执行代码、操作文件、调用 API。那么问题来了：**为什么不能把这些工具调用能力赋予数字人？** 一个能听懂你说话、看着你的眼睛对话、同时在后台帮你查日历、发消息、检索知识库的数字人，才是真正意义上的"数字人助手"。

这正是本篇调研的核心问题。我们将从 LLM Agent 的方法学框架出发，梳理工具使用在 Agent 架构中的位置；深入 MCP（Model Context Protocol）协议作为工具调用标准化的完整架构；展示已有的产品系统、开源项目和学术论文中数字人调用工具的实例；引入"人作为可调用工具"和"工具使用优化"两个前沿范式；最后从具身 AI 的架构视角指出工具使用尚未被系统性整合的空白，并归纳开放问题。

### 与系列前文的衔接

本系列 S14（[[digital-human-backend-agent-design|数字人后端 Agent 设计]]）已从工程视角覆盖了 Fay MCP 工具管理、OpenAvatarChat Chat Agent 模式和 CyberVerse SubAgent 架构。本文不再重复工程细节，而是从学术视角补充：LLM Agent 方法学框架、MCP 协议的完整架构分析、VLM Agent 验证循环范式、人作为工具的前沿研究，以及工具使用优化方法。

概念界定

什么是"工具增强型数字人 Agent"？

在进入技术细节之前，我们需要明确几个关键概念。

### 核心定义

### 工具增强型数字人 Agent

以 LLM/VLM 为大脑、以数字人（2D/3D avatar、talking head、具身对话 Agent）为交互形态、具备外部工具调用能力的自主 Agent 系统。其核心特征是：数字人不仅能"说"和"动"，还能==调用外部工具完成实际任务==——查询信息、操作业务系统、生成多模态内容，甚至在需要时调用人类获取判断。

### 前置术语表

术语| 定义| 本文首次出现  
---|---|---  
**LLM Agent**|  以大语言模型为推理核心的自主软件实体，具备感知-推理-行动能力| §3  
**Tool Utilization**|  Agent 决策何时使用工具、选择哪个工具的能力| §3  
**MCP**|  Model Context Protocol，Anthropic 2024 年推出的 LLM-工具交互标准协议| §4  
**Function Calling**|  LLM 输出结构化 JSON 以调用外部 API 的机制| §4  
**VLM Agent**|  以视觉-语言模型为大脑的 Agent| §6  
**Verification Loop**|  渲染→评估→调整的自闭环工具使用模式| §6  
**Human Tool**|  将人的能力/信息/权限建模为 MCP 风格可调用工具| §8  
**Contrastive Reasoning**|  通过对比正负样本优化 Agent 工具使用的方法| §9  
  
### 概念关系图

{{< mermaid >}} flowchart TD DH["数字人  
（交互形态）"] --> LA["LLM Agent  
（推理大脑）"] LA --> TU["Tool Utilization  
（工具使用能力）"] TU --> MCP["MCP 协议  
（标准化路线）"] TU --> FC["Function Calling  
（原生路线）"] TU --> CI["代码即接口  
（高级路线）"] MCP --> HT["Human Tool  
（人作为工具）"] TU --> VL["VLM 验证循环  
（自主优化）"] TU --> CR["对比推理  
（元优化层）"] {{< /mermaid >}} 

这个概念关系图揭示了本文的核心叙事线索：数字人的“大脑”是 LLM Agent，而工具使用是 Agent 的核心能力之一。实现工具调用有多种技术路线——MCP 标准化协议、Function Calling 原生支持、代码即接口。在此之上，还有两个前沿方向：将人建模为可调用工具，以及自动优化 Agent 的工具使用策略。

### 任务分类：数字人 Agent 要解决什么？

在进入技术路线之前，我们需要先明确“工具增强型数字人 Agent”到底要解决哪些任务。根据已有系统和论文的研究范围，可以归纳为六类任务：

任务类型| 输入| 输出| 评测重点| 代表工作| 不适用场景  
---|---|---|---|---|---  
**信息查询与知识检索**|  用户自然语言问题| 检索到的事实/知识| 准确率、召回率、延迟| Fay MCP, OpenAvatarChat Chat Agent| 需要实时物理操作的场景  
**业务系统操作**|  用户操作指令| API 调用结果（订票/发消息/查日历）| 操作成功率、端到端延迟| NVIDIA ACE + Game Agent SDK, OpenAI Realtime API| 无 API 接口的遗留系统  
**多模态内容生成**|  文本/图像描述| TTS、表情、姿态、身体动作| 适当性、一致性、自然度、情感表达力| [EMO-Avatar](emo-avatar-2025.html), GenECA| 纯文本对话无需多模态生成  
**3D Avatar 生成与精修**|  文本/图像输入| 可编辑的 3D Avatar 模型| ArcFace ID 相似度、CLIP 对齐度、可编辑性| [SmartAvatar](smartavatar-2025.html)| 2D talking head 场景  
**情感支持与心理咨询**|  用户情感状态/心理需求| 多模态共情响应（语言+表情+姿态）| 心理咨询理论依从性、情感适当性| EMO-Avatar (Hill 三阶段)| 非情感导向的事务性对话  
**人机协作决策**|  复杂任务描述| AI 编排的工作流 + 人类判断输入| 任务完成质量、认知负荷、创意支持指数| Human Tool| 完全自动化、无需人类判断的常规任务  
  
这六类任务并非互斥——一个完整的数字人助手可能同时具备信息查询、业务操作和多模态生成能力。但当前没有任何一个系统覆盖全部六类：产品系统主要集中在前两类，学术研究主要探索后四类。==任务覆盖的碎片化==正是当前工具增强型数字人 Agent 领域的显著特征。

方法学基础

LLM Agent 方法学中的工具使用

要理解数字人如何调用工具，首先需要理解工具使用在 LLM Agent 架构中的定位。北京大学 Luo et al. 的综述 #Luo et al., 2025# 提出了一个三层"Build-Collaborate-Evolve"框架，系统性地将 LLM Agent 的方法学拆解为构建、协作和演化三个维度。

### Build-Collaborate-Evolve 框架

在 Agent Construction（构建）维度，论文定义了四个核心组件：**Profile Definition** （角色定义）、**Memory Mechanism** （记忆机制）、**Planning Capability** （规划能力）和 **Action Execution** （行动执行）。工具使用——即 Tool Utilization——位于 Action Execution 层，与 Physical Interaction（物理交互）并列 #Luo et al., 2025#。

这个定位意味着什么？它告诉我们：工具使用不是 Agent 的独立模块，而是==行动执行能力的子集==。一个 Agent 要使用工具，它需要先有角色定义（"我是谁"），然后有记忆（"之前发生了什么"），再进行规划（"我应该做什么"），最后在行动执行阶段决定是否调用工具。

### 工具使用的两个子能力

该综述进一步将 Tool Utilization 拆分为两个子能力 #Luo et al., 2025#：

  * **Tool-use decision（工具使用决策）** ：决定是否使用工具解决问题。当 Agent 对生成内容的信心不足或面临特定工具功能相关的问题时，应决定使用工具。代表工作包括 TRICE（基于执行反馈的工具学习）和 GPT4Tools（通过自指令教 LLM 使用工具）。
  * **Tool selection（工具选择）** ：理解可用工具及当前情境，选择最合适的工具。代表工作包括 EASYTOOL（通过简化工具文档增强 Agent 对工具的理解）和 AvaTaR（通过对比推理优化工具使用策略）。

### 工具分类

该综述将 LLM Agent 使用的工具分为三类 #Luo et al., 2025#：

工具类别| 描述| 代表工作| 数字人应用场景  
---|---|---|---  
知识检索| 搜索引擎、向量数据库等| WebGPT, ToolCoder| 数字人回答用户事实性问题  
API 交互| RESTful API 调用外部服务| RestGPT, GraphQLRestBench| 数字人操作业务系统（订票、发消息）  
代码执行| 生成并执行代码| —| 数字人生成 3D 内容（如 SmartAvatar）  
  
值得注意的是，该综述在部署工具部分特别提到了 MCP（Model Context Protocol），将其定位为"标准化应用程序向 LLM 提供上下文的方式"和"创建 LLM 与数据源之间安全链接"的开放协议 #Luo et al., 2025#。不过，该综述对 MCP 的讨论相对简短，仅在部署工具一节中提及，未深入分析其对 Agent 架构的影响。这正是我们接下来要展开的内容。

### 评估工具使用能力的 Benchmark

在评估方面，该综述提到了两个直接评估工具使用能力的 benchmark：**Seal-Tools** （1,024 个嵌套工具调用实例，标准化工具使用评估）和 **CToolEval** （398 个中文 API，覆盖 14 个领域）#Luo et al., 2025#。这两个 benchmark 分别面向英文嵌套调用和中文单 API 调用场景，但目前都没有专门针对数字人多模态工具调用的评估基准。

协议层

MCP：工具调用标准化协议

如果说 Function Calling 是 LLM 调用工具的"方言"，那 MCP 就是试图统一这些方言的"普通话"。Ehtesham et al. 的综述 #Ehtesham et al., 2025# 系统性地对比了四种 Agent 互操作协议——MCP、ACP、A2A 和 ANP——其中 MCP 与数字人工具调用的关系最为直接。

### MCP 的架构

MCP 由 Anthropic 于 2024 年 11 月推出，采用 ==JSON-RPC 2.0 客户端-服务器模型==，论文将其比喻为"AI 的 USB-C"——即插即用的通用接口 #Ehtesham et al., 2025#。架构包含两个角色：

  * **Client Application（Host）** ：交互发起方，管理到一个或多个 MCP Server 的连接，编排通信工作流
  * **MCP Server** ：数据和服务提供方，暴露 Tools、Resources、Prompts、Sampling 四种核心能力

MCP 通信采用三层抽象：Protocol Layer（JSON-RPC 2.0 消息交换）、Transport Layer（支持 Stdio 本地通信和 HTTP+SSE 网络通信）、消息类型（Requests/Results/Errors/Notifications）#Ehtesham et al., 2025#。

### 四种核心能力

能力| 控制方| 描述| 数字人应用  
---|---|---|---  
**Tools**|  模型控制| LLM 调用外部 API 或服务| 查询知识库、调用业务系统、生成图像  
**Resources**|  应用控制| 结构化上下文数据| 注入用户画像、历史对话、个性化配置  
**Prompts**|  用户控制| 可复用模板| 对话开场白、特定场景话术  
**Sampling**|  服务器控制| Server 委托文本生成给 Client| 外部系统委托数字人的 LLM 生成内容  
  
### 工具发现与调用流程

MCP 框架下的工具调用包含六个步骤 #Ehtesham et al., 2025#：

{{< mermaid >}} flowchart TD A["1. 初始化连接  
版本协商 + 能力交换"] --> B["2. 工具发现  
tools/list 请求"] B --> C["3. 工具选择  
LLM 自主决策"] C --> D["4. 工具调用  
tools/call JSON-RPC"] D --> E["5. 结果返回  
Server 返回执行结果"] E --> F{"需要更多  
工具调用？"} F -->|"是"| C F -->|"否"| G["6. 响应生成  
LLM 综合结果回复用户"] {{< /mermaid >}} 

这个流程的关键特征是：工具选择由 LLM ==自主决策==（model-controlled），而非人工指定。LLM 接收用户查询，结合可用 Tools 的描述，自主决定是否调用某个 Tool、调用哪个 Tool、以什么参数调用。这使数字人 Agent 具备了"理解意图→选择工具→执行操作→综合回复"的完整工作流。

### MCP vs Function Calling

MCP 相对于 OpenAI 2023 年推出的 Function Calling 有几个关键改进 #Ehtesham et al., 2025#：

维度| Function Calling| MCP  
---|---|---  
工具发现| 静态：初始化时固定| 半动态：Server 声明，Client 运行时获取  
工具元数据| 框架特定，各不统一| 统一的 JSON-RPC schema  
安全边界| 临时性、框架特定| 协议级标准化（OAuth 2.1 + PKCE、mTLS）  
跨框架复用| 需要定制适配器| 模型无关，任何 LLM 可用  
传输方式| API 调用| stdio + HTTP + SSE  
  
对于数字人 Agent 而言，MCP 的价值在于：**数字人可以切换底层 LLM（GPT-4 → Claude → Gemini）而无需重写工具集成** 。这意味着数字人的工具调用能力不再绑定于特定 LLM 厂商的 API，而是通过标准协议实现跨平台兼容。

### 渐进式采用路线图

该综述提出了一个四阶段渐进式采用路线图 #Ehtesham et al., 2025#：

阶段| 协议| 目标| 数字人相关性  
---|---|---|---  
Stage 1| MCP| LLM ↔ 外部工具交互| **最直接相关** ：数字人工具调用基础  
Stage 2| ACP| Agent 间异步/同步通信| 数字人与其他系统 Agent 通信  
Stage 3| A2A| 企业内多 Agent 协作| 数字人在企业生态中被发现和调用  
Stage 4| ANP| 开放互联网 Agent 互联| 数字人作为独立 Agent 节点  
  
这个路线图对数字人的启示是：==短期聚焦 MCP 工具调用==，中期引入 ACP 支持数字人与推荐系统、CRM 等基础设施 Agent 通信，长期考虑 A2A/ANP 实现数字人生态。但在当前阶段，MCP 是唯一与数字人工具调用直接相关的协议。

系统盘点

已有系统：三种工具调用范式

有了方法学框架和协议基础，我们现在回到核心问题：==有没有能够调用工具的数字人？==答案是肯定的，但它们分散在产品系统、开源项目和学术论文中，采用不同的技术路线。我们可以将其归纳为三种范式。

### 范式一：产品级 Function Calling 数字人

在商业产品侧，已经出现了将 function calling 与数字人渲染结合的系统：

  * **NVIDIA ACE + Game Agent SDK** ：NVIDIA 将 ACE（Avatar Cloud Engine）数字人渲染技术与 Game Agent SDK 的 function calling 能力结合，使数字人在游戏和虚拟场景中不仅能对话，还能调用游戏内 API 执行操作。这是目前商业级工具调用数字人的代表。
  * **OpenAI Realtime API** ：OpenAI 的 Realtime API 将语音 Agent 与 function calling 结合，支持实时语音交互中调用外部工具。虽然它本身不是传统意义上的"数字人"（无视觉化身），但其语音 Agent + 工具调用的架构与数字人后端完全一致，延迟约 300ms。

这些产品系统的共同特征是：使用 LLM 原生的 function calling 能力（而非 MCP 协议），将工具定义注入 LLM 上下文，由 LLM 自主决策调用。优势是简单直接、生态成熟；限制是工具定义静态、安全边界临时性、跨框架复用需要定制适配器。

### 范式二：开源系统的 MCP 工具管理

在开源社区，多个数字人项目已经引入了工具调用能力。本系列 S14 已详细分析过这些系统，这里简要归纳其工具调用维度：

系统| 工具调用方式| 核心特征| 局限  
---|---|---|---  
**Fay**|  MCP 工具管理（SSE/Studio）| 支持 MCP Server 注册和工具发现，标准化工具调用| 非实时对话，工具调用偏批处理  
**OpenAvatarChat**|  Chat Agent 模式（v0.6.0）| 支持多轮工具调用，实时语音交互| 工具定义偏简单，缺乏复杂编排  
**CyberVerse**|  PersonaAgent + SubAgent| 主 Agent 编排，子 Agent 执行特定工具| 游戏场景定制，通用性有限  
  
Fay 是最早集成 MCP 的开源数字人系统之一，它支持通过 SSE 或 Studio 模式注册 MCP Server，实现工具的标准化发现和调用。OpenAvatarChat v0.6.0 引入了 Chat Agent 模式，支持在实时语音交互中进行多轮工具调用——用户可以边对话边让数字人查信息、执行操作。CyberVerse 则采用了主从 Agent 架构，PersonaAgent 负责对话和编排，SubAgent 负责特定工具的执行。

### 范式三：LLM Agent 编排多模态工具

在学术研究侧，出现了一种更复杂的范式：LLM Agent 作为中央编排器，协调多个多模态生成工具。

**EMO-Avatar** （ACM MM 2025）是一个 LLM-Agent 编排框架，用于数字人多模态情感支持 #Chen et al., 2025#。其核心创新是将 Hill 三阶段心理咨询理论（exploration → insight → action）融入 LLM Agent 的推理过程。Agent 将 TTS、姿态生成、微表情生成、身体动作生成等模块视为可调用的"工具"，根据对话阶段自适应地选择和组合不同模态的生成工具。在 AvaMERG Challenge 中获得 Top-2 排名，评估维度包括适当性、一致性、自然度和情感表达力。

**GenECA** （Interspeech 2025）是一个通用实时多模态具身对话 Agent 框架，采用模块化流水线架构 #Patapati et al., 2025#。其核心设计包含一个"手势裁判"（Gesture Judge）——一个基于 LLM 的二级分类器，作为 few-shot gesture judge 运行。该分类器审查最近的对话上下文，决定是否触发手势以及选择何种手势。这是一种基于 LLM 判断的工具调用决策机制：LLM 不直接调用工具，而是==判断是否需要调用==特定模态的生成模块。

EMO-Avatar 和 GenECA 的共同特征是：LLM Agent 不是调用外部 API，而是编排==内部的生成模块==（TTS、表情模型、姿态模型）。这种范式的优势是可以将领域知识（如心理咨询理论）编码到 Agent 的推理框架中，指导工具调用决策；限制是编排逻辑复杂、模块间通信导致延迟累积。

深读 SmartAvatar

SmartAvatar：VLM Agent 验证循环

在所有已调研的系统中，SmartAvatar（HKUST + Dartmouth, arXiv 2506.04606）是最完整的"数字人 Agent 使用工具"的学术实例 #Huang-Menders et al., 2025#。它展示了一个 VLM Agent 如何通过验证循环自主使用 6 种工具生成 3D Avatar。

![SmartAvatar 四模块流水线](media/images/tool-augmented-digital-human/smartavatar-pipeline.webp)

图 1：SmartAvatar 的四模块流水线架构。Descriptor 从多模态输入提取语义属性，Generator 生成 Blender 兼容的 Python 代码，Evaluator 评估渲染结果与输入的对齐度，Refiner 基于反馈迭代改进。（来源：SmartAvatar, Fig. pipeline）

### 四模块流水线

SmartAvatar 编排四个模块化 LLM Agent 组成流水线 #Huang-Menders et al., 2025#：

  * **Descriptor** （GPT-4o）：从多模态输入（文本/图像）中提取结构化语义属性，配合预定义的 avatar 构建 API 手册（HumGen3D），将自由文本映射为离散的 API 兼容 token
  * **Generator** （GPT-4o）：接收结构化属性，通过 Chain-of-Thought 推理翻译为 Blender 兼容的 Python 代码
  * **Evaluator** （VLM + 视觉编码器）：比较渲染 avatar 与输入，评估身份和属性对齐度
  * **Refiner** （GPT-4o）：基于 Evaluator 反馈迭代改进 avatar

### 验证循环：渲染→评估→调整

验证循环是 SmartAvatar 的==核心创新==。其机制如下：Agent 生成代码 → Blender 渲染 avatar → Evaluator 评估相似度 → 如果不满足阈值（默认 τ = 90%），Refiner 修改代码 → 重新渲染 → ... 直到达标或达到最大迭代次数 #Huang-Menders et al., 2025#。

评估采用两种方式：视觉编码器计算余弦相似度 $s = \cos(F(I_\text{orig}), F(I_\text{rend}))$，以及 VLM 评估器分析面部相似性、解剖学合理性、属性对齐和感知一致性。

### 工具清单与"代码即接口"范式

SmartAvatar 的 Agent 调用 6 种工具 #Huang-Menders et al., 2025#：

工具| 类型| 功能  
---|---|---  
HumGen3D| 参数化生成器| Blender 插件，提供可修改的 avatar 属性 API  
Blender 4.4| 渲染器| 无头模式执行 Python 代码渲染 avatar  
视觉编码器 F| 评估器| 计算输入与渲染结果的余弦相似度  
VLM Evaluator| 语义评估器| GPT-4o 多模态能力评估多维度对齐  
代码示例库| 检索增强| 存储验证过的代码，用于 few-shot 演示  
API 手册| 约束规范| 枚举所有有效可修改属性及参数值  
  
SmartAvatar 采用"**代码即接口** "（Code-as-Interface）模式：Generator 和 Refiner 不直接操作 3D 模型，而是生成 Python 代码，通过 Blender Python API 执行。这提供了精确的参数控制、可验证可追溯的执行过程，以及代码示例库实现的持续学习能力。

### 实验结果

SmartAvatar 的消融实验揭示了一个关键发现：==迭代精修循环贡献最大== #Huang-Menders et al., 2025#。

条件| ArcFace ID Similarity| CLIP_image| 变化  
---|---|---|---  
Full pipeline| 0.52| 0.809| —  
无 CoT 推理| 0.48| 0.796| ArcFace ↓7.6%  
无迭代精修| 0.42| 0.772| ArcFace ↓19.2%  
  
移除迭代精修循环后，ArcFace ID Similarity 下降 19.2%，远大于移除 CoT 推理的 7.6% 下降。这表明：对于工具增强型 Agent 而言，==验证-修正循环比单次推理质量更重要==。Agent 不需要在第一次就做对，它需要一个能发现错误并自主修正的循环机制。

在图像输入对比中，SmartAvatar 达到 ArcFace 0.65、CLIP 0.903，虽然是唯一同时支持可编辑、可绑定骨骼输出的方法，但 ArcFace 分数低于 PSHuman (0.79) 和 CharacterGen (0.66)——这是因为 SmartAvatar 依赖参数化生成器（HumGen3D），真实感上限受限于引擎能力 #Huang-Menders et al., 2025#。

![SmartAvatar 多模态输入处理](media/images/tool-augmented-digital-human/smartavatar-multimodal-input.webp)

图 2：SmartAvatar 的多模态输入处理。系统支持图像输入、文本输入、图像+文本融合以及生成后编辑指令四种输入类型，文本覆盖优先于图像属性。（来源：SmartAvatar, Fig. multimodal_input）

路线对比

技术路线方法矩阵

综合以上系统盘点和论文分析，我们可以归纳出七条技术路线，它们在协议层、编排层和优化层各有定位。

### 七条技术路线对比

技术路线| 核心表示| 代表工作| 优势| 限制| 工程可得性  
---|---|---|---|---|---  
**MCP 标准化协议**|  JSON-RPC 2.0| Fay MCP, MCP-Agent| 模型无关、统一接口、安全边界| 工具发现偏静态、二进制数据支持有限| 高（开源 SDK）  
**Function Calling**|  LLM 输出 JSON| NVIDIA ACE, OpenAI Realtime API| 简单直接、LLM 原生支持| 工具定义静态、安全边界临时性| 高（主流 LLM 支持）  
**LLM Agent 编排**|  LLM 中央编排器| EMO-Avatar, GenECA, CyberVerse| 灵活组合多模态、领域知识可编码| 编排复杂、延迟累积| 中（需自行实现）  
**VLM 验证循环**|  渲染→评估→调整| SmartAvatar| 自主验证、迭代优化、减少人工| 依赖外部引擎、迭代延迟高| 中（需 VLM API）  
**代码即接口**|  Agent 生成代码| SmartAvatar (Python→Blender)| 精确控制、可验证可追溯| 安全风险、需沙箱化| 中（需安全沙箱）  
**人作为工具**|  人的能力/信息/权限| Human Tool| 利用人类高价值判断、降低认知负荷| 延迟高、不确定性大| 低（实验阶段）  
**对比推理优化**|  Actor-Comparator| AvaTaR| 自动优化、无需人工调参、跨任务泛化| 需训练数据、优化开销| 中（需 DSPy）  
  
### 路线组合关系

这些路线并非互斥，而是可以组合使用：

  * **MCP + Function Calling** ：MCP 可封装 function calling 为标准化 JSON-RPC 调用，两者互补
  * **MCP + LLM Agent 编排** ：MCP 提供工具调用层，LLM 编排器在 MCP 之上决策调用顺序
  * **代码即接口 + VLM 验证循环** ：代码生成提供精确控制，VLM 评估提供自主验证——SmartAvatar 的核心组合
  * **人作为工具 + MCP** ：Human Tool 沿用 MCP 风格的 tool schema，可与其他工具并列
  * **对比推理 + 任何路线** ：AvaTaR 是元优化层，可优化上述任何路线的工具使用策略

**关键发现** ：当前没有任何一个系统同时采用了所有七条路线。产品系统（NVIDIA ACE、OpenAI Realtime API）停留在 Function Calling 层；开源系统（Fay、OpenAvatarChat）已引入 MCP 但缺乏验证循环；学术论文（SmartAvatar）展示了验证循环但未使用 MCP。==将 MCP 标准化协议与 VLM 验证循环结合==，是一个尚未被实现但潜力巨大的方向。

前沿范式

Human Tool：人作为可调用工具

如果说前面的系统都在讨论数字人调用软件工具，那么 Human Tool（清华大学等, arXiv 2602.12953）提出了一个更激进的想法：==人本身也可以是数字人调用的"工具"== #Tang et al., 2026#。

![Human Tool 框架](media/images/tool-augmented-digital-human/human-tool-framework.webp)

图 3：Human Tool 框架。将人类贡献者表示为 AI Agent 可按需调用的结构化工具，通过 Capabilities、Information、Authority 三维建模。Agent 拥有工作流编排权，在需要时自主"调用"人类获取判断、创意或授权。（来源：Human Tool, Fig. framework）

### 核心概念：范式反转

Human Tool 将人定义为"结构化的、可调用的抽象"，使 LLM 可以自主决定何时以及如何引入人类参与 #Tang et al., 2026#。这反转了传统范式：

维度| AI Tool 范式（传统）| Human Tool 范式（本文）  
---|---|---  
编排者| 人类| AI Agent  
人类角色| 工作流领导者、监督者| 可调用工具  
AI 角色| 被人类调用的工具| 编排者 + 人类工具的调用者  
交互模式| 人类持续监督| AI 按需"调用"人类  
  
### 三维建模框架

Human Tool 沿三个维度对人类贡献进行结构化建模 #Tang et al., 2026#：

  * **Capabilities（能力）** ：认知判断、创造力、专业判断、外部世界交互——AI 仍然难以复制的人类能力
  * **Information（信息）** ：领域专业知识、私有/情境信息、偏好约束——AI 无法获取的知识资源
  * **Authority（权限）** ：责任范围、可授权内容——需要人类批准的决策边界

系统基于三种条件决定是否调用人类：能力互补（任务需要创造力或物理交互）、信息交换（任务涉及私有信息或个人偏好）、权限控制（决策需要人类授权）#Tang et al., 2026#。

### 实验结果

32 人受控实验（within-subject counterbalanced 设计，唯一操纵变量是是否启用"人作为工具"机制）的结果令人印象深刻 #Tang et al., 2026#：

指标| Human Tool Group| AI Tool Group| 提升| p 值  
---|---|---|---|---  
TP 准确率| M=86.72| M=72.66| +19.34%| .003  
SW LLM 评分| M=68.38| M=58.56| +14.35%| .006  
SW 人类胜率| M=0.611| M=0.371| —| .003  
CSI（创意支持）| M=75.48| M=52.83| —| 4.90×10⁻⁶  
SW 认知负荷（RSME）| M=70.625| M=87.875| -19.63%| .016  
  
核心发现是：Human Tool 的优势并非来自让人类做得更多，而是让人类==少做错误类型的工作==——Agent 吸收了编排开销（分解、协调、进度跟踪），人类则专注于高价值判断（偏好、意图、创意、主观评估）#Tang et al., 2026#。

对于数字人 Agent 的启示是：如果数字人采纳 Human Tool 范式，它可以自主编排工作流，在需要人类判断时动态"调用"人类。==人类从持续监督中解放，仅在关键决策点提供输入==。这种"人作为工具"的范式为数字人 Agent 的工具库增加了一个高价值但非确定性的工具类型。

优化层

AvaTaR：工具使用优化

前面的系统都在讨论"如何调用工具"，但 Agent 的工具使用策略本身也可以被优化。AvaTaR（NeurIPS 2024, arXiv 2406.11200）提出了对比推理方法，通过 Actor-Comparator 双 LLM 架构自动优化 Agent 的工具使用 #Wu et al., 2024#。

![AvaTaR 对比推理架构](media/images/tool-augmented-digital-human/avatar-overview.webp)

图 4：AvaTaR 的 Actor-Comparator 架构。Actor 是主 LLM Agent，负责使用工具完成任务；Comparator 是独立 LLM，通过对比正负样本的行动序列识别工具使用差异，生成改进指令。（来源：AvaTaR, Fig. overview）

### 对比推理机制

AvaTaR 的核心创新是 **Actor-Comparator** 双 LLM 架构 #Wu et al., 2024#：

  * **Actor（执行器）** ：主 LLM Agent，接收指令生成行动序列（包括工具调用决策）
  * **Comparator（比较器）** ：独立 LLM，从训练数据中采样正例查询和负例查询（各 10 个），Actor 对正负例分别生成行动序列，Comparator 对比正负例的行动序列，识别工具使用中的差异（信息遗漏、无效工具使用、次优分数合成），生成改进指令

这个优化流程迭代进行固定轮次，选择性能最高的行动序列或指令，然后将优化后的策略部署到测试查询。关键超参数为 ℓ = h = 0.5, b = 20（正负例各 10 个）#Wu et al., 2024#。

### 实验结果

AvaTaR 在全部 7 个任务（4 个检索任务 + 3 个 QA 任务）上一致优于所有基线方法 #Wu et al., 2024#：

任务类型| 数据集| 关键结果  
---|---|---  
检索| STaRK (MAG/Prime/Amazon)| Hit@1 平均相对提升 14%  
检索| Flickr30k-Entities| Hit@1 相对提升 9.2%, MRR 提升 13.0%  
QA| HotpotQA| EM 53.0% (vs Retroformer 51.0%)  
QA| ArxivQA (Agenda-hard)| 提升 33.1%  
QA| ToolQA| 平均相对提升 13%  
  
消融实验中，移除 Comparator（AvaTaR-C）后性能显著下降，验证了对比推理模块的有效性。AvaTaR 已集成至 ==DSPy 框架==（作为 AvatarOptimizer），便于在实际系统中部署 #Wu et al., 2024#。

对于数字人 Agent 而言，AvaTaR 的价值在于提供了一个==通用的元优化层==：不需要针对数字人场景重新设计工具使用策略，而是通过对比成功和失败的交互案例，自动生成改进指令。不过，AvaTaR 目前只在文本检索和 QA 任务上验证，尚未涉及多模态工具调用或实时交互场景。

架构视角

具身 AI 视角：工具使用的架构空白

Meta AI 的 position paper "Embodied AI Agents: Modeling the World"（arXiv 2506.22355）提供了一个更高维度的视角：从具身 AI 的完整架构出发，工具使用处于什么位置？答案令人意外——==它几乎不在架构中== #Fung et al., 2025#。

### 三种 Agent 形态

论文将具身 AI Agent 分为三种类型 #Fung et al., 2025#：

  * **Type I - 虚拟具身 Agent (VEA)** ：在数字空间执行 2D/3D 动作，使用可控运动模型调整面部表情和肢体语言——这正是数字人
  * **Type II - 可穿戴 Agent** ：以自我中心视角感知物理世界，规划程序性动作并指导用户
  * **Type III - 机器人 Agent** ：在物理世界中控制机器人动作

论文的 VEA 部分聚焦于表情、手势、情感等呈现层面，以及 RL 训练的运动控制层面。但论文**未讨论** 虚拟 Agent 的外部工具调用能力、API 集成、知识检索与工具增强、多步推理与工具链式调用 #Fung et al., 2025#。

### 工具使用在架构中的位置

论文采用 LeCun (2022) 的模块化自主智能系统架构，包含 Perception、World Model、Actor、Cost、Memory、Configurator 六个模块。在这个架构中，工具使用的位置非常模糊 #Fung et al., 2025#：

  * RAG（检索增强生成）被归入**外部记忆** 模块，作为最突出的外部记忆形式
  * Tool Use 在音频/语音处理中被列为==未解决的挑战==，而非已实现的系统能力
  * 在机器人能力分类中，"tool use" 指物理工具的操作能力（如抓取、放置）
  * 论文没有提出专门的工具调用框架或工具增强架构

**关键洞察** ：在具身 AI Agent 架构中，工具使用尚未被系统性整合为一级架构组件。现有架构将"知识获取"主要归入记忆模块（RAG），而非独立的工具调用模块。这恰恰表明：==将工具使用提升为独立架构组件==是一个有待填补的研究空白——也是"工具增强型数字人 Agent"的研究机会。

### 可借鉴的架构元素

尽管工具使用薄弱，论文的架构对数字人 Agent 仍有重要启示 #Fung et al., 2025#：

  * **世界模型作为推理核心** ：数字人 Agent 可以通过世界模型决定"何时调用工具"和"调用什么工具"
  * **心智世界模型** ：数字人需要理解用户的目标、意图和情绪，以选择合适的工具辅助策略
  * **记忆层级** ：短期记忆（对话上下文）、长期记忆（用户画像）、外部记忆（RAG/工具检索）的三层架构可直接应用
  * **情节记忆** ：论文提出的可扩展情节记忆概念可用于存储数字人与用户的长期交互历史

发展脉络

时间线：从工具萌芽到人作为工具

### 2023：工具使用范式萌芽

2023 年是 LLM 工具使用的元年。OpenAI 推出 Function Calling，允许 LLM 输出结构化 JSON 调用外部 API。Toolformer 展示了 LLM 可以通过自监督学习预测 API 调用位置，ReAct 提出了推理与行动交替的链式范式。这些工作奠定了基础，但尚未涉及数字人场景。工具定义是静态的，各框架格式不统一，无安全标准。

### 2024：协议标准化与 Agent 编排

2024 年出现两个关键转变。一是 Anthropic 于 11 月推出 MCP，将 LLM-工具交互标准化为 JSON-RPC 2.0 客户端-服务器模型。二是 AvaTaR（NeurIPS 2024）提出对比推理方法，在 7 个任务上一致优于基线（Hit@1 +14%, QA +13%）#Wu et al., 2024#。同时，开源数字人系统开始引入工具调用——Fay 支持 MCP 工具管理，OpenAvatarChat 引入 Chat Agent 模式。

### 2025：数字人 Agent 工具使用多元化

2025 年出现多个直接面向数字人/Avatar 的工具使用系统。SmartAvatar 展示 VLM Agent 验证循环（消融显示迭代精修贡献最大，ArcFace -19.2%）#Huang-Menders et al., 2025#。EMO-Avatar 将 Hill 三阶段心理咨询理论融入 LLM Agent 推理（AvaMERG Top-2）#Chen et al., 2025#。GenECA 展示实时具身对话 Agent 的模块化流水线 #Patapati et al., 2025#。产品侧，NVIDIA ACE 结合 Game Agent SDK，OpenAI Realtime API 将语音 Agent 与 function calling 结合。

### 2026：前沿范式——人作为工具

Human Tool 开创了将人建模为 MCP 风格可调用工具的范式（TP 准确率 +19.34%，认知负荷 -19.63%）#Tang et al., 2026#。同期 Embodied AI Agents position paper 暴露了工具使用在虚拟 Agent 架构中未被系统性整合的空白 #Fung et al., 2025#。

### 跨阶段转变

转变点| 之前| 之后| 推动力  
---|---|---|---  
静态工具定义 → 标准化协议| Function Calling: 各框架格式不统一| MCP: JSON-RPC 统一接口| Anthropic 推出 MCP  
单工具调用 → 多工具编排| ReAct/Toolformer: 单步调用| EMO-Avatar/SmartAvatar: 多工具协调| LLM Agent 架构成熟  
软件工具 → 人作为工具| 仅限 API/软件| Human Tool: 人也是可调用资源| MCP 风格框架泛化  
文本工具 → 多模态工具| 聚焦文本搜索/API| TTS/渲染/表情/姿态| VLM 和多模态 LLM 成熟  
人工调参 → 自动优化| 依赖人工设计 prompt| AvaTaR: 对比推理自动优化| Actor-Comparator 架构  
  
开放问题

开放问题与未来方向

### 1\. 工具使用在数字人架构中的一级组件化

Meta AI 的论文将工具使用仅归入"外部记忆"或视为"未解决挑战"，而非独立架构组件。如果工具使用不被提升为一级组件，数字人 Agent 的工具调用能力只能作为临时附件。当前缺乏将工具使用与感知/记忆/规划模块交互机制的系统设计。

### 2\. MCP 在实时多模态场景中的性能验证

数字人需要 ≤500ms 端到端延迟和音频/视频流的多模态工具调用。MCP 的 JSON-RPC 消息格式对二进制数据支持有限，stdio/HTTP+SSE 传输层的实时性未经验证。产品系统（NVIDIA ACE、OpenAI Realtime API）使用自有 function calling 而非 MCP，缺乏 MCP 在实时数字人场景中的延迟基准测试。

### 3\. 工具发现与动态工具注册

数字人 Agent 在运行时可能需要调用新出现的工具（如新 API、用户自定义工具）。MCP 的工具发现是半静态的（Server 启动时注册），虽然支持 Notifications 通知能力变更，但动态性有限。缺乏数字人场景中动态工具注册的用例研究。

### 4\. 多模态工具调用的状态管理

数字人需要维护对话状态、用户画像、情感上下文、工具调用历史等持续状态。MCP 的 "Stateless + optional persistent tool context" 会话模型可能不足以支持持续的个性化交互。缺乏长期个性化数字人场景中的状态管理方案。

### 5\. Prompt Injection 与工具安全

MCP 明确将 "Tool Poisoning"（恶意 prompt 影响 LLM 行为）列为运行阶段威胁。数字人 Agent 调用外部工具时，工具返回的数据可能包含恶意指令。缺乏针对数字人 Agent 的 prompt injection 攻击-防御实证研究。

### 6\. 人作为工具的延迟与不确定性

Human Tool 将人建模为可调用工具，但人类响应具有高延迟（秒级到分钟级）和不确定性（可能拒绝、可能出错）。数字人实时交互中，等待人类响应会破坏对话流畅性。缺乏超时处理和降级策略。

### 7\. 跨协议互操作

渐进式采用路线图（MCP→ACP→A2A→ANP）意味着完整生态需要支持四种协议，但当前无标准化的跨协议桥接机制。缺乏"协议网关"或"元协议"层的设计方案。

### 8\. 工具使用优化在数字人场景的适配

AvaTaR 的对比推理在通用任务上有效（7 任务一致提升），但数字人场景具有多模态、实时性、情感上下文等特殊性。缺乏 AvaTaR 在数字人多模态工具调用场景的实验，以及对比推理在实时约束下的优化效率评估。

结语

总结与展望

回到开篇的问题——==有没有能够调用工具的数字人？==答案是肯定的，但它们还处于早期阶段。

从产品侧看，NVIDIA ACE 和 OpenAI Realtime API 已经展示了商业级的工具调用数字人，但它们使用的是自有 function calling 而非标准化协议。从开源侧看，Fay 和 OpenAvatarChat 已经引入了 MCP 工具管理，实现了标准化工具调用，但在多模态编排和验证循环方面还有很大提升空间。从学术侧看，SmartAvatar 展示了 VLM Agent 验证循环的完整范式，EMO-Avatar 展示了领域知识指导的多模态工具编排，Human Tool 开创了人作为工具的前沿范式，AvaTaR 提供了工具使用优化的元方法。

但我们也看到了明显的空白：==没有任何一个系统同时实现了 MCP 标准化协议 + VLM 验证循环 + 工具使用优化==。工具使用在具身 AI 架构中尚未被系统性整合。MCP 在实时多模态场景中的性能未经验证。人作为工具的延迟和不确定性需要更鲁棒的处理机制。

这些空白恰恰是未来的研究方向。一个理想的工具增强型数字人 Agent 应该：使用 MCP 标准化工具调用、具备 VLM 验证循环的自闭环优化能力、通过对比推理自动改进工具使用策略、在需要时调用人类获取高价值判断，并将工具使用作为架构的一级组件与世界模型、记忆、规划模块深度整合。

[←上一章 S14数字人后端 Agent 设计理念](digital-human-backend-agent-design.html) [枢纽页数字人系列总览](digital-human-hub.html) [→下一章 S15训练全景：Loss 函数族](digital-human-training-loss-survey.html)

### 参考来源

  * Luo, J. et al. (2025). "Large Language Model Agent: A Survey on Methodology, Applications and Challenges." _arXiv preprint_. [arXiv:2503.21460](https://arxiv.org/abs/2503.21460)
  * Ehtesham, A. et al. (2025). "A Survey of Agent Interoperability Protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)." _arXiv preprint_. [arXiv:2505.02279](https://arxiv.org/abs/2505.02279)
  * Fung, P. et al. (2025). "Embodied AI Agents: Modeling the World." _Meta AI Research (FAIR)_. [arXiv:2506.22355](https://arxiv.org/abs/2506.22355)
  * Tang, Y. et al. (2026). "Human Tool: An MCP-Style Framework for Human-Agent Collaboration." _arXiv preprint_. [arXiv:2602.12953](https://arxiv.org/abs/2602.12953)
  * Huang-Menders, A. et al. (2025). "SmartAvatar: Text- and Image-Guided Human Avatar Generation with VLM AI Agents." _HKUST & Dartmouth College_. [arXiv:2506.04606](https://arxiv.org/abs/2506.04606) · [精读 →](smartavatar-2025.html)
  * Chen, K. et al. (2025). "EMO-Avatar: An LLM-Agent-Orchestrated Framework for Multimodal Emotional Support in Human Animation." _ACM Multimedia 2025_. [DOI:10.1145/3746027.3762030](https://dl.acm.org/doi/10.1145/3746027.3762030) · [精读 →](emo-avatar-2025.html)
  * Patapati, S. et al. (2025). "GenECA: A General-Purpose Framework for Real-Time Adaptive Multimodal Embodied Conversational Agents." _Interspeech 2025_ , pp. 3541–3542. [ISCA Archive](https://www.isca-archive.org/interspeech_2025/patapati25_interspeech.html)
  * Wu, S. et al. (2024). "AvaTaR: Optimizing LLM Agents for Tool Usage via Contrastive Reasoning." _NeurIPS 2024_. [arXiv:2406.11200](https://arxiv.org/abs/2406.11200) · [GitHub: zou-group/avatar](https://github.com/zou-group/avatar)
