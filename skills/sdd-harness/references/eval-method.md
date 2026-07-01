# SDD Harness 评估方法

用可复现 case 评估 harness 行为。

## Case 类型

1. `should_trigger`：用户请求 harness 审计、设计、生成、评估或演进。
2. `should_not_trigger`：用户请求普通 feature 实现或产品 QA。
3. `dry_run`：模拟一个最小普通 feature 走过 SDD core。
4. `ab_artifact`：比较 baseline 产物和启用 harness 后的产物质量。
5. `portability`：关闭 profiles，确认 core 仍可运行。
6. `drift_regression`：重放一个已修复的漂移问题。

## 评分维度

| 维度 | 通过信号 |
|---|---|
| 路由（Routing） | 选择正确 skill，没有绕过角色 |
| 可移植性（Portability） | core 在无 profile 时成功 |
| 证据（Evidence） | 输出中包含稳定证据路径 |
| ACL | 写范围保持显式 |
| 回流（Reroute） | 失败能正确回流到 PM/RA/TA/DEV/QA |
| Profile 卫生 | profile 建议可选且边界清楚 |

## 最小评估轮次

- 6 个 should-trigger case
- 6 个 should-not-trigger case
- 1 个 portability dry-run
- 如果已有历史漂移，至少 1 个 drift regression

## 结果判定

- `pass`：可以进入普通 feature 使用。
- `conditional_pass`：可用，但必须列出 caveat。
- `fail`：rollout 前必须回到 design/build/evolve。
