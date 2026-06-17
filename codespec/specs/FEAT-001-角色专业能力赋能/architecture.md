---
id: FEAT-001
title: 角色专业能力赋能
owner_role: ta
status: draft
---

# 架构设计

## 背景

- Quick SDD 通过 `codespec/` 保存跨角色共享事实，通过独立 role skill 保存角色行为约束。
- 当前调整把文档责任从“前置角色代写后置产物”改成责任链：RA 写 proposal，TA 写 stories/architecture 并审 task，DEV 写 tasks/实现，QA 审全链路，RA 在 QA 之后做最终需求验收。

## 关键决策

| ID | 决策 | 原因 | 影响 |
|----|------|------|------|
| AD-001 | 新增 `architecture.md` 作为 feature 级技术设计事实源 | 原流程缺少独立架构设计文档，架构约束容易散落在 story 或 task 中 | DEV 的 task 需要引用架构决策，QA 审计时检查 architecture 与 tasks 是否一致 |
| AD-002 | `tasks.md` 主责任人改为 DEV，TA 负责审计 | task 是执行计划和 ACL 载体，更接近实现责任；但需要 TA 防止边界漂移 | runtime 允许 DEV 写 tasks.md，TA 可写审计记录 |
| AD-003 | resolver 支持 optional task 范围 | planning 阶段 DEV 需要写 tasks.md，但尚未有 active task | 无 active task 时 DEV 只能写 tasks.md；有 active task 时再展开代码写范围 |
| AD-004 | 新增 `acceptance.md` 和 `accepting` 阶段 | QA 的质量裁决不能替代 RA 对原始需求和用户价值的最终判断 | QA pass/conditional_pass 后路由到 RA；RA 写最终接受、要求修改或拒绝结论 |

## 模块与接口

- `skills/quick-sdd/templates/architecture.template.md`：新 feature 的架构文档模板。
- `skills/quick-sdd/scripts/init_codespec.py`：初始化 feature 时生成 `architecture.md`。
- `skills/quick-sdd/templates/acceptance.template.md`：新 feature 的 RA 最终验收模板。
- `codespec/runtime/role-policy.yaml` 与模板：定义 RA/TA/DEV/QA 的新读写边界。
- `skills/quick-sdd/scripts/resolve_dispatch.py`：解释 optional resolver。
- `skills/quick-sdd/scripts/resume_orchestrator.py`：按新阶段推荐下一角色；QA 通过后进入 `accepting` 并派给 RA。

## 风险与验证影响

- DEV 写自己的 task 可能扩大实现范围；由 TA 的 `task_review` 阶段和 QA 全链路审计兜底。
- 新阶段 `architecture`、`task_review` 与 `accepting` 需要安装者理解；README、AGENT 模板和 role skill 必须同步说明。
- 旧 feature 没有 architecture 时，QA 审计会发现文档缺口；新模板和初始化脚本应保证后续 feature 默认具备该文档。
- 旧 feature 没有 acceptance 时，RA 最终验收缺少落盘位置；新模板和初始化脚本应保证后续 feature 默认具备该文档。
