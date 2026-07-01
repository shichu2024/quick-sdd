# 可移植性检查清单

审计、设计和评估时使用这份清单。

- Core 可以在没有 profile 的情况下初始化。
- Core 不命名具体产品模块、包名或业务领域。
- Profile 声明 `optional: true`。
- 角色归属与 Quick SDD skills 一致。
- 动态写路径来自 task ACL，而不是聊天上下文。
- 证据路径稳定，并存放在 `codespec/` 下。
- 只凭文件状态即可恢复流程。
- 非 ASCII feature 名不会破坏发现或同步。
- Adapter 说明只描述运行时差异，不承担角色职责。
- Eval case 覆盖误触发防护。

