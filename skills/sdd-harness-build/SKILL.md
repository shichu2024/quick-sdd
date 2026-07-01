---
name: sdd-harness-build
description: >
  用于根据已批准的 harness plan 创建或更新 SDD Harness registry、core 脚手架、模板、adapter 说明、可选 profile 文件和 eval case 文件。
  不用于临场发明 harness 设计、改变 Quick SDD 角色归属、实现产品代码，或编写 feature proposal/stories/tasks/validation/acceptance。
  输出具体的 `codespec/harness/` 产物，以及 plan 明确要求的新 `skills/sdd-harness-*` 文件。
---

# SDD Harness 生成

根据已批准的设计落地 harness 产物。每个生成文件都要能追溯到 plan，且默认只写 `codespec/harness/**`。

## 先读

- `codespec/harness/harness-plan.md` 或指定 plan
- `../sdd-harness/references/core-contract.md`
- `../sdd-harness/references/profile-contract.md`
- `../sdd-harness/templates/` 下相关模板

## 生成目标

| 目标 | 默认路径 |
|---|---|
| 注册表（Registry） | `codespec/harness/registry.yaml` |
| 核心计划（Core plan） | `codespec/harness/harness-plan.md` |
| 可选 profile | `codespec/harness/profiles/<profile>.md` |
| 评估用例（Eval case） | `codespec/harness/eval/cases/*.yaml` |
| 评估报告（Eval report） | `codespec/harness/eval/runs/<run-id>/report.md` |
| 演进日志 | `codespec/harness/evolution-log.md` |

## 生成规则

- 先创建核心（core）产物。
- Profile 必须声明 `optional: true`。
- 除非 plan 明确要求 core contract 变更，否则不要编辑 `quick-sdd-*` skill。
- 不要覆盖已有 harness 产物；默认追加版本或保留旧内容，除非用户明确要求替换。
- 生成文件要易 diff，尽量贴合模板。

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 只凭聊天上下文生成 | Harness 不可复现 | 必须先有计划产物（plan artifact） |
| 混放 core 和 profile 内容 | 可移植性下降 | Profile 内容写入 `profiles/` |
| 静默改 role policy | SDD 路由被破坏 | 把 policy 变更记录为显式漂移修复 |
| 漏生成评估用例 | 无法证明 harness 有效 | 至少生成触发和 dry-run 用例 |

## 压力测试

生成后，一个新 agent 只读 `registry.yaml`、core contract 和 plan，就应该知道如何跑审计和评估，而不依赖隐藏聊天上下文。

## 下一步

声明 harness 可用于普通 feature 前，先运行 `sdd-harness-eval`。
