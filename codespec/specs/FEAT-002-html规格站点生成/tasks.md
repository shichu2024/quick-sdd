# 任务清单

## 索引

| ID | Story | 标题 | 状态 | 依赖 | 负责人 |
|----|-------|------|------|------|--------|
| T-001 | ST-001 | 扩展 HTML 生成器为站点生成器 | done | - | dev |
| T-002 | ST-001 | 接入初始化自动生成与 AGENTS 开关 | done | T-001 | dev |
| T-003 | ST-002 | 支持存量转换命令与回归测试 | done | T-002 | dev |

## 阶段 A 生成链路

## T-001 扩展 HTML 生成器为站点生成器

```yaml
id: T-001
story_id: ST-001
title: 扩展 HTML 生成器为站点生成器
owner_role: dev
status: done
depends_on: []
read_paths:
  - skills/quick-sdd/scripts/generate_overview.py
  - codespec/specs/**
write_paths:
  - skills/quick-sdd/scripts/generate_overview.py
  - codespec/index.html
  - codespec/specs/**/overview.html
verify:
  - type: command
    value: python -m py_compile skills/quick-sdd/scripts/generate_overview.py
```

### 目标

- 支持发现 `codespec/specs/FEAT-*`。
- 支持生成 feature overview 和项目级 `codespec/index.html`。
- 保留旧单 feature 命令入口。

### 交付物

- `generate_site`、`generate_index`、`discover_feature_dirs` 等生成入口。
- `codespec/index.html`。

## T-002 接入初始化自动生成与 AGENTS 开关

```yaml
id: T-002
story_id: ST-001
title: 接入初始化自动生成与 AGENTS 开关
owner_role: dev
status: done
depends_on:
  - T-001
read_paths:
  - AGENTS.md
  - skills/quick-sdd/templates/agents.template.md
  - skills/quick-sdd/scripts/init_codespec.py
write_paths:
  - AGENTS.md
  - skills/quick-sdd/templates/agents.template.md
  - skills/quick-sdd/scripts/init_codespec.py
verify:
  - type: command
    value: python -m unittest discover -s tests
```

### 目标

- `AGENTS.md` 默认开启自动 HTML 生成，可手动改为 `enabled:false`。
- `init_codespec.py` scaffold feature 后按配置触发 HTML 生成。
- 提供 `--no-html` 单次关闭。

### 交付物

- `QUICK-SDD-HTML` 配置块。
- `init_codespec.py` 自动生成接入。

## T-003 支持存量转换命令与回归测试

```yaml
id: T-003
story_id: ST-002
title: 支持存量转换命令与回归测试
owner_role: dev
status: done
depends_on:
  - T-002
read_paths:
  - skills/quick-sdd/scripts/generate_overview.py
  - tests/**
write_paths:
  - tests/test_generate_overview.py
  - skills/quick-sdd/SKILL.md
  - skills/quick-sdd/templates/README.template.md
  - codespec/README.md
verify:
  - type: command
    value: python -m unittest discover -s tests
  - type: command
    value: python skills/quick-sdd/scripts/generate_overview.py --repo-root . --all --json
```

### 目标

- 提供 `--repo-root . --all` 存量转换命令。
- `--json` 输出生成文件列表。
- 测试覆盖自动禁用、手动覆盖禁用、CLI 和初始化默认生成。

### 交付物

- `tests/test_generate_overview.py`。
- 更新后的使用说明。
