# Quick SDD Skills

这是一个汇总型 skill 仓库，用来发布一套轻量级 SDD（Specification-Driven Development）多 agent 协作技能。

这个仓库不是单一 skill，而是一个可安装的 skill collection：

- 提供主编排 skill：`quick-sdd`
- 提供 1 个存量项目接入 skill：`quick-sdd-bootstrap-existing`
- 提供 5 个独立可发现的角色 skill：`quick-sdd-pm / quick-sdd-ra / quick-sdd-ta / quick-sdd-dev / quick-sdd-qa`
- 提供运行时脚本、模板和参考规约，用于初始化、续跑、权限展开和 QA 回流

## 仓库定位

- 用一套轻量、可恢复、可续跑的 `codespec/` 工作区管理 SDD 产物
- 兼容 Claude / Codex 风格的多 agent 协作
- 把角色职责、状态流转、验证回流和 ACL 约束落到文件与脚本，而不只是提示词约定
- 把“主 skill 编排”和“角色 skill 执行”拆开，便于独立发现、组合安装和 repo-path 发布

## Installable Skills

| Skill | 作用 | 是否可单独安装 |
| --- | --- | --- |
| `quick-sdd` | 初始化 `codespec/`、续跑工作区、驱动主流程和 runtime 脚本 | 是 |
| `quick-sdd-pm` | 路由、派发、续跑、状态推进、吸收 QA 裁决 | 需要同时安装 `quick-sdd` |
| `quick-sdd-bootstrap-existing` | 初始化已有项目、盘点功能与架构、反向生成 baseline SDD 文档 | 需要同时安装 `quick-sdd` |
| `quick-sdd-ra` | 需求分析、范围收敛、`proposal / stories` 生成 | 是 |
| `quick-sdd-ta` | `tasks` 拆解、依赖设计、ACL 规划、`verify` 设计 | 是 |
| `quick-sdd-dev` | 单 task 实现、`verify` 执行、证据回收 | 是 |
| `quick-sdd-qa` | 验收裁决、缺陷回流、`validation-report` 维护 | 是 |

说明：

- `quick-sdd-pm` 会调用 `quick-sdd` 中的 runtime 脚本，所以不建议单独安装。
- 推荐默认安装整组 bundle，而不是只装 `pm`。

## 发布约定

这个仓库已经整理成适合 `repo-path` 安装的结构：

```text
quick-sdd/
  README.md
  install/
    manifest.json
  scripts/
    list_install_targets.py
  skills/
    quick-sdd/
      SKILL.md
      agents/openai.yaml
      templates/
      scripts/
      references/
    quick-sdd-bootstrap-existing/
      SKILL.md
      agents/openai.yaml
      references/
    quick-sdd-pm/
      SKILL.md
      agents/openai.yaml
    quick-sdd-ra/
      SKILL.md
      agents/openai.yaml
    quick-sdd-ta/
      SKILL.md
      agents/openai.yaml
    quick-sdd-dev/
      SKILL.md
      agents/openai.yaml
    quick-sdd-qa/
      SKILL.md
      agents/openai.yaml
```

发布约束：

- 每个可安装 skill 都必须位于 `skills/<skill-name>/`
- 每个 skill 都必须带 `SKILL.md`
- 每个 skill 都建议带 `agents/openai.yaml`
- 角色 skill 如有对主 skill 的脚本依赖，必须在安装清单和 skill 文档里显式声明

## 安装方式

### 1. 安装完整 bundle

推荐安装完整 bundle：`quick-sdd-full`

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/quick-sdd \
  --path skills/quick-sdd-pm \
  --path skills/quick-sdd-bootstrap-existing \
  --path skills/quick-sdd-ra \
  --path skills/quick-sdd-ta \
  --path skills/quick-sdd-dev \
  --path skills/quick-sdd-qa
```

### 2. 只安装主 skill

如果你只想初始化或续跑 `codespec/`，可以只装：

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/quick-sdd
```

### 3. 安装最小编排组合

如果你需要 PM 路由能力，最小建议组合是：

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/quick-sdd \
  --path skills/quick-sdd-pm
```

### 4. 安装已有项目接入组合

如果你要给一个已经存在的项目补齐 `codespec/` 并反向生成现状 SDD 文档，推荐组合是：

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/quick-sdd \
  --path skills/quick-sdd-bootstrap-existing
```

## 机器可读安装清单

仓库级安装清单位于：

- `install/manifest.json`

它定义了：

- 哪些 skill 可安装
- 每个 skill 的 repo-path
- 每个 skill 是否可单独安装
- skill 依赖关系
- 推荐安装 bundle

## 安装辅助脚本

仓库根目录提供：

- `scripts/list_install_targets.py`

这个脚本可以：

- 列出所有可安装 skill
- 列出所有 bundle
- 自动展开 skill 依赖
- 输出某个 bundle 或 skill 对应的 repo-path
- 生成适合 `skill-installer` 的命令示例

示例：

```bash
python scripts/list_install_targets.py
python scripts/list_install_targets.py --bundle quick-sdd-full --repo <owner>/<repo>
python scripts/list_install_targets.py --skill quick-sdd-pm --repo <owner>/<repo>
python scripts/list_install_targets.py --bundle quick-sdd-existing-project --repo <owner>/<repo>
```

## 主流程

`quick-sdd` 负责编排这条主链路：

`pm -> ra -> ta -> dev -> qa`

初始化后生成的项目级 `codespec/` 会集中管理以下产物：

- `proposal.md`
- `stories.md`
- `tasks.md`
- `validation-report.md`
- `runtime/role-policy.yaml`
- `runtime/tools.yaml`
- `runtime/state.json`

## 运行时能力

主 skill 内置 4 个关键脚本原型：

- `init_codespec.py`
  - 初始化 `AGENT.md`、`codespec/` 和 feature 骨架
- `sync_validation_snapshot.py`
  - 把 `validation-report.md` 中最近一次 QA 裁决标准化同步到 `state.json.latest_validation`
- `resume_orchestrator.py`
  - 根据 `state.json` 和最近一次 QA 裁决，推荐下一角色与下一动作
- `resolve_dispatch.py`
  - 解析 `role-policy.yaml + state.json + tasks.md`，展开当前轮次的读写范围

## 推荐使用方式

1. 先使用 `$quick-sdd` 初始化或续跑项目级 `codespec/`
2. 如果项目已经存在但还没有 SDD 文档，优先使用 `$quick-sdd-bootstrap-existing` 生成 baseline SDD 文档
3. 当任务收敛到单一角色后，切换到对应角色 skill
4. 当 QA 更新 `validation-report.md` 后，先运行 `sync_validation_snapshot.py` 同步 `latest_validation`
5. 再运行 `resume_orchestrator.py` 生成下一跳建议
6. 最后运行 `resolve_dispatch.py` 为目标角色展开最小读写范围
