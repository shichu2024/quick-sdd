---
name: sdd-harness-evolve
description: >
  用于把重复出现的 SDD Harness 失败、审计漂移、评估漏判、用户绕过或路由歧义沉淀为持久 harness 规则。
  不用于一次性 feature 修复、产品代码修复、无证据的流程重写，或在缺少证据时改变 core 不变量。
  输出 evolution log 条目，并按需更新 harness refs、templates、eval cases、profiles 或 registry。
---

# SDD Harness 演进

只有从证据中长出来的规则才进入 harness。重复失败可以变成规则、测试用例、模板变更或 profile 说明。

## 先读

- `codespec/harness/evolution-log.md`
- 最新 audit 和 eval report
- 如果失败来自 feature 验证，读取相关 QA report
- `../sdd-harness/references/evolution-policy.md`

## 演进触发条件

- 同类漂移出现在两次 audit 中。
- 同类路由错误出现在两次 eval 或真实运行中。
- 用户因为路径不清晰或过重而绕过 harness。
- QA 报告指出证据缺口来自 harness 模板。
- 某个 profile 开始像隐藏 core 依赖一样工作。

## 变更目标

| 失败类型 | 变更位置 |
|---|---|
| 路由歧义 | SKILL description 或触发用例 |
| 缺少证据 | 模板或评估用例 |
| 角色漂移 | Core contract 或 registry warning |
| Profile 越界 | Profile contract 和可移植性评估 |
| 重复项目特定风险 | 可选 profile checklist |

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 因一次不顺手就演进 | Harness 频繁抖动 | 要有证据，或先标记为 proposal |
| 只改文字不加测试 | 问题会回归 | 添加评估用例 |
| 把项目事实塞进 core | 可移植性下降 | 项目事实写入可选 profile |
| 改模板不记日志 | 未来 agent 不知道为什么 | 先写 evolution entry |

## 压力测试

每次演进都必须回答：哪里失败了，证据在哪里，改了哪个产物，哪个 eval case 防止回归？

## 下一步

演进后对受影响 case 运行 `sdd-harness-eval`。
