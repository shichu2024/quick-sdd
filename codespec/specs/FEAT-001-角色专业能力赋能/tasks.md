# 任务清单

## 索引

| ID | Story | 标题 | 状态 | 依赖 | 负责人 |
|----|-------|-------|--------|------------|-------|
| T-001 | ST-001 | 盘点 claude 顶层 agent 项目与主要能力承载面 | done | - | dev |
| T-002 | ST-001 | 建立项目去重规则与角色研究顺序 | done | T-001 | dev |
| T-003 | ST-002 | 提炼编排与治理类角色优秀实践 | done | T-002 | dev |
| T-004 | ST-002 | 提炼需求、架构、工程、测试类角色优秀实践 | done | T-002 | dev |
| T-005 | ST-002 | 形成 quick-sdd 五角角色能力矩阵 | done | T-003, T-004 | dev |
| T-006 | ST-003 | 审计 quick-sdd 当前角色 skill 缺口 | done | T-005 | dev |
| T-007 | ST-003 | 设计角色赋能分层与文件映射方案 | done | T-006 | dev |
| T-008 | ST-004 | 落地 PM 角色的编排与治理增强 | done | T-007 | dev |
| T-009 | ST-004 | 落地 RA 与 TA 角色的分析与架构增强 | done | T-007 | dev |
| T-010 | ST-004 | 落地 DEV 角色的工程实践增强 | done | T-007 | dev |
| T-011 | ST-004 | 落地 QA 角色的验证与质量门禁增强 | done | T-007 | dev |
| T-012 | ST-004 | 补齐共享参考资料与复用结构 | done | T-008, T-009, T-010, T-011 | dev |
| T-013 | ST-005 | 更新 README 与安装使用说明 | done | T-012 | dev |
| T-014 | ST-005 | 完成一致性检查与 validation 报告 | done | T-013 | qa |

## 阶段 A 研究基线

## T-001 盘点 claude 顶层 agent 项目与主要能力承载面

```yaml
id: T-001
story_id: ST-001
title: 盘点 claude 顶层 agent 项目与主要能力承载面
owner_role: dev
status: done
depends_on: []
read_paths:
  - ../claude/**
  - codespec/specs/FEAT-001-角色专业能力赋能/**
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
verify:
  - type: manual
    value: research-inventory.md 覆盖 claude 六个顶层项目，并记录主要 agent/skill/rule/command 载体
  - type: manual
    value: 文档中标注每个项目的主源文档或关键目录
```

### 目标

<!-- 用 1-3 条描述这个 task 的工程结果。 -->

- 建立 `claude` 六个顶层项目的研究总表。
- 明确每个项目用什么目录和文档承载 agent 角色、skills、rules 与 orchestration 机制。
- 为后续角色提炼准备统一入口，而不是在多个仓库间重复摸索。

### 交付物

<!-- 列出具体输出或可观察结果。 -->

- `research-inventory.md` 中的项目总览表。
- 每个项目的主要研究入口、能力侧重点和与 `quick-sdd` 的关联说明。
- 初始的主源/变体/翻译关系标记。

### 备注

<!-- 可选。补充实现边界、限制条件或复用提示。 -->

- `read_paths` 和 `write_paths` 使用 glob 路径模式。
- 不要在这里重复完整的验收标准。

## T-002 建立项目去重规则与角色研究顺序

```yaml
id: T-002
story_id: ST-001
title: 建立项目去重规则与角色研究顺序
owner_role: dev
status: done
depends_on:
  - T-001
read_paths:
  - ../claude/**
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
verify:
  - type: manual
    value: research-inventory.md 明确主源、补充源、翻译镜像与变体项目的处理策略
  - type: manual
    value: 文档中给出后续按角色提炼的阅读顺序与优先级
```

### 目标

- 避免 `everything-claude-code`、`everything-claude-code-zh`、`harmony-claude-code` 之间出现重复研究。
- 先研究最能提供角色方法论的项目，再研究补充型项目。

### 交付物

- 一份明确的去重规则。
- 一份按角色提炼的研究顺序说明。

### 备注

- 去重规则优先基于职责和内容来源，而不是项目名称。

## 阶段 B 角色能力提炼

## T-003 提炼编排与治理类角色优秀实践

```yaml
id: T-003
story_id: ST-002
title: 提炼编排与治理类角色优秀实践
owner_role: dev
status: done
depends_on:
  - T-002
read_paths:
  - ../claude/agents/**
  - ../claude/Claude-Code-Game-Studios/**
  - ../claude/edict/**
  - ../claude/everything-claude-code/**
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
verify:
  - type: manual
    value: 能力矩阵中至少覆盖 PM 相关的编排、派发、升级、审议、恢复与质量门禁实践
  - type: manual
    value: 每条实践带有来源项目或角色出处
```

### 目标

- 从 `edict`、`agents`、`CCGS`、`ECC` 中抽取适用于 `PM` 的编排治理实践。
- 识别哪些机制适合 Quick SDD，哪些过重只应作为参考。

### 交付物

- `role-capability-matrix.md` 中的 PM 相关章节。

### 备注

- 优先关注角色分层、派发协议、审议机制、恢复策略和质量门禁。

## T-004 提炼需求、架构、工程、测试类角色优秀实践

```yaml
id: T-004
story_id: ST-002
title: 提炼需求、架构、工程、测试类角色优秀实践
owner_role: dev
status: done
depends_on:
  - T-002
read_paths:
  - ../claude/agents/**
  - ../claude/Claude-Code-Game-Studios/**
  - ../claude/everything-claude-code/**
  - ../claude/everything-claude-code-zh/**
  - ../claude/harmony-claude-code/**
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
verify:
  - type: manual
    value: 能力矩阵中覆盖 RA、TA、DEV、QA 的方法、输入输出、质量标准与常见反模式
  - type: manual
    value: 能区分必须内置、共享引用和不建议引入三类实践
```

### 目标

- 为 `RA / TA / DEV / QA` 提炼职责导向而非名称导向的专业实践。
- 把测试驱动、安全审查、架构评审、验收门禁等方法纳入统一矩阵。

### 交付物

- `role-capability-matrix.md` 中除 PM 外的角色章节。

### 备注

- 优先关注能和 Quick SDD 主流程自然耦合的实践。

## T-005 形成 quick-sdd 五角角色能力矩阵

```yaml
id: T-005
story_id: ST-002
title: 形成 quick-sdd 五角角色能力矩阵
owner_role: dev
status: done
depends_on:
  - T-003
  - T-004
read_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/research-inventory.md
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
verify:
  - type: manual
    value: PM、RA、TA、DEV、QA 五个角色均形成能力画像、关键实践、边界约束与来源追踪
  - type: manual
    value: 矩阵可直接作为后续文件改造的输入
```

### 目标

- 将分散实践收敛成 `quick-sdd` 可以直接消费的统一矩阵。
- 输出角色边界、共享能力和角色专属能力的分层结果。

### 交付物

- 完整的 `role-capability-matrix.md`。

### 备注

- 这是从研究进入设计的关口任务。

## 阶段 C 赋能设计

## T-006 审计 quick-sdd 当前角色 skill 缺口

```yaml
id: T-006
story_id: ST-003
title: 审计 quick-sdd 当前角色 skill 缺口
owner_role: dev
status: done
depends_on:
  - T-005
read_paths:
  - skills/quick-sdd-pm/**
  - skills/quick-sdd-ra/**
  - skills/quick-sdd-ta/**
  - skills/quick-sdd-dev/**
  - skills/quick-sdd-qa/**
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
verify:
  - type: manual
    value: enablement-design.md 明确记录每个角色当前缺失的专业能力和待增强点
```

### 目标

- 将 `quick-sdd` 现状与目标能力矩阵做差异分析。
- 找出适合放进角色 prompt、agent manifest、共享 reference 的内容边界。

### 交付物

- `enablement-design.md` 中的差距分析章节。

### 备注

- 缺口分析必须基于现有文件，而不是凭印象判断。

## T-007 设计角色赋能分层与文件映射方案

```yaml
id: T-007
story_id: ST-003
title: 设计角色赋能分层与文件映射方案
owner_role: dev
status: done
depends_on:
  - T-006
read_paths:
  - skills/quick-sdd/**
  - skills/quick-sdd-pm/**
  - skills/quick-sdd-ra/**
  - skills/quick-sdd-ta/**
  - skills/quick-sdd-dev/**
  - skills/quick-sdd-qa/**
  - codespec/specs/FEAT-001-角色专业能力赋能/role-capability-matrix.md
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
verify:
  - type: manual
    value: enablement-design.md 指定每项能力落在哪些文件、以何种形式维护
  - type: manual
    value: 方案说明如何避免内容重复和角色越权
```

### 目标

- 设计“共享参考文档 + 角色 skill + agent manifest”的分层方案。
- 明确后续实现任务的写入范围和顺序。

### 交付物

- 完整的 `enablement-design.md`。

### 备注

- 设计结果要能直接指导实施任务，不再需要二次拆解。

## 阶段 D 角色落地

## T-008 落地 PM 角色的编排与治理增强

```yaml
id: T-008
story_id: ST-004
title: 落地 PM 角色的编排与治理增强
owner_role: dev
status: done
depends_on:
  - T-007
read_paths:
  - skills/quick-sdd-pm/**
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
write_paths:
  - skills/quick-sdd-pm/SKILL.md
  - skills/quick-sdd-pm/agents/openai.yaml
```

### 目标

- 让 PM 在保留路由职责的前提下，具备更成熟的编排、升级、阻塞处理和恢复策略。

### 交付物

- 更新后的 PM skill 与 agent 入口描述。

### 备注

- 避免把 PM 写成“大包大揽”的全能角色。

## T-009 落地 RA 与 TA 角色的分析与架构增强

```yaml
id: T-009
story_id: ST-004
title: 落地 RA 与 TA 角色的分析与架构增强
owner_role: dev
status: done
depends_on:
  - T-007
read_paths:
  - skills/quick-sdd-ra/**
  - skills/quick-sdd-ta/**
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
write_paths:
  - skills/quick-sdd-ra/SKILL.md
  - skills/quick-sdd-ra/agents/openai.yaml
  - skills/quick-sdd-ta/SKILL.md
  - skills/quick-sdd-ta/agents/openai.yaml
```

### 目标

- 为 RA 增补需求澄清、价值切片、风险识别等方法。
- 为 TA 增补架构权衡、任务边界、验证设计和依赖拆解方法。

### 交付物

- 更新后的 RA/TA skill 与 agent 入口描述。

### 备注

- RA 负责需求，TA 负责技术设计，不交叉越权。

## T-010 落地 DEV 角色的工程实践增强

```yaml
id: T-010
story_id: ST-004
title: 落地 DEV 角色的工程实践增强
owner_role: dev
status: done
depends_on:
  - T-007
read_paths:
  - skills/quick-sdd-dev/**
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
write_paths:
  - skills/quick-sdd-dev/SKILL.md
  - skills/quick-sdd-dev/agents/openai.yaml
```

### 目标

- 为 DEV 增补实现前计划、TDD、验证证据、代码质量和安全实践。

### 交付物

- 更新后的 DEV skill 与 agent 入口描述。

### 备注

- DEV 的增强必须服务于单 task 边界，不扩大写权限。

## T-011 落地 QA 角色的验证与质量门禁增强

```yaml
id: T-011
story_id: ST-004
title: 落地 QA 角色的验证与质量门禁增强
owner_role: dev
status: done
depends_on:
  - T-007
read_paths:
  - skills/quick-sdd-qa/**
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
write_paths:
  - skills/quick-sdd-qa/SKILL.md
  - skills/quick-sdd-qa/agents/openai.yaml
```

### 目标

- 为 QA 增补基于证据的验收、风险分类、回流建议和质量门禁策略。

### 交付物

- 更新后的 QA skill 与 agent 入口描述。

### 备注

- QA 负责裁决，不替代 DEV/TA 直接改实现。

## T-012 补齐共享参考资料与复用结构

```yaml
id: T-012
story_id: ST-004
title: 补齐共享参考资料与复用结构
owner_role: dev
status: done
depends_on:
  - T-008
  - T-009
  - T-010
  - T-011
read_paths:
  - skills/quick-sdd/**
  - codespec/specs/FEAT-001-角色专业能力赋能/enablement-design.md
write_paths:
  - skills/quick-sdd/references/**
```

### 目标

- 把多角色共用的优秀实践沉淀为共享参考资料，减少重复复制。

### 交付物

- 新增或更新的共享 reference 文档。

### 备注

- 共享资料是复用层，不应取代角色 skill 的执行指令。

## 阶段 E 验证闭环

## T-013 更新 README 与安装使用说明

```yaml
id: T-013
story_id: ST-005
title: 更新 README 与安装使用说明
owner_role: dev
status: done
depends_on:
  - T-012
read_paths:
  - README.md
  - install/manifest.json
  - skills/quick-sdd*/**
write_paths:
  - README.md
  - install/manifest.json
```

### 目标

- 让使用者知道角色 skill 已经从“流程型”升级为“流程 + 专业实践型”。

### 交付物

- 更新后的仓库说明与安装清单。

### 备注

- 只有在确实需要时才调整安装清单。

## T-014 完成一致性检查与 validation 报告

```yaml
id: T-014
story_id: ST-005
title: 完成一致性检查与 validation 报告
owner_role: qa
status: done
depends_on:
  - T-013
read_paths:
  - README.md
  - install/manifest.json
  - skills/quick-sdd/**
  - skills/quick-sdd-pm/**
  - skills/quick-sdd-ra/**
  - skills/quick-sdd-ta/**
  - skills/quick-sdd-dev/**
  - skills/quick-sdd-qa/**
  - codespec/specs/FEAT-001-角色专业能力赋能/**
write_paths:
  - codespec/specs/FEAT-001-角色专业能力赋能/validation-report.md
verify:
  - type: manual
    value: validation-report.md 给出 decision、证据、残留风险与下一步建议
```

### 目标

- 检查研究、设计、实现和说明文档是否闭环。
- 形成最终验收结论与残留风险说明。

### 交付物

- 更新后的 `validation-report.md`。

### 备注

- QA 结论要基于文件事实和验证证据。
