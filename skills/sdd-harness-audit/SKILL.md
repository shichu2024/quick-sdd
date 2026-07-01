---
name: sdd-harness-audit
description: >
  用于检查仓库的 SDD Harness 就绪度、可移植性、漂移、role-policy 对齐、证据纪律，或已有 `codespec/harness` 产物。
  不用于从零设计新 harness、修改 profile、编写 feature SDD 产物，或替产品 feature 做 QA/RA 裁决。
  输出 `codespec/harness/audits/` 下的审计报告，包含漂移发现、严重级别、证据和回流建议。
---

# SDD Harness Audit

审计当前仓库是否适合作为通用 SDD Harness 的宿主，并找出会破坏可恢复性、角色边界或证据链的漂移。

## 为什么这是一个 Skill

Harness 失败经常不是模型不会做，而是流程事实源漂移：角色文档说一套、权限文件给另一套，状态指向旧 feature，证据只留在临时缓存里。本 skill 让这些问题在真正跑 feature 前暴露出来。

## 先读

- `AGENTS.md`
- `codespec/README.md`
- `codespec/runtime/state.json`
- `codespec/runtime/role-policy.yaml`
- `codespec/harness/registry.yaml`（如果存在）
- `../sdd-harness/references/core-contract.md`
- `../sdd-harness/references/portability-checklist.md`

## 审计项

| 范围 | 检查内容 |
|---|---|
| Core 可移植性 | 没有 profile 时 core 是否仍可运行 |
| 角色归属 | RA/TA/DEV/QA 写权限是否匹配 skill 职责 |
| 状态一致性 | `state.json`、README 激活 feature、latest validation 是否一致 |
| 证据纪律 | validation round 是否有稳定证据路径 |
| 非 ASCII 路径 | 脚本和报告是否会在中文 feature 名上漂移 |
| Profile 卫生 | profile 是否只是可选覆盖层，而不是隐藏依赖 |
| Eval 就绪度 | trigger case、dry-run 场景是否存在，缺失是否显式记录 |

## 输出

创建或更新：

```text
codespec/harness/audits/YYYY-MM-DD-audit.md
```

使用 `../sdd-harness/templates/audit-report.template.md` 的结构。

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 把缺失文档判成产品 bug | 责任人错误 | 归类为 harness 漂移或 SDD 治理缺口 |
| 只相信 `state.json` | 旧状态看起来也像真的 | 交叉核对 README、validation report 和 acceptance |
| 因可选 profile 缺口阻断 core | 误报 blocker | 区分 core blocker 和 profile 建议 |
| 只按文件名审计 | 漏掉契约漂移 | 判断前读取角色 skill 和 policy 正文 |

## 压力测试

如果 `role-policy.yaml` 允许 RA 写 `stories.md`，但 RA skill 明确禁止 RA 写 stories，本审计必须抓出来。

## 下一步

- 有漂移：路由到 `sdd-harness-design` 或 `sdd-harness-build`。
- 同类漂移重复出现：路由到 `sdd-harness-evolve`。

