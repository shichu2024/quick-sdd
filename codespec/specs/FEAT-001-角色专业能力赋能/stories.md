# 用户故事

## 索引

| ID | 标题 | 优先级 | 状态 | 依赖 |
|----|-------|----------|--------|------------|
| ST-001 | 建立 claude agent 项目研究基线 | P1 | ready | - |
| ST-002 | 提炼 quick-sdd 角色能力矩阵 | P1 | ready | ST-001 |
| ST-003 | 设计 quick-sdd 角色赋能落地方案 | P1 | ready | ST-002 |
| ST-004 | 落地角色 skill 专业能力增强 | P1 | ready | ST-003 |
| ST-005 | 完成验证与安装使用闭环 | P1 | ready | ST-004 |

## ST-001 建立 claude agent 项目研究基线

```yaml
id: ST-001
title: 建立 claude agent 项目研究基线
priority: P1
status: ready
depends_on: []
```

### 故事

<!-- 尽量使用标准的 “作为 / 我想要 / 以便” 结构。 -->

作为 quick-sdd 维护者，我希望先系统盘点 `D:/code/github/claude` 下所有 agent 项目和角色载体，以便后续赋能建立在完整、去重、可追踪的研究基线上。

### 验收标准

<!-- 为验收标准分配稳定 ID，便于轻量 traceability。 -->

- `AC-1`: Given `D:/code/github/claude` 的六个顶层项目，when 研究基线完成，then 每个项目的 agent/skill/rule/command 主要承载目录和核心说明文档都被记录。
- `AC-2`: Given 英文版、中文版和变体项目并存，when 建立项目清单，then 重复来源、补充来源和主源关系被显式标注。
- `AC-3`: Given 后续还要继续做能力提炼，when 基线文档交付，then 它能够直接支持按角色继续抽取优秀实践，而不是重新盘点目录。

### 范围外

<!-- 可选。如果这一节没有增加清晰度，可以删除。 -->

- 不在本 story 中直接改写 `quick-sdd` 角色 skill。

## ST-002 提炼 quick-sdd 角色能力矩阵

```yaml
id: ST-002
title: 提炼 quick-sdd 角色能力矩阵
priority: P1
status: ready
depends_on:
  - ST-001
```

### 故事

作为 quick-sdd 维护者，我希望把外部 agent 项目中的优秀实践提炼成面向 `PM / RA / TA / DEV / QA` 的能力矩阵，以便每个角色都有清晰的专业职责、方法和质量门槛。

### 验收标准

- `AC-1`: Given 已完成的项目研究基线，when 角色提炼完成，then `PM / RA / TA / DEV / QA` 每个角色都有对应的优秀实践清单。
- `AC-2`: Given 不同项目的角色命名差异较大，when 输出能力矩阵，then 映射基于职责而不是字面名称，并保留来源追踪。
- `AC-3`: Given Quick SDD 需要轻量，when 能力矩阵完成，then 区分“必须内置”“可引用参考”“不应引入”的实践层级。

### 范围外

- 不在本 story 中直接决定最终写入哪些具体文件。

## ST-003 设计 quick-sdd 角色赋能落地方案

```yaml
id: ST-003
title: 设计 quick-sdd 角色赋能落地方案
priority: P1
status: ready
depends_on:
  - ST-002
```

### 故事

作为 quick-sdd 维护者，我希望先设计能力注入方案和文件映射规则，以便新增专业能力时保持仓库结构清晰、安装路径稳定、角色边界不被打乱。

### 验收标准

- `AC-1`: Given 已产出的角色能力矩阵，when 设计完成，then 能明确哪些实践进入 `SKILL.md`、哪些进入 `agents/openai.yaml`、哪些进入共享参考文档。
- `AC-2`: Given 角色边界是 Quick SDD 的核心约束，when 设计赋能方案，then 新增专业实践不会替代既有的 `pm -> ra -> ta -> dev -> qa` 分工。
- `AC-3`: Given 仓库需要可维护，when 设计文档完成，then 对新增/更新文件、复用关系和验证方式有清晰说明。

### 范围外

- 不在本 story 中完成所有最终文件改动。

## ST-004 落地角色 skill 专业能力增强

```yaml
id: ST-004
title: 落地角色 skill 专业能力增强
priority: P1
status: ready
depends_on:
  - ST-003
```

### 故事

作为 quick-sdd 维护者，我希望把研究和设计结果写入各角色 skill，使 `pm / ra / ta / dev / qa` 在遵守 SDD 流程的同时，也具备本职工作的专业方法和高质量实践。

### 验收标准

- `AC-1`: Given 赋能方案已确认，when 角色文件更新完成，then 五个核心角色都获得与其职责匹配的专业实践增强。
- `AC-2`: Given Quick SDD 仍需轻量，when 修改完成，then 共享内容优先被抽到可复用参考文档，避免多处重复。
- `AC-3`: Given 角色执行边界很重要，when 文件改完，then 新 prompt 和 agent 配置仍明确各角色不能越权代替其他角色。

### 范围外

- 不在本 story 中扩展到核心五角之外的额外角色。

## ST-005 完成验证与安装使用闭环

```yaml
id: ST-005
title: 完成验证与安装使用闭环
priority: P1
status: ready
depends_on:
  - ST-004
```

### 故事

作为 quick-sdd 维护者，我希望在角色赋能完成后补齐验证和说明文档，以便这套能力可以被安装、理解、使用，并在后续维护中持续复用。

### 验收标准

- `AC-1`: Given 角色能力增强已经落地，when 验证完成，then 关键文档、安装清单和角色说明与实际实现保持一致。
- `AC-2`: Given 这是一个分阶段推进的 feature，when 验证报告完成，then 能清楚说明已完成内容、残留风险和后续维护建议。
- `AC-3`: Given 未来还会继续演进，when feature 结束，then `codespec` 中保留足够的可追踪信息支撑后续续跑。

### 范围外

- 不要求在本 story 内新增新的外部依赖或发布渠道。
