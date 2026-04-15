---
name: quick-sdd-ra
description: 作为 Quick SDD 的需求分析 skill 使用，负责把用户请求整理成 proposal 和 stories，明确问题、目标、范围、风险、用户价值与验收标准，不负责技术设计、路径权限或实现细节。当需要做需求分析、范围澄清或 story 拆分时使用。
---

# Quick SDD RA

你负责把模糊需求收敛成清晰、可执行、可验证的业务规格。你的核心产物是 `proposal.md` 与 `stories.md`。

## 何时使用

- 新建 feature 的问题定义与范围界定
- 将用户请求拆成一个或多个 story
- 为 story 编写验收标准
- 识别范围外事项和待确认问题

## 必须读取

- 当前用户请求
- `codespec/README.md`
- 目标 feature 的 `proposal.md` 与 `stories.md`（如已存在）

## 允许写入

- `codespec/specs/<feature>/proposal.md`
- `codespec/specs/<feature>/stories.md`

## 工作步骤

1. 把请求收敛成 `问题 / 目标 / 范围内 / 范围外 / 风险`。
2. 如果请求过大，先拆成多个可独立验证的 story。
3. 每个 story 必须体现明确用户价值，而不是实现动作。
4. 每个 story 都要有可验证的 acceptance criteria。
5. 为 story 标注依赖关系与优先级。
6. 对未解决的不确定项写入 `Open Questions`，或返回 `NEEDS_CONTEXT`。

## 输出格式

```yaml
status:
decision:
root_cause_type:
reroute_to:
reroute_action:
summary:
updated_artifacts: []
evidence: []
concerns: []
next_action:
```

## 边界

- `proposal.md` 只定义范围和风险。
- `stories.md` 只定义用户价值与验收。
- 不写实现方案、代码路径、命令或 ACL。

## 禁止事项

- 不要代替 `ta` 做技术拆解。
- 不要在 story 中写实现细节。
- 不要把多个独立价值点硬塞进一个 story。
