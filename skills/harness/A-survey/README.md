# Harness Engineering 生态全景报告

> 调研日期: 2026-06-30 | 作者: 架构猫 (zhipu/glm-5.2)
> 数据源: GitHub API @ 2026-06-30 + awesome-harness-engineering README + QA/PM 独立报告

---

## 一、概念定义

**Harness Engineering**（脚手架工程）是围绕 AI Agent 设计运行时脚手架的系统工程学科。脚手架（harness）指包裹 LLM 的 agent 运行时框架——负责上下文传递、工具接口、规划产物、验证循环、记忆系统和沙箱。

核心洞察（来自 OpenAI/Anthropic）：
- **模型不行，harness 来补**——每个 harness 组件的存在都因为模型单独做不到
- **最佳 harness 设计者知道这些组件会随模型进步而变得不必要**——harness 是过渡性工程
- **harness 设计是主要性能杠杆，不是模型能力**——LangChain 实测：harness-only 改动让 coding agent 从 Terminal Bench 2.0 第 30 名冲到前 5，无模型替换

harness 的四个充要条件（arXiv:2606.10106 构成性定义）：
1. Agent Loop（agent 循环）
2. Tool Interface（工具接口）
3. Context Management（上下文管理）
4. Control Mechanisms（控制机制）

Claude Code、Codex CLI、Aider、Cline、OpenHands、SWE-agent 都满足这四条，是 harness；纯生成器、guardrail、工具包装器不是。

---

## 二、基础理论（Foundations）

### 定义性文章

| 来源 | 文章 | 核心贡献 |
|------|------|----------|
| OpenAI | [Harness Engineering](https://openai.com/index/harness-engineering/) | 将 harness engineering 定义为学科：设计让 Codex 等 agent 可靠运行的脚手架 |
| OpenAI | [Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | Codex agent loop 分解：observe → plan → act → verify |
| Anthropic | [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | workflow vs agent 何时使用，如何组合原语 |
| Anthropic | [Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 多会话持续开发任务的 harness 设计；关键洞察：每个组件都假设模型做不到某事，这些假设会过期 |
| Martin Fowler | [Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) | 三个互锁系统：context engineering + architectural constraints + entropy management；"humans on the loop" 框架 |
| LangChain | [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | 五原语：filesystem + code execution + sandbox + memory + context management；共进化警告：模型会对特定 harness 过拟合 |

### 关键学术论文

| 论文 | 核心贡献 |
|------|----------|
| arXiv:2603.05344 | 终端编码 agent harness 首篇系统实践论文：eager-construction scaffolding + compound multi-model + 5层安全 + schema-filtered planning |
| arXiv:2603.25723 | 自然语言 agent harness (NLAH)：控制逻辑外化为可移植自然语言制品 |
| arXiv:2606.10106 | harness 的充要条件定义，应用于 6 个主流系统 |
| arXiv:2604.18071 | 70 个公开 agent 系统的实证研究，5 个架构模式 |
| arXiv:2604.14228 | 逆向工程 Claude Code 架构：5 阶段渐进压缩 + 27 事件类型 hook pipeline |
| arXiv:2604.11378 | 70 个开源 agent 项目分析：60% 采用 Agent Loop 模式；调度器理论框架 |

### 生产级案例研究

| 案例 | 规模 | 关键发现 |
|------|------|----------|
| Microsoft Azure SRE Agent | 35,000+ 生产事故自动处理 | MTTM 从 40.5h → 3min；filesystem-based context engineering 比 100+ 专用工具更优（Intent Met 45% → 75%）|
| Meta REA (Ads Ranking) | 多日 ML 管道自动化 | hibernate-and-wake 检查点：恢复中断的 6h 任务不丢上下文 |
| GitHub Copilot in VS Code | 生产级 coding agent | 三核心循环职责（上下文组装/工具暴露/工具执行）+ 多 provider 路由 + PR-gated eval |
| Meta CCA (Confucius Code Agent) | SWE-Bench-Pro 59% Resolve@1 | AX/UX/DX 三视角 + 持久笔记 + meta-agent 自动 build-test-improve |

---

## 三、设计原语（Design Primitives）

### 1. Agent Loop（agent 循环）

ReAct（Thought/Action/Observation）是所有 harness 的基础。关键演进：

- **Codex Item/Turn/Thread 协议**（JSON-RPC/JSONL over stdio）：暴露 harness 给所有客户端 surface，MCP 的工具模型不足以支撑审批流/流式 diff/线程持久化
- **Hook pipeline**：Codex 的 `SessionStart`/`PreToolUse`/`PostToolUse` 生命周期钩子；Claude Code 的 27 事件类型
- **Middleware 模式**（LangChain AgentMiddleware）：6 个可组合钩子（before_agent / before_model / wrap_model_call / wrap_tool_call / after_model / after_agent），实现 PII 脱敏/动态工具注入/中途换模型/HITL 中断
- **State machine guardrails**（statewright）：状态机约束工具空间，本地模型从 2/10 → 10/10；证明 loop 结构而非模型大小才是约束瓶颈
- **动态并行编排**（Claude Code dynamic workflows）：plan 存在可执行代码中而非上下文窗口，fan-out 到数百并行子 agent

### 2. Planning & Task Decomposition（规划与任务分解）

- **Plan-then-Execute 分离**：planner 和 executor 可用不同模型/工具/推理预算（Plan-and-Act: WebArena-Lite 57.58%, WebVoyager 81.36%）
- **持久规划制品**：Codex 的 Plan.md / Implement.md / Documentation.md 作为 harness 级状态
- **多 agent 拓扑选择**（LangChain）：subagents vs skills vs handoffs vs router；subagents 在多域场景比 skills 少 67% token（上下文隔离防止跨域膨胀）
- **动态拓扑**（AdaptOrch）：根据任务依赖图动态选择拓扑（并行/顺序/层次/混合），比模型选择单独提升 12-23%
- **跨上下文窗口进度维持**（Anthropic）：initializer agent 建环境 → coding agent 增量推进；feature list + git commit + test gate 作为跨会话状态

### 3. Context Delivery & Compaction（上下文投递与压缩）

- **上下文是有限资源需要策划**，不是越多越好（Anthropic Effective Context Engineering）
- **服务端压缩**（Claude Compaction）：100 轮 web search eval 减少 84% token
- **agent 自主压缩**（LangChain Autonomous Context Compression）：agent 主动调工具触发压缩，避免被动在限额时压缩打断子任务
- **Focus Agent 架构**（arXiv:2601.07190）：agent 自主决定何时将交互历史整合为持久知识块，22.7% token 减少无精度损失
- **context-mode MCP**：拦截原始工具输出，沙箱化 bulky data（Playwright 快照/GitHub issue/日志），按需 BM25 检索片段；"think in code"——用一次脚本执行替代十次文件读取
- **LLMLingua**：微软 prompt 压缩工具，最高 20x 压缩

### 4. Tool Design（工具设计）

- **工具设计就是 Agent UX**（Anthropic）：命名、schema、错误面
- **Beyond Permission Prompts**（Anthropic）：结构化权限系统替代自然语言权限文本
- **Writing Effective Tools for Agents**：工具接口设计原则

### 5. Skills & MCP

- **Skills** = harness 里的能力扩展单元，渐进式披露（Progressive Disclosure）管理上下文
- **MCP**（Model Context Protocol）：工具导向的标准化接口，但 Codex 团队发现 MCP 不足以支撑审批流/流式 diff/线程持久化
- **可移植 .agent/ 文件夹**（agentic-stack）：记忆 + skills + 协议跨 harness 保持知识

### 6. Memory & State（记忆与状态）

- **文件系统作为协作面优于专用工具**（LangChain）：filesystem = 持久状态 + agent 协作面
- **跨会话持久化**：记忆是跨会话延续的关键
- **co-evolution 警告**：模型会对特定 harness 的记忆模式过拟合

### 7. Verification & CI Integration（验证与 CI 集成）

- **结构化验证循环**（lint/test/eval）是 harness 的核心反馈传感器
- **计算控制 vs 推理控制**（Martin Fowler）：linters/tests 是计算控制（确定性）；LLM-as-judge 是推理控制（需独立 eval/score/threshold/rollback）
- **harness 可测试性应成为一等公民**（Birgitta Böckeler）：技术选型时考虑 harnessability

### 8. Observability & Tracing（可观测性与追踪）

- 27 事件类型 hook pipeline（Claude Code）
- 轨迹日志（AgentSPEX: Docker 沙箱 + 50+ MCP tools + checkpointing + trajectory logging）

### 9. Human-in-the-Loop

- **Humans on the loop**（Martin Fowler）：harness 工程师设计和维护 agent 环境，而非检查单个输出
- **HITL 中断**（Middleware）：after_model / after_agent 钩子实现人审中断

---

## 四、热门项目分层清单

### Tier 1 — 全栈 Agent Harness 平台

| 项目 | Stars | 语言 | 核心定位 | 活跃度注意 |
|------|-------|------|----------|-----------|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 223k | JS | agent harness 性能优化系统（skills/instincts/memory/security）| ⚠️ star 数与项目年龄不太相称，需交叉验证 |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 76k | Python | 字节跳动长周期 SuperAgent harness | 字节背书，可信度较高 |
| [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | 69k | Python | "Bash is all you need" — 从 0 到 1 构建类 Claude Code agent harness | 教学性质 |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | 64k | TS | 复杂代码库专用 agent harness，面向 Codex/OpenCode | |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 62k | TS | Agent meta-harness：多 agent swarm 编排 + 自适应记忆 + 自学习 | |
| [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | 46k | Python | 开源超级 AI 助手 & Agent Harness（前身 chatgpt-on-wechat）| |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 25k | Python | LangChain 的 batteries-included agent harness | LangChain 官方 |
| [coleam00/Archon](https://github.com/coleam00/Archon) | 23k | TS | 首个开源 harness builder，让 AI 编码确定性和可重复 | |

### Tier 2 — Meta-Harness / Harness 工厂

| 项目 | Stars | 定位 |
|------|-------|------|
| [revfactory/harness](https://github.com/revfactory/harness) | 8.1k | Team-Architecture Factory：一句话生成 agent 团队 + skills，6 种架构模式 |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | — | Codex port of harness 概念 |
| [ModelEngine-Group/nexent](https://github.com/ModelEngine-Group/nexent) | 5.4k | 零代码平台，Harness Engineering 原则自动生成生产级 AI agent |
| [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) | 3.5k | SDD harness：spec → 自主实现，跨 Claude Code/Codex/Cursor/Copilot |

### Tier 3 — 评估/Eval Harness

| 项目 | Stars | 定位 |
|------|-------|------|
| [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | 13.1k | LLM few-shot 评估框架（业界标准）|
| [bigcode-project/bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness) | 1.05k | 代码生成模型评估 |
| [claw-eval/claw-eval](https://github.com/claw-eval/claw-eval) | 692 | LLM-as-agent 评估，所有任务人工验证 |

### Tier 4 — 知识资源 & 辅助工具

| 项目 | Stars | 定位 |
|------|-------|------|
| [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | 2.1k | **最佳入口**：harness engineering 的 Awesome List |
| [wshobson/agents](https://github.com/wshobson/agents) | 37.3k | 多 harness agent 插件市场（182 agents, 149 skills）|
| [codejunkie99/agentic-stack](https://github.com/codejunkie99/agentic-stack) | 2.1k | 可移植 .agent/ 文件夹（记忆+skills+协议）|

### 其他值得关注的

| 项目 | Stars | 亮点 |
|------|-------|------|
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 185k | 单 CLAUDE.md 改善 Claude Code 行为 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 151k | "Skills for Real Engineers"，直出 .claude 目录 |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 111k | 跨平台 harness 切换器 + skills-management |
| [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU) | 14k | agent memory + self-evolving skills |
| [statewright/statewright](https://github.com/statewright/statewright) | — | 状态机 guardrails，本地模型 2/10 → 10/10 |
| [Tianshi-Xu/Life-Harness](https://github.com/Tianshi-Xu/Life-Harness) | — | 生命周期感知 runtime harness，跨 18 个模型骨干迁移 |
| [aattaran/deepclaude](https://github.com/aattaran/deepclaude) | — | 将 Claude Code 全 agent loop 移植到 DeepSeek V4 Pro |

---

## 五、架构模式总结

### Agent Loop 执行模式（arXiv:2604.11378，70 个项目分析）

| 模式 | 占比 | 特点 |
|------|------|------|
| Agent Loop (ReAct) | 60% | 最常见，observe→plan→act→verify 循环 |
| Event-driven | — | 事件触发 |
| State-machine | — | 状态机约束（如 statewright）|
| Graph/flow | — | DAG（如 LangGraph）|
| Hybrid | — | 混合 |

### 多 Agent 架构模式（arXiv:2604.18071，70 个系统实证）

5 个反复出现的架构模式：
1. **Pipeline** — 顺序依赖任务
2. **Fan-out/Fan-in** — 并行独立任务
3. **Expert Pool** — 上下文依赖的选择性调用
4. **Producer-Reviewer** — 生成后质量审查
5. **Supervisor** — 中央 agent 动态任务分发
6. **Hierarchical Delegation** — 自顶向下递归委托

### 上下文管理策略

| 策略 | 控制方 | 优点 | 风险 |
|------|--------|------|------|
| 固定 token 阈值压缩 | harness | 简单可预测 | 可能在子任务中途打断 |
| Agent 自主压缩 | agent | 语义连贯，不打断 | 依赖 agent 判断力 |
| Focus Agent 知识块 | agent | 22.7% token 减少无精度损失 | 实现复杂 |
| MCP 拦截 + BM25 检索 | harness | bulky data 不进上下文窗口 | 检索质量依赖索引 |

---

## 六、对 Cat Café 的启示

### Learn（立刻值得学的）

1. **Middleware 模式**：Cat Café 的 hook 系统可以参考 LangChain 的 6 钩子模型，明确 before/after agent/model/tool 的拦截点
2. **Plan-then-Execute 分离**：我们的 skill 体系已经隐含了这一点，可以更显式地将 planner 和 executor skill 分开
3. **文件系统作为协作面**：我们已经在做（AGENTS.md / shared-rules / 记忆系统），LangChain 的论文验证了这个方向正确
4. **结构化验证循环**：quality-gate skill 已经在做，可以参考 Anthropic 的 feature list + git commit + test gate 跨会话状态
5. **动态并行编排**：thread-orchestration skill 可以参考 Claude Code 的"plan 存在可执行代码中"模式

### Gap（我们承认的缺口）

1. **eval harness 缺失**：没有系统化的 agent 行为评估框架（EleutherAI/claw-eval 模式）
2. **上下文压缩策略**：依赖 CLI 内置自动压缩，没有 agent 自主压缩或 Focus Agent 策略
3. **harness 可测试性**：技术选型时没有显式考虑 harnessability

### Do Not Follow（我们不做的及理由）

1. **不把所有控制逻辑放进 prompt**：我们选择文件系统外化（shared-rules / AGENTS.md），而非 NLAH 论文的全自然语言控制
2. **不做多 provider 路由**：我们绑定特定模型生态，tradeoff 是丧失灵活性换取深度集成
3. **不追求 harness 组件随模型进步而消失**：我们的 skill 体系有独立的长期价值（协作规范/知识工程），不是纯过渡性工程

---

## 七、信源卫生声明

- ⚠️ 部分 2026 年初新建项目 star 数偏高（如 ECC 223k、karpathy-skills 185k），与项目年龄不太相称。**本文如实呈现 GitHub API 返回值，但建议拆解前交叉验证真实活跃度**（commit 频率 / contributor 数 / issue 活跃度）
- ✅ awesome-harness-engineering 引用大量一手论文和官方博客，信源卫生良好
- ✅ 架构模式总结基于 70 个系统的实证研究（arXiv:2604.18071, arXiv:2604.11378），非主观判断
- ⚠️ revfactory/harness 的 +60% 质量提升为作者自测（n=15），无第三方复现

---

## 八、建议的深入研究路径

1. **入门**：读 awesome-harness-engineering 的 Foundations 部分（OpenAI + Anthropic 博客）
2. **架构对比**：研究 revfactory/harness 的 6 种团队架构模式 vs Cat Café 的多猫编排（→ 见 B-teardown 报告）
3. **实操参考**：ECC 的 hooks 系统 + skill 分层设计
4. **评估方法**：EleutherAI/lm-evaluation-harness + claw-eval 的 eval 框架设计
5. **生产案例**：Microsoft Azure SRE Agent 的 filesystem-based context engineering

---

*报告状态: v1 初稿完成。后续需 clone 源码做深度验证（需 bash 权限）。*
