---
name: sdd-harness-profile
description: >
  用于创建、更新或审计可选的 SDD Harness 质量 profile，在不改变可移植 core 的前提下补充项目、领域或技术栈特定检查。
  不用于必需 core 行为、Quick SDD 角色归属、产品实现，或 feature 最终验收。
  输出 `codespec/harness/profiles/` 下的可选 profile 文件，包含触发边界、附加检查、verify 建议和可移植性限制。
---

# SDD Harness Profile（可选质量画像）

Profile 是可选覆盖层。它提高本地质量，但不能成为 SDD Harness core 的依赖。

## 为什么这是一个 Skill

项目知识很有价值，但一旦塞进 core，系统就难以复用。本 skill 把本地经验放在可删除、可替换的覆盖层里。

## 先读

- `../sdd-harness/references/profile-contract.md`
- `../sdd-harness/templates/profile.template.md`
- `codespec/harness/registry.yaml`（如果存在）
- 相关项目文档或 feature 样本

## 允许补充

- 项目术语和模块地图
- 额外检查清单
- 额外触发示例和非触发示例
- 推荐 verify 命令
- 常见失败模式
- 风险分类
- 指向本地权威文档的链接

## 禁止补充

- 改变 core 状态机
- 让 profile 直接编写 RA/TA/DEV/QA 产物
- 让 profile 成为普通 SDD 执行的必需条件
- 把项目特定假设藏进 core 模板

## 输出

创建或更新：

```text
codespec/harness/profiles/<profile-name>.md
```

frontmatter 必须包含 `optional: true`。

## 常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 把 profile 叫“领域技能包” | 听起来像必需依赖 | 使用“可选质量 profile”说法 |
| 重复 core 规则 | core 和 profile 漂移 | 引用 core contract，不复制 |
| 添加泛泛建议 | 增加噪声 | 只写项目特定证据标准 |
| 不写非触发示例 | profile 过度触发 | 至少写两条 not-for case |

## 压力测试

删除 profile 后，如果 core harness 仍能跑通普通 feature，说明 profile 边界健康。

## 下一步

Profile 创建后，用 `sdd-harness-build` 注册，再用 `sdd-harness-eval` 测试路由。
