---
name: sdd-harness
description: >
  用于创建、续跑、审计、设计、生成、评估、演进，或跨多个 feature 运行围绕 Quick SDD 的通用可移植 SDD Harness 系统。
  不用于直接编写 feature 的 proposal/stories/architecture/tasks/validation/acceptance、实现产品代码，或把领域 profile 作为必需依赖。
  输出路由决策、最小交接包，以及 `codespec/harness/` 下的 SDD Harness 产物位置。
---

# SDD Harness

这是通用可移植 SDD Harness 的总入口。它在 Quick SDD 外围增加审计、设计、生成、评估和演进闭环，但不替代 Quick SDD 的角色链路。

## 为什么这是一个 Skill

Agent 很容易把“改进流程”写成散落在聊天里的提示词。本 skill 把流程改进固化为可携带的 harness：明确的产物、角色边界、证据门禁和可恢复的 registry。

## 核心契约

需要确认不变量时读取 `references/core-contract.md`。简版规则：

- Core 必须可移植：角色、产物、状态机、ACL、证据、QA 回流、RA 验收、评估和演进都属于通用层。
- Profile 只是可选覆盖层：可以补充检查清单和示例，但不能改变 core 状态机或角色归属。
- Harness 工作不替代 `quick-sdd-ra/ta/dev/qa/pm`；它只准备、审计或增强这些角色工作的环境。

## 路由

| 用户意图 | 使用 |
|---|---|
| “把一个大需求拆成多个 feature 并逐个走完 SDD” | `sdd-harness-run` |
| “检查 SDD harness / 漂移 / 可复用性” | `sdd-harness-audit` |
| “设计一套 harness / 架构怎么放” | `sdd-harness-design` |
| “生成/安装 harness 产物” | `sdd-harness-build` |
| “生成可选项目画像/profile” | `sdd-harness-profile` |
| “测试 harness 是否有效” | `sdd-harness-eval` |
| “把反复失败沉淀成规则” | `sdd-harness-evolve` |
| “继续单个普通 feature 开发” | `quick-sdd` 或对应 Quick SDD 角色 skill |

## 先读

- `AGENTS.md`
- `codespec/runtime/state.json`（如果存在）
- `codespec/README.md`（如果存在）
- `codespec/harness/registry.yaml`（如果存在）
- `references/core-contract.md`

## 输出格式

```yaml
status:
decision:
target_skill:
reason:
owned_artifacts: []
read_first: []
write_targets: []
next_action:
```

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 把 profile 当成必需项 | Core 失去可移植性 | profile 必须可选、可删除 |
| 让 harness 编写 feature 产物 | 角色归属坍塌 | 路由给 Quick SDD 角色 skill |
| 只把流程状态留在聊天里 | 压缩或换线程后无法恢复 | 写入 `codespec/harness/` 产物 |
| 写成一个超大 `SKILL.md` | 后续 agent 不会按需加载细节 | 契约、模板、评估方法放到 refs/templates |

## 压力测试

合格的 SDD Harness 应该能复制到一个新仓库，在没有任何 profile 的情况下，仍然把一个普通 feature 跑完 proposal、stories、tasks、validation、acceptance 和证据门禁。

## 相关 Skill

- `quick-sdd`：初始化和续跑 feature 级 SDD 工作区。
- `quick-sdd-pm`：负责具体 feature 的路由与运行态状态。
- `writing-skills`：修改这些 skill 文件时使用。
