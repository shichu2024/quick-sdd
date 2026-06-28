---
name: quick-sdd
description: >
  用于初始化、续跑和治理轻量级 SDD 工作区，需要生成/维护 `AGENTS.md`、`codespec/`、proposal、stories、architecture、tasks、validation 和 acceptance 产物。
  不用于跨角色直接包办 RA/TA/DEV/QA 的主产物，或跳过 SDD 直接实现代码。
  输出初始化结果、状态更新、权限展开或下一角色派发建议，基于 PM/RA/TA/DEV/TA/QA/RA 主链路。
---

# Quick SDD

使用这个 skill 初始化、恢复和路由一套轻量级规格驱动开发工作区。它是流程入口，不是总代办执行器。

## 核心边界

- 主链路保持为：`pm -> ra -> ta -> dev -> ta -> qa -> ra`。
- `quick-sdd` 与 `pm` 只做初始化、续跑、状态推进、权限展开和派发。
- 一旦下一角色明确且不是 `pm`，当前回合停在派发结果，不继续生成该角色主产物。
- 用户把完整需求交给入口 skill，不等于授权入口 skill 连续完成 `ra / ta / dev / qa` 的主工作。

## 角色与产物

| 角色 | 主责任 | 主产物 |
|------|--------|--------|
| `pm` | 路由、状态、索引、阻塞恢复 | `codespec/README.md`、`runtime/state.json` |
| `ra` | 需求收敛与最终需求验收 | `proposal.md`、`acceptance.md` |
| `ta` | story、架构设计、task 审计 | `stories.md`、`architecture.md`、`tasks.md` 审计记录 |
| `dev` | task 文档与实现 | `tasks.md`、task 授权范围内代码/测试 |
| `qa` | 全链路文档审计与质量裁决 | `validation-report.md` |

## 工作区骨架

初始化项目时创建或维护：

```text
AGENTS.md
codespec/
  README.md
  specs/
    FEAT-001-example/
      proposal.md
      stories.md
      architecture.md
      tasks.md
      validation-report.md
      acceptance.md
  runtime/
    role-policy.yaml
    tools.yaml
    state.json
```

## 先读

- `codespec/runtime/state.json`：唯一续跑入口。
- `codespec/README.md`：feature 索引与状态说明。
- `references/dispatcher-resolution-spec.md`：实现或调试 resolver / resume 逻辑时读取。
- 对应角色 skill：任务已经收敛到单一角色时，优先切换到 `quick-sdd-ra/ta/dev/qa/pm`。

## 内置脚本

- `scripts/init_codespec.py`
  - 初始化 `AGENTS.md`、`codespec/` 与 feature 骨架；默认同时生成 HTML 规格站点。
- `scripts/generate_overview.py`
  - 生成 feature 级 `overview.html` 与项目级 `codespec/index.html`，也可用于转换存量规格文档。
- `scripts/sync_validation_snapshot.py`
  - 把 `validation-report.md` 的最近 QA 裁决同步到 `state.json.latest_validation`。
- `scripts/resume_orchestrator.py`
  - 基于 state、task 状态和 QA 快照推荐下一角色与阶段。
- `scripts/resolve_dispatch.py`
  - 基于 `role-policy.yaml + state.json + tasks.md` 展开读写范围。

## 初始化流程

项目缺少 `codespec/` 时：

1. 运行 `scripts/init_codespec.py --repo-root <项目根目录> [--feature-title <标题>]`，或按 `templates/` 手动创建同等结构。
2. 如果已有旧版 `AGENT.md`，迁移到 `AGENTS.md`；如果已有类似入口文件，合并 Quick SDD 规则，不创建平行规范。
3. 有明确 feature 时，只创建当前阶段需要的骨架，不顺手写满后续角色产物。
4. 初始化时如 `AGENTS.md` 未关闭 `quick_sdd.html_export.enabled`，同步生成 `overview.html` 与 `codespec/index.html`。
5. 初始化后将 `active_phase` 设为 `proposal` 或 `idle`，并把下一跳写进 `resume.next_role / resume.next_action`。

## HTML 规格站点

- 自动生成默认开启；在项目根目录 `AGENTS.md` 的 `quick_sdd.html_export.enabled` 改为 `false` 可关闭自动生成。
- 关闭自动生成后，仍可手动触发：

```bash
python skills/quick-sdd/scripts/generate_overview.py --repo-root <项目根目录> --all
```

- 单个 feature 也可继续使用兼容入口：

```bash
python skills/quick-sdd/scripts/generate_overview.py <feature_dir>
```

## 续跑流程

项目已有 `codespec/` 时：

1. 先读 `runtime/state.json`，再读 `codespec/README.md`。
2. 如果 `active_feature` 为空，选择或创建 feature；如果不为空，优先续跑该 feature。
3. 如果 QA 刚更新 `validation-report.md`，先运行：

```bash
python skills/quick-sdd/scripts/sync_validation_snapshot.py --repo-root <项目根目录> --apply
```

4. 生成下一跳建议：

```bash
python skills/quick-sdd/scripts/resume_orchestrator.py --repo-root <项目根目录>
```

5. 为目标角色展开最小读写范围：

```bash
python skills/quick-sdd/scripts/resolve_dispatch.py --repo-root <项目根目录> --target-role <角色> --mode <read|write>
```

6. 派发目标角色并停下；不要在入口 skill 里代写目标角色产物。

## 状态流转

Feature 主流程（architecture 为条件阶段，由 TA 在 stories 阶段评估）：

```text
idle -> proposal -> stories -> planning -> task_review -> implementing -> validating -> accepting -> done
                            ↘ architecture ↗
```

TA 在 `stories.md` 顶部 frontmatter 写入 `architecture_needed`：

- `architecture_needed: true`：`stories -> architecture -> planning`
- `architecture_needed: false`：`stories -> planning`（跳过 architecture）
- 不确定时默认 `true`（保守原则）

回流规则：

- `validating -> implementing`：实现问题。
- `validating -> task_review`：task 边界、依赖、ACL 或 verify 问题。
- `validating -> architecture`：架构缺口或接口契约不清；若此前跳过 architecture，TA 需补写 `architecture.md` 并把 frontmatter 改为 `architecture_needed: true`。
- `validating -> accepting`：QA 通过或有条件通过，交给 RA 最终验收。
- `accepting -> done`：RA 接受最终结果。
- 任意活动状态可以进入 `blocked`，解除后回到进入阻塞前的活动状态。

## 运行规则

- 把 `codespec/` 视为唯一共享协作工作区。
- 不要假设不同角色有共享隐藏上下文。
- 不要把 task ACL 复制到 state；state 只引用当前 feature、story、task。
- `validation-report.md` 是 QA 质量事实源；`state.json.latest_validation` 是同步快照。
- `acceptance.md` 是 RA 最终需求验收事实源；QA 报告只是它的输入。
- `resolve_dispatch.py` 只消费 state 快照，不直接回退解析 QA 报告。
- 统一闭环顺序：`validation-report.md -> sync_validation_snapshot.py -> state.json.latest_validation -> resume_orchestrator.py -> resolve_dispatch.py -> acceptance.md`。

## 按轮次归档证据

- 将 `check-report/` 等共享输出目录视为工具缓存，不作为长期 SDD 证据。
- 每次正式验证都必须有稳定的轮次目录：
  `codespec/specs/<feature>/validation/round-NNN/`。
- 使用补零且单调递增的轮次 ID：`round-001`、`round-002`、`round-003`。
- 轮次 QA 报告存放在：
  `codespec/specs/<feature>/validation/round-NNN/validation-report.md`。
- 该轮原始证据存放在：
  `codespec/specs/<feature>/validation/round-NNN/evidence/`。
- `codespec/specs/<feature>/validation-report.md` 只保留为给脚本和人工阅读的最新指针/摘要。
  摘要中必须写明当前轮次，并链接到轮次报告和证据目录。
- 工具必须写入共享路径时，在 QA 或 RA 裁决前先把相关输出归档/复制到当前轮次目录。
- 不要把不同轮次的截图、运行报告、相似度报告、覆盖报告或 diff 产物混放在同一个证据目录。
- 如果旧证据是在本规则建立前生成且无法恢复，创建历史轮次 manifest，并明确标注证据缺口。

## 输出要求

- 输出初始化结果、状态更新、派发建议或权限展开结果。
- 明确下一角色、下一动作、建议阶段和需要读取/写入的路径。
- 保持产物精简、可追加、易 diff。
- 优先使用稳定 ID：`FEAT-001`、`ST-001`、`T-001`。
