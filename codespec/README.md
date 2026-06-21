# CodeSpec

## 概览

<!-- 简要说明项目是什么，以及为什么需要在这里使用 CodeSpec。 -->

- 项目：quick-sdd
- 负责人：
- 当前激活的功能：FEAT-002-html规格站点生成
- 最后更新时间：2026-06-18T01:24:40+08:00

## 术语

- `Feature`：一个自包含的产品能力，存放在 `codespec/specs/<feature>/` 下
- `Story`：带有明确验收标准的用户价值切片
- `Architecture`：TA 维护的架构设计、技术边界和关键决策记录
- `Task`：用于路由、归属和执行的工程单元
- `Validation`：对一个或多个 story 的验证结果
- `Acceptance`：RA 对整个需求和最终结果的最终验收决定
- `Traceability`：story、验收标准、task 与验证结果之间的映射关系
- `ACL`：角色或 task 允许读取与写入的路径范围

## 流程

- `pm -> ra -> ta -> dev -> ta -> qa -> ra`
- 共享存储，隔离角色上下文
- `pm` 负责路由与运行时状态
- 项目根目录 `AGENTS.md` 负责协作约束，`codespec/` 负责规格与状态

## Feature 索引

| ID | 标题 | 状态 | 优先级 | 路径 |
|----|------|------|--------|------|
| FEAT-001 | 角色专业能力赋能 | done | P1 | specs/FEAT-001-角色专业能力赋能/ |
| FEAT-002 | HTML 规格站点生成 | validating | P1 | specs/FEAT-002-html规格站点生成/ |

## HTML 规格站点

- 项目级入口：`codespec/index.html`
- Feature 级入口：`codespec/specs/<feature>/overview.html`
- 自动生成默认开启，可在项目根目录 `AGENTS.md` 的 `quick_sdd.html_export.enabled` 中关闭。
- 手动转换存量规格：

```bash
python skills/quick-sdd/scripts/generate_overview.py --repo-root . --all
```

## 状态说明

### Feature 状态

- `proposal`：正在定义问题和范围
- `stories`：TA 正在定义用户价值切片和验收标准
- `architecture`：TA 正在补齐架构设计、技术边界和关键决策
- `planning`：DEV 正在编写 task 文档、ACL、依赖和验证方式
- `task_review`：TA 正在审计 DEV 的 task 文档
- `implementing`：一个或多个 task 正在执行
- `validating`：QA 正在审计全部文档和验证结果
- `accepting`：RA 正在对整个需求和最终结果做最终验收
- `done`：feature 已验收完成
- `blocked`：feature 受依赖或决策阻塞

### 运行时状态

- `idle`：当前没有激活的 feature 或 task，等待初始化、恢复或下一次派发

## 状态流转

- `idle -> proposal` 表示开始一个新 feature
- `idle -> implementing / validating` 表示恢复已有流程
- `proposal -> stories -> architecture -> planning -> task_review -> implementing -> validating -> accepting -> done`
- 任意活动状态都可以进入 `blocked`
- `blocked` 解除后回到阻塞前状态
- `validating -> implementing` 表示验证失败且根因为实现问题
- `validating -> task_review` 表示验证失败且根因为 task 边界、依赖、ACL 或 verify 问题
- `validating -> architecture` 表示验证失败且根因为架构设计或接口契约缺口
- `validating -> accepting` 表示 QA 通过或有条件通过后交给 RA 做最终需求验收
- `accepting -> done` 表示 RA 接受最终结果

## ID 规则

- `Feature` 使用 `FEAT-001` 这类稳定编号
- `Story` 使用 `ST-001` 这类稳定编号
- `Task` 使用 `T-001` 这类稳定编号
- 新编号通过扫描现有产物递增生成，不复用旧编号
