# Claude Agent 项目研究清单

## 目的

为 `FEAT-001` 建立一个可续跑的研究基线，确保我们对 `D:/code/github/claude` 的学习覆盖完整、去重明确，并且能直接支撑后续的角色能力提炼。

## 顶层项目总览

| 项目 | 主要定位 | 主要能力承载面 | 主要研究入口 | 对 quick-sdd 的主要价值 | 去重备注 |
|---|---|---|---|---|---|
| `agents` | 大型插件化 agent 市场，提供 182 个专业 agent | `plugins/*/agents/`、`plugins/*/skills/`、`docs/agents.md` | `agents/docs/agents.md`、`agents/README.md` | 提供细粒度角色专家库与模型分层样本 | 主源 |
| `everything-claude-code` | 通用 AI 编码工作台，强调 planner/TDD/review/security/workflow | `AGENTS.md`、`agents/`、`skills/`、`rules/`、`hooks/` | `everything-claude-code/AGENTS.md`、`CLAUDE.md` | 提供工程流程、代码质量、TDD、安全与验证方法 | 主源 |
| `everything-claude-code-zh` | ECC 的中文化/变体仓库 | `AGENTS.md`、`skills/`、`rules/`、`docs/zh-CN/` | `everything-claude-code-zh/AGENTS.md` | 适合作为中文表达与本地化补充 | 以 ECC 为主，当前仓库为补充源 |
| `harmony-claude-code` | 轻量变体，保留 agent orchestration 与工程 skills | `rules/agents.md`、`skills/` | `harmony-claude-code/rules/agents.md` | 提供更简化的角色集合与移动/Harmony 场景经验 | 变体源，选择性吸收 |
| `Claude-Code-Game-Studios` | 游戏工作室化多角色体系，49 agents、72 skills、强层级和质量门禁 | `.claude/agents/`、`.claude/skills/`、`.claude/rules/`、`.claude/docs/templates/` | `Claude-Code-Game-Studios/README.md` | 提供多层角色体系、阶段门禁、跨团队协作与 readiness/release 流程 | 主源 |
| `edict` | 制度化多 agent 编排系统，强调审议、派发、审计、看板与恢复 | `agents/*/SOUL.md`、`docs/`、`scripts/`、`dashboard/` | `edict/README.md`、`docs/task-dispatch-architecture.md` | 提供 PM/QA 向的审议、派发、状态管理和治理实践 | 主源 |

## 已确认的主要结构特征

- `agents` 项目以插件为核心，每个插件下普遍存在 `agents/`，很多插件还配有 `commands/` 与 `skills/`；`docs/agents.md` 已经给出了 182 个 agent 的分类清单。
- `everything-claude-code` 同时维护多种客户端/运行面，例如 `.codex`、`.claude`、`.cursor`、`.opencode`，但核心工程理念集中在 `AGENTS.md`、`skills/`、`rules/`、`hooks/`。
- `everything-claude-code-zh` 与 `everything-claude-code` 结构高度相似，更适合作为中文术语和本地化表达参考，而不是重复抽取同一套工程实践。
- `harmony-claude-code` 是更窄的变体，保留 `rules/agents.md` 和一组工程技能，适合作为“如何保持轻量”的补充样本。
- `Claude-Code-Game-Studios` 用三层工作室架构组织角色，显式定义 director、lead、specialist 层级，并通过 skills、rules、hooks 与 templates 形成完整流程面。
- `edict` 用制度型角色分工组织多 agent 协作，角色集中在 `taizi / zhongshu / menxia / shangshu / bingbu / xingbu / gongbu / libu / hubu` 等实体中，强项在于审议、派发、状态机、看板和可审计性。

## 面向 quick-sdd 的初始角色映射

| quick-sdd 角色 | 优先研究来源 | 关注点 |
|---|---|---|
| `PM` | `edict`、`Claude-Code-Game-Studios`、`everything-claude-code` | 编排、派发、升级、阻塞处理、恢复、质量门禁 |
| `RA` | `edict`、`Claude-Code-Game-Studios`、`everything-claude-code` | 需求澄清、目标切片、问题定义、风险识别、故事化表达 |
| `TA` | `agents`、`everything-claude-code`、`Claude-Code-Game-Studios` | 架构权衡、任务边界、依赖设计、验证设计 |
| `DEV` | `everything-claude-code`、`agents`、`Claude-Code-Game-Studios` | TDD、代码质量、安全、实现边界、证据回传 |
| `QA` | `agents`、`everything-claude-code`、`Claude-Code-Game-Studios`、`edict` | 验收策略、质量门禁、回流建议、风险分类、审议机制 |

## 初始去重策略

- `everything-claude-code` 视为通用工程流程主源。
- `everything-claude-code-zh` 视为 ECC 的中文补充源，优先吸收表达方式和本地化组织，不重复抽取同一工程原则。
- `harmony-claude-code` 视为变体源，优先提取“轻量化角色集”和移动场景相关经验，不与 ECC 做逐项对照复写。
- `agents`、`Claude-Code-Game-Studios`、`edict` 视为三个主源，分别负责“细粒度专家实践”“层级协作与质量门禁”“制度化编排与审议”。

## 建议研究顺序

1. `edict`
说明：先拿下编排、审议、派发、状态与恢复，因为这些最接近 `quick-sdd` 的 PM/QA 能力增强。

2. `Claude-Code-Game-Studios`
说明：补充多层角色体系、阶段门禁、story/sprint/release 流程与跨团队协作方式。

3. `everything-claude-code`
说明：补充 planner、architect、tdd-guide、code-reviewer、security-reviewer 等工程角色的方法论。

4. `agents`
说明：为 TA/DEV/QA 提供细粒度的架构、语言、安全、测试和基础设施专家实践样本。

5. `everything-claude-code-zh`
说明：用于中文术语、本地化表达和部分技能封装差异校对。

6. `harmony-claude-code`
说明：用于验证哪些实践在轻量变体中仍然成立，帮助 quick-sdd 控制体量。

## 当前结论

- 这次工作不适合直接“抄 prompt”，而是应该先把主源项目按职责拆解，再把可复用的实践映射到 `quick-sdd` 五个核心角色。
- `edict` 与 `Claude-Code-Game-Studios` 对 `PM / QA / TA` 的启发尤其大，`everything-claude-code` 与 `agents` 对 `DEV / QA / TA` 的启发尤其大。
- 下一步优先进入能力矩阵阶段，先把各角色的优秀实践抽出来，再决定哪些写进 `SKILL.md`，哪些下沉为共享 reference。
