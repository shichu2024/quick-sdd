# 角色赋能设计说明

## 设计目标

基于 `research-inventory.md` 和 `role-capability-matrix.md`，把外部主源中的优秀实践注入 `quick-sdd`，同时保持以下约束：

- 不破坏 `pm -> ra -> ta -> dev -> qa` 的主流程边界。
- 不把角色 prompt 写成庞大百科全书。
- 尽量把共享内容抽到可复用参考层，避免五个角色重复维护。

## 现状判断

`quick-sdd` 当前并非“完全没有专业实践”，而是已经具备一层与角色职责相匹配的基础 guidance：

- `PM` 已经强调 gate check、最小交接包和关键路径思维。
- `RA` 已经强调 `observed / inferred` 区分、验收标准和范围收敛。
- `TA` 已经强调 ownership、接口契约、`read_paths / write_paths / verify`。
- `DEV` 已经强调作用域、证据和边界/回归风险。
- `QA` 已经强调证据优先、根因分类和回流建议。

问题不在于“从零开始”，而在于以下 4 个缺口：

1. 缺少一份显式的、来源可追踪的角色能力框架。
2. 各角色专业实践的深度不均衡，尤其是 `PM / TA / DEV / QA` 还缺少更明确的方法论清单。
3. `agents/openai.yaml` 的入口描述偏流程导向，没有把角色的专业定位暴露出来。
4. 共享实践没有沉淀到公共 reference 层，导致未来只能继续把长说明塞进每个角色 `SKILL.md`。

## 角色缺口审计

| 角色 | 已有基础 | 主要缺口 | 设计动作 |
|---|---|---|---|
| `PM` | 路由、续跑、状态推进、最小交接包 | 缺少任务分拣、目标去噪、审议前后动作、用户决策点、并行化准则 | 扩充 `SKILL.md`，强化 `openai.yaml` 的治理定位 |
| `RA` | 需求收敛、故事拆分、AC、Open Questions | 缺少 story readiness、traceability、单会话粒度、需求与实现解耦的更强表达 | 扩充 `SKILL.md`，强化故事质量与可交接性 |
| `TA` | task 拆解、ACL、依赖、verify | 缺少 ADR/架构一致性、浅依赖图、分层模式、任务设计 heuristics | 扩充 `SKILL.md`，加入架构与验证设计方法 |
| `DEV` | 作用域约束、verify、证据回传 | 缺少明确 TDD 流程、verification loop、编码质量底线、缺上下文时停止机制 | 扩充 `SKILL.md`，强化工程方法而非只强调边界 |
| `QA` | verdict、证据优先、缺陷分级、回流建议 | 缺少 readiness 检查、QA plan、phase gate 思维、审议维度模板 | 扩充 `SKILL.md`，强化前置测试计划和门禁方法 |

## 文件映射方案

| 能力层 | 文件位置 | 写法原则 |
|---|---|---|
| 角色使命、边界、关键工作法 | `skills/quick-sdd-*/SKILL.md` | 直接影响角色默认执行，必须短而明确 |
| 角色入口文案 | `skills/quick-sdd-*/agents/openai.yaml` | 让角色在列表页/唤起时就体现专业定位 |
| 共享方法、检查清单、跨角色原则 | `skills/quick-sdd/references/role-capability-playbook.md` | 作为共享引用层，减少重复 |
| feature 过程记录 | `codespec/specs/FEAT-001-角色专业能力赋能/*.md` | 继续保存研究、设计和状态推进证据 |

## 共享与角色专属的拆分规则

适合放入共享 playbook：

- 全角色共享原则
- readiness / evidence / gate / verification 的共通语言
- “并行只在真正独立时成立”这类跨角色约束

适合放入角色 `SKILL.md`：

- 这个角色的使命、禁止事项、必须执行的方法
- 与上下游角色的交接要求
- 该角色在本仓库中的默认判断顺序

适合放入 `openai.yaml`：

- 对外可见的一句话定位
- 入口 prompt 中最关键的角色专业标签

## 本轮实现顺序

1. 新增共享 `role-capability-playbook.md`。
2. 更新 `PM / RA / TA / DEV / QA` 的 `SKILL.md`，吸收矩阵中的高价值做法。
3. 更新五个角色的 `agents/openai.yaml`，把专业定位前置到入口层。
4. 后续再补 README 与 validation 闭环。

## 当前决策

- 本轮不重写角色文件结构，只做“增量增强”。
- 先补“方法”和“门槛”，再考虑更细粒度模板拆分。
- `quick-sdd` 主 skill 下的 `references/` 将新增共享角色能力文档，而不是在每个角色目录各建一份重复说明。
