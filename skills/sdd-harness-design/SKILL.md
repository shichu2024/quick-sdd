---
name: sdd-harness-design
description: >
  用于设计可移植 SDD Harness core、仓库 adapter、评估策略、可选 profile 边界，或基于审计结果编写 harness plan。
  不用于安装生成文件、编写具体 feature SDD 产物、实现代码，或把领域 profile 变成必需项。
  输出 `codespec/harness/harness-plan.md` 或 `codespec/harness/plans/<name>.md`，包含决策、取舍和 rollout 门禁。
---

# SDD Harness 设计

先设计，再生成。核心（core）必须保持通用；仓库和运行时差异放到适配层（adapter），可选质量增强放到画像（profile）。

## 先读

- `../sdd-harness/references/core-contract.md`
- `../sdd-harness/references/profile-contract.md`
- 最新的 `codespec/harness/audits/*.md`（如果存在）
- `AGENTS.md`
- `codespec/README.md`

## 设计轴

| 设计轴 | 要回答的问题 |
|---|---|
| 核心（Core） | 哪些 SDD 不变量在所有仓库都必须成立 |
| 适配层（Adapter） | 当前仓库/运行时需要哪些映射才能执行 |
| 画像（Profile） | 哪些可选质量覆盖层有价值 |
| 评估（Eval） | 用哪些触发、dry-run、A/B 用例证明有效 |
| 发布门禁（Rollout） | 进入普通 feature 使用前需要通过哪些门禁 |
| 演进（Evolution） | 哪些失败模式会反哺 harness 规则 |

## 模式选择

| 模式 | 适用场景 |
|---|---|
| Pipeline（流水线） | 工作必须严格按阶段推进 |
| Producer-Reviewer（产出-审查） | 一个角色产出，另一个角色审查或验证 |
| Supervisor（监督路由） | PM 需要根据状态和裁决动态路由 |
| Fan-out/Fan-in（分发-汇总） | 多个审计项或评估用例可以并行 |
| Hybrid（混合） | 不同阶段需要不同模式 |

## 输出

使用 `../sdd-harness/templates/harness-plan.template.md`。

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 围绕单一项目类型设计核心 | 核心不再可移植 | 项目知识放入 profile |
| 用 profile 修补核心歧义 | 形成隐藏依赖 | 强化 core contract |
| 跳过评估设计 | Harness 质量只能靠体感 | 现在就定义触发和 dry-run 用例 |
| 把适配层当成角色 | 责任边界混乱 | Adapter 只映射运行时/平台差异 |

## 压力测试

把 plan 中所有 profile 删除。如果 harness 不能再跑通一个普通 Quick SDD feature，说明设计没有守住可移植性。

## 下一步

Plan 通过后进入 `sdd-harness-build`。需要可选覆盖层时进入 `sdd-harness-profile`。
