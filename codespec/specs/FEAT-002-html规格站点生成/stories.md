# 用户故事

## 索引

| ID | 标题 | 优先级 | 状态 | 依赖 |
|----|------|--------|------|------|
| ST-001 | 自动生成 HTML 规格站点 | P1 | ready | - |
| ST-002 | 手动转换存量规格 | P1 | ready | ST-001 |

## ST-001 自动生成 HTML 规格站点

```yaml
id: ST-001
title: 自动生成 HTML 规格站点
priority: P1
status: ready
depends_on: []
```

### 故事

作为 Quick SDD 维护者，我希望新建规格文档时默认同步生成 HTML 视图，以便规格能直接通过浏览器阅读。

### 验收标准

- `AC-1`: Given `AGENTS.md` 未关闭 HTML 自动生成，when 运行 `init_codespec.py --feature-title ...`，then 新 feature 目录包含 `overview.html`。
- `AC-2`: Given 已生成至少一个 feature overview，when 初始化完成，then `codespec/index.html` 包含项目级规格入口。
- `AC-3`: Given `AGENTS.md` 中 `quick_sdd.html_export.enabled=false`，when 自动生成路径运行，then HTML 生成被跳过且规格 Markdown 仍能生成。

### 范围外

- 不要求在本 story 中实现最终自定义视觉模板。

## ST-002 手动转换存量规格

```yaml
id: ST-002
title: 手动转换存量规格
priority: P1
status: ready
depends_on:
  - ST-001
```

### 故事

作为 Quick SDD 维护者，我希望可以用命令批量转换已有 `codespec/specs/*`，以便历史 feature 也能进入 HTML 规格站点。

### 验收标准

- `AC-1`: Given 已有 feature 规格目录，when 运行 `python skills/quick-sdd/scripts/generate_overview.py --repo-root . --all`，then 每个 feature 生成或刷新 `overview.html`。
- `AC-2`: Given 自动生成已在 `AGENTS.md` 中关闭，when 手动运行转换命令，then 仍然生成 HTML。
- `AC-3`: Given 调用方需要机器读取结果，when 加上 `--json`，then 命令输出包含生成文件列表。

### 范围外

- 不要求手动转换命令启动本地开发服务器。
