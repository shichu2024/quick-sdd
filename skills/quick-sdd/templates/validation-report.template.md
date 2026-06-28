# 验证报告

> 最新摘要：本文档只汇总当前 feature 的最新 QA 裁决。
> 当前轮次：`round-001`
> 轮次报告：`validation/round-001/validation-report.md`
> 权威证据目录：`validation/round-001/evidence/`
> `check-report/...` 等共享工具输出路径仅作缓存，可能被后续轮次覆盖。

## 功能总结

- 功能 ID：{{feature_id}}
- 当前轮次状态（status）：
- 总体裁决（decision）：
- 总体建议回流角色（reroute_to）：
- 总体摘要（summary）：
  - 无
- 已验证故事：
  - {{story_id}}
- 已审计文档：
  - `proposal.md`
  - `stories.md`
  - `architecture.md`
  - `tasks.md`
- 未解决问题：
  - 无
- 说明：
  - QA 裁决是 RA 最终验收的输入；最终需求验收写入 `acceptance.md`。

## {{story_id}}

- 当前轮次状态（status）：
- 验证裁决（decision）：
- 根因分类（root_cause_type）：
- 建议回流角色（reroute_to）：
- 建议回流动作（reroute_action）：
  - 无
- 摘要（summary）：
  - 无
- 已检查验收标准：
  - `AC-1`
  - `AC-2`
- 文档审计：
  - `proposal.md`：
  - `stories.md`：
  - `architecture.md`：
  - `tasks.md`：
- 证据：
  - 命令：
    - `npm test`
  - 工具：
    - `e2e-start`
  - 变更文件：
    - `src/...`
- 缺陷：
  - 无
- 剩余风险：
  - 无

## 追踪摘要

枚举参考：

- status：`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`
- decision：`pass | conditional_pass | fail`
- root_cause_type：`implementation | task_boundary | dependency | requirement_gap | architecture_gap | evidence_gap | risk_acceptance | none`
- reroute_to：`dev | ta | ra | pm`

| 故事 | 验收标准 | 任务 | 验证裁决（decision） | 根因分类 | 建议回流角色 |
|------|------------|-------|--------------------|----------|----------------|
| {{story_id}} | AC-1, AC-2 | {{task_id}} | pass | none | ra |
