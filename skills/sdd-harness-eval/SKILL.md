---
name: sdd-harness-eval
description: >
  用于测试 SDD Harness 是否路由正确、保持可移植、提升产物质量，或避免 trigger/profile 漂移。
  不用于评估模型 benchmark 分数、做产品 QA 裁决、接受 feature 风险，或替代 `quick-sdd-qa`。
  输出 `codespec/harness/eval/runs/<run-id>/` 下的评估轮次，包含 trigger、dry-run、A/B 和可移植性结果。
---

# SDD Harness 评估

评估 harness 本身，而不是评估产品 feature。目标是证明路由、可移植性、证据纪律和质量提升。

## 先读

- `codespec/harness/registry.yaml`
- `../sdd-harness/references/eval-method.md`
- `codespec/harness/eval/cases/` 下的 eval case
- 相关 audit 或 plan 文件

## 评估类型

| 类型 | 目的 |
|---|---|
| 触发评估（Trigger eval） | 检查 should-trigger 和 should-not-trigger 路由 |
| 干跑（Dry-run） | 模拟一个普通 feature 走通 core SDD |
| A/B 产物评估 | 对比启用 harness 前后的产物质量 |
| 可移植性评估 | 确认 core 在无 profile 时仍可运行 |
| 漂移回归评估 | 重放已修复的历史漂移 case |

## 输出

使用 `../sdd-harness/templates/eval-report.template.md`，写入：

```text
codespec/harness/eval/runs/YYYY-MM-DD-<name>/report.md
```

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 把评估当成产品 QA | 裁决权错位 | 产品 QA 仍属于 `quick-sdd-qa` |
| 只测 should-trigger | 容易过度触发 | 必须包含 should-not-trigger |
| 靠感觉比较质量 | 没有可复核信号 | 使用 rubric 维度和证据 |
| 可移植性评估依赖 profile | core 评估无效 | 关闭 profiles 后再跑 |

## 压力测试

合格评估必须包含至少一个“profile 会有帮助，但 core 不依赖 profile 也能成功”的 case。

## 下一步

通过后，harness 可以进入普通 Quick SDD 工作。失败时根据根因回流到 `sdd-harness-design`、`sdd-harness-build` 或 `sdd-harness-evolve`。
