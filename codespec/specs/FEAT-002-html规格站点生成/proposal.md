---
id: FEAT-002
title: HTML 规格站点生成
type: enhancement
priority: P1
depends_on:
  - FEAT-001
status: validating
---

# 提案

## 问题

- Quick SDD 的规格产物目前主要是 Markdown，适合 diff 和协作，但不适合直接作为浏览式规格站点阅读。
- 已有 `generate_overview.py` 雏形只能生成单个 feature 的 `overview.html`，尚未接入初始化流程、AGENTS 开关、项目级索引或存量转换命令。
- 用户希望 HTML 生成默认开启，但可以在 `AGENTS.md` 中关闭自动生成，并保留手动命令触发能力。
- 后续会提供正式 HTML 模板，因此当前机制需要先固定生成入口和扩展点，避免把功能写成一次性脚本。

## 目标

- 初始化或生成新规格文档时，默认同步生成 feature 级 `overview.html` 与项目级 `codespec/index.html`。
- 在 `AGENTS.md` 中提供稳定配置块，可把自动 HTML 生成关闭为 `enabled: false`。
- 提供手动转换存量规格的命令：`python skills/quick-sdd/scripts/generate_overview.py --repo-root . --all`。
- 保持旧入口 `python skills/quick-sdd/scripts/generate_overview.py <feature_dir>` 兼容。
- 用自动化测试覆盖配置开关、手动转换、CLI 和初始化默认生成行为。

## 范围内

- 扩展 `skills/quick-sdd/scripts/generate_overview.py`，支持 repo 级发现、批量生成、项目索引、JSON 输出与 AGENTS 配置读取。
- 扩展 `skills/quick-sdd/scripts/init_codespec.py`，在 scaffold feature 后按配置自动触发 HTML 生成。
- 更新 `AGENTS.md`、`agents.template.md`、`README.template.md`、`codespec/README.md` 与主 `SKILL.md` 的说明。
- 为当前存量 `FEAT-001` 生成 `overview.html`，并生成项目级 `codespec/index.html`。
- 新增 `tests/test_generate_overview.py` 回归测试。

## 范围外

- 不在本轮确定用户后续会提供的最终视觉模板内容。
- 不引入 Web 服务、前端框架或构建系统；当前 HTML 仍是静态文件。
- 不改变 Quick SDD 的角色流程、状态机或 Markdown 规格事实源。

## 风险

- 如果未来模板变量设计变复杂，当前内置模板可能需要进一步拆分为外部模板文件。
- 自动生成会产生派生 HTML 文件，需要团队确认是否作为可提交产物保留。
- `AGENTS.md` 的配置块需要保持稳定，避免不同项目自行改名导致脚本无法识别。

## 待确认问题

- 后续正式 HTML 模板的变量契约、视觉结构和是否需要外部静态资源仍待用户提供。
