---
name: sdd-harness-run
description: >
  用于把一个大需求拆成多个 feature，并编排这些 feature 逐个或按依赖顺序走完 Quick SDD 全流程，最后生成跨 feature 汇总验收。
  不用于代替 RA/TA/DEV/QA 编写单个 feature 的主产物、绕过用户授权自动无限推进、或把未验收 feature 伪装成整体完成。
  输出 `codespec/harness/runs/<epic-id>/` 下的总体计划、运行状态、feature 映射、依赖图、执行记录和汇总验收。
---

# SDD Harness 运行

这是 SDD Harness 的跨 feature 运行编排层。它处理“一个大需求拆成多个 feature 并逐个走完 SDD”的场景，但不接管单个 feature 的角色产物。

## 为什么这是一个 Skill

单个 Quick SDD feature 的边界清楚，但大需求经常需要拆成多个 feature、管理依赖、追踪每个 feature 的验收状态，并在最后判断整体目标是否满足。本 skill 把这件事落成可恢复的总体运行，而不是靠聊天上下文记进度。

## 先读

- `AGENTS.md`
- `codespec/README.md`
- `codespec/runtime/state.json`
- `../sdd-harness/references/core-contract.md`
- `../sdd-harness/references/epic-run-contract.md`
- `codespec/harness/registry.yaml`（如果存在）

## 运行产物

每个大需求使用一个目录：

```text
codespec/harness/runs/EPIC-001-短标题/
  epic-plan.md
  run-state.yaml
  feature-map.md
  dependency-graph.md
  execution-log.md
  aggregate-acceptance.md
  handoffs/
  evidence/
```

## 工作流

1. `需求接收`：读取大需求，确认目标、非目标、约束、期望 feature 数量和自动推进授权。
2. `审计门禁`：必要时先路由 `sdd-harness-audit`，确认 SDD 工作区可运行。
3. `总体规划`：把大需求拆成 N 个 feature，写入 `epic-plan.md`、`feature-map.md` 和 `dependency-graph.md`。
4. `Feature 派发`：按依赖顺序逐个派发给 `quick-sdd-pm`，再由 PM 路由 RA/TA/DEV/QA/RA。
5. `Feature 闭环检查`：每个 feature 必须有 `validation-report.md` 和 `acceptance.md`，否则不能标记为整体完成。
6. `汇总评估`：运行 `sdd-harness-eval` 或最小完整性检查，确认所有 feature 覆盖原始目标。
7. `汇总验收`：写 `aggregate-acceptance.md`，汇总整体通过、条件通过、失败或需补 feature。

## 自动推进规则

- 用户明确要求“自动拆分并一一走完”时，可以连续推进；但遇到需求歧义、权限扩大、QA fail、RA rejected 或跨 feature 冲突必须停下。
- 未明确授权自动推进时，每完成一个 feature gate 要回报下一步。
- 任一 feature 的最终验收仍以该 feature 的 `acceptance.md` 为准；汇总验收只能汇总，不覆盖单 feature RA 决策。

## 输出格式

```yaml
status:
epic_id:
decision:
current_feature:
feature_status: []
updated_artifacts: []
blocked_by: []
next_action:
```

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 直接在 run skill 里写 feature proposal | 绕过 RA | 创建 feature 后派发给 `quick-sdd-pm/ra` |
| 只拆 feature 不写依赖图 | 执行顺序靠记忆 | 写 `dependency-graph.md` |
| 某个 feature 没验收就整体 pass | 假完成 | 汇总验收必须引用每个 `acceptance.md` |
| QA fail 后继续下一个 feature | 缺陷扩散 | 先按 QA reroute 修复或显式记录阻塞 |
| 把自动推进理解成无条件推进 | 风险失控 | 遇到 gate 失败、权限扩大、需求歧义必须停 |

## 压力测试

输入“把需求拆成 5 个 feature 并全部走完”。合格行为是创建总体运行目录，拆出 5 个 feature，按依赖逐个进入 Quick SDD 主链路，每个 feature 有独立验收，最后再写汇总验收。

## 下一步

- 需要先搭建或修复 harness：路由 `sdd-harness-audit/design/build`。
- Feature 已拆好：逐个派发 `quick-sdd-pm`。
- 所有 feature 已验收：生成或更新 `aggregate-acceptance.md`。
