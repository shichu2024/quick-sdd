# Quick SDD 角色能力矩阵

## 目的

把 `D:/code/github/claude` 中分散的 agent 优秀实践，收敛成适合 `quick-sdd` 五个核心角色的能力框架，为后续 skill 赋能提供直接输入。

## 当前使用的主源

| 来源 | 主要贡献 |
|---|---|
| `edict` | 制度化编排、审议把关、派发执行、状态与进展治理 |
| `Claude-Code-Game-Studios` | 多层角色体系、story readiness、phase gate、协作式而非自动驾驶式工作方式 |
| `everything-claude-code` | planner/architect/TDD/review/security/verification 的工程方法论 |
| `agents` | 架构、安全、测试、代码审查等细粒度专家职责样本 |
| `everything-claude-code-zh` | 中文表达、本地化组织方式补充 |
| `harmony-claude-code` | 轻量变体约束、并行协作和即时调用习惯补充 |

## 全角色共享原则

- 先规划再执行。
来源：`everything-claude-code/AGENTS.md` 的 `Plan Before Execute`；`Claude-Code-Game-Studios` 的阶段式技能链路。

- 协作不是自动驾驶，必须保留用户决策点。
来源：`Claude-Code-Game-Studios/README.md` 的 `Collaborative, Not Autonomous`。

- 质量门禁不能后置到最后一刻，准备度检查、代码审查、阶段 gate 和验证 loop 都要前移。
来源：`story-readiness`、`gate-check`、`code-review`、`verification-loop`。

- 文档与证据必须可追踪，避免“做完就算”。
来源：`create-stories` 的 traceability 要求、`verification-loop` 的报告格式、`edict` 的看板与流转记录。

- 角色边界要清晰，规划、审议、执行、验收不能混成一个角色。
来源：`edict` 的太子/中书省/门下省/尚书省分工，`Claude-Code-Game-Studios` 的 director/lead/specialist 层级。

- 并行只用于真正独立的工作。
来源：`harmony-claude-code/rules/agents.md` 的 parallel task execution 指引。

## 角色总览

| 角色 | 主职责 | 关键主源 | 最适合注入的能力类型 |
|---|---|---|---|
| `PM` | 路由、编排、恢复、阻塞与门禁 | `edict`、`CCGS`、`ECC` | 编排协议、升级策略、状态治理 |
| `RA` | 问题定义、价值切片、故事化表达 | `edict`、`CCGS`、`ECC` | 需求澄清、故事质量、准备度 |
| `TA` | 架构权衡、边界设计、任务拆解 | `agents`、`ECC`、`CCGS` | ADR、任务边界、依赖与验证设计 |
| `DEV` | 在任务边界内实现并自证 | `ECC`、`agents`、`CCGS` | TDD、编码规范、验证闭环、安全与质量 |
| `QA` | 基于证据判定、回流与 gate | `CCGS`、`ECC`、`agents`、`edict` | readiness、测试计划、验收门禁、风险分类 |

## PM

### 角色使命

让正确的角色在正确阶段处理正确文件，并保持状态可恢复、可追踪、可升级。

### 主要源角色

- `edict/taizi`：消息分拣、任务标题提炼、避免把闲聊误判为正式任务。
- `edict/zhongshu`：只做规划，不替代执行角色；方案必须继续推进到审议和派发。
- `edict/menxia`：可行性、完整性、风险、资源四维审议。
- `edict/shangshu`：按部门派发、汇总结果、维护进展。
- `Claude-Code-Game-Studios` 的 `producer / release-manager`：阶段推进、跨团队协调、质量门禁。
- `everything-claude-code` 的 `planner / loop-operator`：复杂任务拆解、续跑与监控。

### 必须内化的实践

- 先判断请求是“闲聊/问答”还是“正式任务”，避免无意义地创建工作项。
- 在派发前先用人话重述目标，去掉原始消息中的路径、会话元数据和噪声。
- PM 负责分析、规划、派发与恢复，不越权替代 RA、TA、DEV、QA 做主体工作。
- 通过明确的审议/门禁节点决定是否继续推进，不能跳过 review 直接执行。
- 一旦进入派发链路，就要负责推进到下一个明确责任人，不能在“方案通过”后停下。
- 维护状态、进度和阻塞说明，让任何一次续跑都能找到下一步最小动作。
- 只有在任务真正独立时才并行推进。
- 需要保留用户决策权，优先给出选项、风险和建议，而不是默认替用户拍板。

### 适合抽成共享参考的实践

- 进度更新模板
- 阻塞升级模板
- 任务标题提炼与去噪规则

### 需要避免的反模式

- PM 变成“全能执行者”
- 未经审议直接派发
- 只更新结论，不维护状态与过程证据
- 为了省事把多个并不独立的任务并行化

## RA

### 角色使命

把模糊需求收敛成可验证、可交接、可实现的用户价值切片。

### 主要源角色/技能

- `edict/zhongshu`：接旨后先分析目标、起草方案、说清楚谁做什么。
- `Claude-Code-Game-Studios/.claude/skills/create-stories`：story 必须小到一个专注会话内可完成，且可追踪到需求与设计决策。
- `Claude-Code-Game-Studios/.claude/skills/story-readiness`：实现前必须排除开放式设计问题和模糊验收标准。
- `everything-claude-code` 的 `planner` 思维：复杂问题先拆阶段和依赖。

### 必须内化的实践

- 先定义问题、目标、价值和边界，再落到 story。
- story 应是单一可实现行为，而不是把多个价值点硬塞进一个故事。
- story 必须自包含，让开发接手时不需要中途二次猜测需求。
- 明确 acceptance criteria，避免“完成了但无法验证”。
- 识别并显式记录 open questions，而不是把不确定性交给下游角色消化。
- 让 story 具备 traceability，知道它对应哪个目标、哪个需求来源。
- 需求文本优先描述用户价值和业务变化，不提前写成技术实现方案。

### 适合抽成共享参考的实践

- Story 拆分检查清单
- 验收标准写作模板
- Open questions 归档模板

### 需要避免的反模式

- 在 story 里偷写架构方案
- story 粒度过大，无法在一个明确 task 周期内落地
- 需求中没有验收标准或仍保留关键设计空洞

## TA

### 角色使命

把“准备好实现的需求”转成边界清晰、依赖清楚、可验证的工程任务设计。

### 主要源角色/技能

- `agents/docs/agents.md` 中的 `backend-architect`、`graphql-architect`、`architect-reviewer` 等架构类角色。
- `everything-claude-code/AGENTS.md` 中的 `architect` 与 `backend-patterns`。
- `Claude-Code-Game-Studios/.claude/skills/create-stories` 与 `code-review`：强调 ADR、控制清单和架构一致性。

### 必须内化的实践

- 架构师定义 epic 和技术边界，开发者接手的是 implementable story/task，而不是反过来。
- 在拆 task 时同步定义依赖关系、接口边界和验证方式。
- 任务设计必须能支撑 traceability，知道每个 task 服务哪个 story/AC。
- 架构决策要引用或沉淀 ADR，避免实现阶段出现“隐性架构”。
- 设计时就考虑回滚、风险和验证，不把这些全部推给 QA。
- 倾向于清晰分层，如 repository/service/controller 等职责分离，而不是把实现揉成一层。
- 把“需要共享的约束”抽成规范或参考，而不是散落在多个任务里。

### 适合抽成共享参考的实践

- Task 边界与依赖设计准则
- ADR 与架构一致性检查清单
- Verify 设计模板

### 需要避免的反模式

- task 太大，无法独立验证
- 架构约束只存在于脑中，没有写进文档或任务
- 为了省事给 DEV 过宽的写范围

## DEV

### 角色使命

在授权边界内稳定实现任务，并主动提交足够的验证证据证明结果可接受。

### 主要源角色/技能

- `everything-claude-code/skills/tdd-workflow`
- `everything-claude-code/skills/verification-loop`
- `everything-claude-code/skills/coding-standards`
- `everything-claude-code/skills/backend-patterns`
- `Claude-Code-Game-Studios/.claude/skills/dev-story`
- `agents/docs/agents.md` 中的语言专家、`test-automator`、`tdd-orchestrator`、`code-reviewer`

### 必须内化的实践

- 严格采用先测后写，至少覆盖单元、集成、E2E 三类验证思维。
- 实现前读取完整上下文，尤其是 story、架构决策和控制约束；缺关键上下文时先停。
- 写完后执行验证闭环：build、types、lint、tests、security、diff review。
- 以可读性优先，遵守 KISS、DRY、YAGNI、命名清晰和默认不可变等基础规范。
- 在任务边界内工作，不擅自扩大实现范围。
- 主动补齐边界条件、错误处理和输入校验，而不是只让 happy path 跑通。
- 输出实现证据，而不是只说“已经完成”。

### 适合抽成共享参考的实践

- TDD 执行模板
- verification loop 检查表
- 通用代码质量底线

### 需要避免的反模式

- 直接编码，不先看 story/ADR/verify
- 测试后补或完全缺失
- 没有 build/type/security 级别的自查
- 把未验证的结果直接交给 QA

## QA

### 角色使命

基于证据而不是感觉给出验收裁决，并把问题分类后正确回流。

### 主要源角色/技能

- `Claude-Code-Game-Studios/.claude/skills/story-readiness`
- `Claude-Code-Game-Studios/.claude/skills/qa-plan`
- `Claude-Code-Game-Studios/.claude/skills/gate-check`
- `Claude-Code-Game-Studios/.claude/skills/code-review`
- `agents/docs/agents.md` 中的 `code-reviewer`、`security-auditor`、`test-automator`
- `edict/menxia`：四维审议与结论输出

### 必须内化的实践

- 在开发前就能定义测试计划和测试类型分类，而不是等实现完再想怎么验。
- 对 story readiness 做明确判定：READY / NEEDS WORK / BLOCKED。
- 验收时同时检查功能、架构一致性、测试证据、安全和阶段门禁，而不是只看“跑过了没”。
- 问题输出要具体到缺口，而不是笼统说“不通过”。
- 裁决要区分 pass / concerns / fail，并给出回流角色与建议动作。
- 基于明确维度审议，例如可行性、完整性、风险、资源，避免纯主观评价。
- 报告要能支持 PM 续跑，包含证据、风险和下一步建议。

### 适合抽成共享参考的实践

- readiness 检查表
- QA 计划模板
- 验收裁决与回流建议模板

### 需要避免的反模式

- 只做结果判断，不说明证据与原因
- 把 requirement gap、task boundary、implementation defect 混成同一类问题
- QA 发现问题后直接自己改实现

## 初步落地判断

| 能力层 | 适合放置位置 | 说明 |
|---|---|---|
| 角色使命、边界、关键工作法 | 角色 `SKILL.md` | 这是角色默认执行面，必须显式可见 |
| agent 展示名、简短入口提示 | `agents/openai.yaml` | 用于让入口文案和角色定位一致 |
| 检查清单、模板、通用实践底线 | `skills/quick-sdd/references/` | 作为共享引用层，减少五个角色重复抄写 |

## 当前结论

- `quick-sdd` 不缺流程骨架，真正缺的是每个角色在自己职责范围内的“专业做法”。
- `PM` 的最佳输入主要来自 `edict`，`DEV` 的最佳输入主要来自 `ECC`，`QA` 最适合融合 `CCGS + ECC + edict`。
- 下一步应进入缺口审计与赋能设计阶段，把这份矩阵逐条映射到 `SKILL.md`、`openai.yaml` 和共享 `references/`。
