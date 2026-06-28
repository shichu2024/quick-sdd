# 任务清单

> Owner: `dev`。Task 文档定义执行计划、ACL、依赖和验证方式；TA 只审计边界与架构一致性，不替 DEV 代写任务。

## 索引

| ID | Story | 标题 | 状态 | 依赖 | 负责人 |
|----|-------|-------|--------|------------|-------|
| 待 DEV 编写 | {{story_id}} |  | draft | - | dev |

## 编写说明

DEV 在 `planning` 阶段把本文件改写为真实任务。每个真实 task 必须使用 `## T-xxx ...` 二级标题，并在标题下放置 YAML 元数据块。

示例：

````markdown
  ## T-001 {{task_title}}

  ```yaml
  id: T-001
  story_id: {{story_id}}
  title: {{task_title}}
  owner_role: dev
  status: todo
  review:
    reviewer_role: ta
    status: pending
    notes: ""
  depends_on: []
  read_paths:
    - src/**
  write_paths:
    - src/**
  verify:
    - type: command
      value: npm test
    - type: manual
      value: 确认验收标准已满足
  ```
````

### 目标

<!-- 用 1-3 条描述这个 task 的工程结果。 -->

- 

### 架构依据

<!-- 引用 architecture.md 中的设计决策或约束。 -->

- `AD-001`

### 交付物

<!-- 列出具体输出或可观察结果。 -->

- 

### TA 审计记录

<!-- TA 审计 task 边界、依赖、ACL、verify 和架构一致性。 -->

- 状态：pending
- 意见：

### 备注

<!-- 可选。补充实现边界、限制条件或复用提示。 -->

- `read_paths` 和 `write_paths` 使用 glob 路径模式。
- 不要在这里重复完整的验收标准。
- 验证产物、截图、diff 和报告应归档到 `validation/round-NNN/evidence/`；共享 `check-report/` 只作为工具输出缓存。
