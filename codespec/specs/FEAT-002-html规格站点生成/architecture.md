---
id: FEAT-002
title: HTML 规格站点生成
owner_role: ta
status: validating
---

# 架构设计

## 背景

- Markdown 继续作为 Quick SDD 的规格事实源；HTML 是可再生成的阅读视图。
- 现有 `generate_overview.py` 已能从 feature 文档生成单页 HTML，适合作为扩展基础。

## 关键决策

| ID | 决策 | 原因 | 影响 |
|----|------|------|------|
| AD-001 | 将 `generate_overview.py` 扩展为 repo 级站点生成器 | 复用已有 feature 解析和 HTML 渲染逻辑，避免新增并行脚本 | 同时支持旧单 feature 入口与新 `--repo-root --all` 入口 |
| AD-002 | `AGENTS.md` 使用 `QUICK-SDD-HTML` 配置块控制自动生成 | AGENTS 是项目级协作入口，适合承载人工可改的默认策略 | 自动路径尊重 `enabled:false`，手动命令不受影响 |
| AD-003 | `init_codespec.py` 在 scaffold 后调用生成器 | 用户要求“生成规格文档的同时”生成 HTML | 新 feature 默认得到 `overview.html` 和 `codespec/index.html` |
| AD-004 | 项目级入口落在 `codespec/index.html` | 与 `codespec/README.md` 同层，避免污染项目根目录 | 可直接从浏览器打开并导航到各 feature overview |

## 模块与接口

- `skills/quick-sdd/scripts/generate_overview.py`
  - `generate_feature_overview(feature_dir)`
  - `generate_index(repo_root)`
  - `generate_site(repo_root, feature_dirs=None, include_index=True, respect_agents_config=False)`
  - CLI：`<feature_dir>`、`--repo-root --all`、`--feature`、`--index-only`、`--json`
- `skills/quick-sdd/scripts/init_codespec.py`
  - scaffold feature 后调用 `generate_site(..., respect_agents_config=True)`
  - 支持 `--no-html` 作为单次关闭
- `AGENTS.md`
  - 配置块：

```yaml
quick_sdd:
  html_export:
    enabled: true
```

## 风险与验证影响

- HTML 是派生产物，QA 应以 Markdown 和脚本测试为事实源，同时检查生成文件存在性。
- 后续模板落地时，建议先增加模板变量契约测试，再替换内置布局。
