# SDD Harness 总体运行契约

总体运行用来承载一个大需求拆成多个 feature 后的跨 feature 编排状态。它属于 `codespec/harness/**`，不替代任何单 feature 的 Quick SDD 产物。

## 不变量

1. 总体运行可以拆分、排序、派发和汇总 feature，但不能代写单个 feature 的 RA/TA/DEV/QA 主产物。
2. 每个 feature 的完成事实源仍然是该 feature 的 `validation-report.md` 和 `acceptance.md`。
3. `aggregate-acceptance.md` 只做整体汇总和跨 feature 风险判断，不能覆盖单 feature RA 裁决。
4. 自动推进必须受 gate 约束：需求歧义、QA fail、RA rejected、权限扩大、依赖冲突都必须停止并回报。
5. 总体运行状态必须落文件，不能只存在聊天上下文。

## 目录结构

```text
codespec/harness/runs/<epic-id>/
  epic-plan.md
  run-state.yaml
  feature-map.md
  dependency-graph.md
  execution-log.md
  aggregate-acceptance.md
  handoffs/
  evidence/
```

## run-state 最小字段

```yaml
epic_id:
objective:
requested_feature_count:
execution_mode: sequential
auto_continue_authorized:
current_feature:
features:
  - id:
    title:
    status:
    depends_on: []
    codespec_path:
    validation_ref:
    acceptance_ref:
aggregate:
  decision:
  open_risks: []
  missing_coverage: []
```

## Feature 状态

- `planned`：已拆分，尚未启动 Quick SDD。
- `proposal` / `stories` / `architecture` / `planning` / `task_review` / `implementing` / `validating` / `accepting`：跟随 Quick SDD 阶段。
- `accepted`：feature 的 RA 已接受。
- `blocked`：等待用户、修复、依赖或裁决。
- `rejected`：feature 的 RA 拒绝或需求不再成立。

## 整体验收判定

- `accepted`：所有必需 feature 均 accepted，且原始目标覆盖完整。
- `conditional_pass`：主目标达成，但存在明确剩余风险或后续 feature。
- `blocked`：至少一个必需 feature 未完成或证据不足。
- `rejected`：整体目标不成立，或关键 feature 被拒绝且无替代方案。
