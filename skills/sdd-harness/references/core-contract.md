# SDD Harness Core 契约

SDD Harness core 必须可移植。它应该能在没有任何领域 profile 的仓库里运行。

## Core 不变量

1. 角色归属固定：`pm -> ra -> ta -> dev -> ta -> qa -> ra`。
2. Core 产物固定：`proposal.md`、`stories.md`、可选 `architecture.md`、`tasks.md`、`validation-report.md`、`acceptance.md`。
3. 状态必须落文件：`codespec/runtime/state.json` 和 `codespec/harness/registry.yaml` 是恢复入口。
4. Task ACL 必须显式：实现工作通过 `read_paths`、`write_paths` 和 `verify` 约束。
5. 必须有证据：没有稳定的测试、日志、截图、review 或已记录的手工证据，就不能说 done。
6. QA 负责质量裁决；RA 负责最终需求验收。
7. Harness eval 评估 harness，不评估产品 feature。
8. Profile 是可选覆盖层，不能改变角色归属或状态机。

## 可移植目录结构

```text
codespec/
  runtime/
    state.json
    role-policy.yaml
  specs/
  harness/
    registry.yaml
    harness-plan.md
    audits/
    runs/
    profiles/
    eval/
      cases/
      runs/
    evolution-log.md
```

## Registry 最小字段

```yaml
version:
core:
  enabled:
  contract_ref:
adapters: []
profiles: []
eval:
  required_before_rollout:
  cases_path:
evolution:
  log_path:
```

## 归属边界

Harness skills 可以创建和维护 `codespec/harness/**`。它们可以建议修改 Quick SDD 产物，但 feature 级角色产物必须由对应 Quick SDD 角色 skill 编写，除非用户明确要求做一次性迁移。
