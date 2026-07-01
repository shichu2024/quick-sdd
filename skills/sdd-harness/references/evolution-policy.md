# SDD Harness 演进策略

演进的目标是把证据转成持久 harness 变更，而不是把一次性的偏好写进规则。

## 证据门槛

至少满足一项：

- 同类失败出现两次或更多。
- 单次失败阻断了恢复、角色归属、证据链或最终验收。
- 用户明确因为 harness 路径不清晰或过重而绕过它。

## 必需条目

每条 evolution log 必须包含：

```yaml
date:
source:
failure:
evidence:
root_cause:
changed_artifacts: []
new_eval_cases: []
rollout_note:
```

## 变更优先级

1. 新增或调整 eval case。
2. 修复模板或 registry。
3. 澄清 skill 路由。
4. 更新可选 profile。
5. 只有当失败跨项目成立时，才修改 core contract。

