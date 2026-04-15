---
name: quick-sdd-bootstrap-existing
description: 为一个已经存在、但还没有完整 quick-sdd 规格工作区的项目初始化 `AGENT.md` 和 `codespec/`，盘点现有功能、技术栈、模块边界与架构约束，并输出可直接衔接后续 Quick SDD 流程的 baseline proposal、stories、tasks、validation 文档。当需要把存量项目接入 SDD、把现有系统反向整理成规格文档，或为后续需求开发补齐现状基线时使用。
---

# Quick SDD Bootstrap Existing

你负责把一个“已经在运行的项目”接入 Quick SDD。你的目标不是发明新需求，而是把现有项目的功能、架构和边界反向整理成可以继续演进的 SDD 文档基线。

## 何时使用

- 项目已经有代码，但没有 `codespec/`
- 项目已经有 `codespec/`，但缺少对现有系统能力的基线文档
- 需要在开始新需求前，先把现有项目整理成可续跑的 SDD 规格
- 需要把项目功能、模块边界、技术栈和关键架构约束沉淀下来

## 安装依赖

- 这个 skill 依赖同仓安装的 `quick-sdd`
- 原因是它会复用 `quick-sdd` 的模板、runtime 约定和初始化脚本
- repo-path 安装时，推荐至少安装 `quick-sdd + quick-sdd-bootstrap-existing`

## 必须读取

- 项目根目录 `README`、包管理文件和主要配置文件
- 入口文件、路由、控制器、页面、服务层、数据模型、测试目录
- 如已存在：`AGENT.md`、`codespec/README.md`、`codespec/runtime/state.json`
- `../quick-sdd/templates/`
- `references/bootstrap-existing-project.md`

## 优先使用的脚本

- `../quick-sdd/scripts/init_codespec.py`

## 工作步骤

1. 判断当前项目是否已有 `codespec/`；若没有，优先运行 `../quick-sdd/scripts/init_codespec.py --repo-root <项目根目录>`
2. 扫描项目的技术栈、构建方式、入口点、目录边界、核心模块和外部依赖
3. 从现有代码和 README 中提炼“当前已经存在的用户能力”，不要把假设功能写进 baseline
4. 先产出项目级总览：更新 `AGENT.md` 和 `codespec/README.md`，补充项目目标、模块地图、关键约束和活跃 feature 索引
5. 按能力域或关键用户旅程拆分 feature；小项目可先产出 1 个 baseline feature，中大型项目建议先覆盖 3-7 个核心 feature
6. 对每个 feature 生成 `proposal.md` 和 `stories.md`，强调“当前系统已具备什么能力、边界是什么、有哪些已知限制”
7. 如当前没有明确的后续开发请求，`tasks.md` 和 `validation-report.md` 以 baseline 占位方式初始化，给后续 TA / QA 留出可续写入口
8. 完成后将 `state.json` 调整为可续跑状态：默认由 `pm` 接手下一步，而不是把项目停在半初始化状态
9. 如果发现现有项目结构混乱、功能边界无法可靠归类，返回 `NEEDS_CONTEXT`，并明确指出需要补充的项目背景

## 输出要求

- `AGENT.md`
- `codespec/README.md`
- 至少 1 个 feature 目录，包含：
  - `proposal.md`
  - `stories.md`
  - `tasks.md`
  - `validation-report.md`
- `codespec/runtime/state.json` 保持为可续跑状态

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

## 关键约束

- 这是“现状基线化”，不是“重新设计系统”
- 只记录现有代码和文档能支撑的功能与架构，不臆造未来能力
- `proposal.md` 要描述当前 feature 的问题域、目标用户价值和边界
- `stories.md` 要描述当前系统已提供的行为与验收，不写未来实现方案
- `tasks.md` 如暂无开发任务，可以保留 baseline 占位说明，但不要伪造实现任务
- `validation-report.md` 如暂无系统性验收，可写成 baseline 初始化状态，但要让 QA 后续能直接续写

## 禁止事项

- 不要把“猜测中的功能”写成已存在能力
- 不要只根据目录名机械生成 feature，必须结合实际代码职责和用户价值
- 不要覆盖用户已有的 `codespec/` 产物；如已有文档，优先补充和对齐
- 不要把架构分析写成大而空的概念图，必须落回当前仓库中的模块和边界
