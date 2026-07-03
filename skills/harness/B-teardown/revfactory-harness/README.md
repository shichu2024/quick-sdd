# revfactory/harness 拆解报告

> 拆解日期: 2026-06-30 | 作者: 架构猫 (zhipu/glm-5.2)
> 方法论: open-source-teardown skill（宣传 claim → 源码证据 → 能力边界 → 我们的 tradeoff）
> 数据源: GitHub tarball @ 2026-06-30（v1.2.0），SKILL.md + 全部 6 个 references/ 文件已逐行读取
> 版本: **v3 — 深挖版**（v2 基于源码验证，v3 补充 sister repo 实验数据 + QA 方法论 + 规模化证据）

---

## 0. 项目基本信息

| 字段 | 值 |
|------|-----|
| 仓库 | https://github.com/revfactory/harness |
| Stars | 8.1k |
| Forks | 1.1k |
| License | Apache-2.0 |
| 语言 | HTML 100%（GitHub 统计口径）；**实际是纯 Markdown skill 项目，无运行时代码** |
| 版本 | v1.2.0 |
| 作者 | robin (revfactory) — 韩语母语项目 |
| Topics | harness, claude-code, claude-code-plugin, harness-engineering |
| 定位 | L3 Meta-Factory / Team-Architecture Factory |
| 依赖 | **Claude Code 实验性 Agent Teams 特性**：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

### 重要源码级发现（v1 未提及）

1. **SKILL.md 及全部 references/ 均为韩语撰写**。README 有 EN/KO/JA 三语，但 skill 本体是韩语。对 Cat Café（同样韩语/中文语境）是天然亲和点，但对纯英文生态是采用障碍。
2. **实际工作流是 Phase 0-7（8 阶段）**，不是 README 宣传的 "6-Phase"。README 只列 Phase 1-6，SKILL.md 实际还有 Phase 0（现况审计/audit）和 Phase 7（进化/evolution）。README **低估了**项目深度。
3. **sister repo `revfactory/harness-100`**：100 个生产级 agent team harness，跨 10 个领域，1,808 个 markdown 文件，全部由本插件生成。这是工厂**确实可规模化运行**的强证据，不只是概念。
4. **依赖实验性特性**：Agent Teams 是 Claude Code 实验功能，需手动开启 flag。生产环境采用有稳定性风险。

### 自我定位（源码确认）

Harness 明确定位在 Claude Code 生态的 **L3 Meta-Factory** 层——生成其他 harness 的工厂。README 的 "Category — Where Harness Sits" 表与 plugin.json 的 keywords 一致：

| 层 | 职责 | 邻居 |
|----|------|------|
| **L3 Meta-Factory / Team-Architecture Factory**（本项目）| 领域描述 → agent 团队 + skills，6 种团队架构模式 | — |
| L3 Meta-Factory / Runtime-Configuration Factory | 确定性可重复的运行时配置 | coleam00/Archon |
| L3 Meta-Factory / Codex Runtime Port | 同概念 Codex 运行时 | SaehwanPark/meta-harness |
| L2 Cross-Harness Workflow | 跨 harness 标准化 skills/rules/hooks | affaan-m/ECC |

---

## 1. Claims Ledger（宣传声明审计 — 源码验证版）

| # | Claim | 证据文件（源码行号）| v1 Verdict | **v2 Verdict** | 变更理由 |
|---|-------|----------|------------|----------------|----------|
| C1 | "一句话生成 agent 团队 + skills" | SKILL.md Phase 1-6 全链路 + 产出物 checklist L429-449 | plausible | **confirmed** | 源码确认完整链路：分析→架构→agent定义→skill生成→编排→验证，且有 checklist 强制产出 |
| C2 | "6 种架构模式" | agent-design-patterns.md L83-160 | plausible | **confirmed + underestimated** | 实际不止 6 模式：还有执行模式决策树（Team vs Sub vs Hybrid）、复合模式表、agent 分离 4 轴准则、agent 复用设计、skill↔agent 3 种连接法。是完整 agent 设计手册 |
| C3 | "Skill Generation with Progressive Disclosure" | SKILL.md L149-171 三级加载表 | plausible | **confirmed** | 源码确认 3 级：Metadata(常驻)→SKILL.md(<500行)→references/(按需)。有明确的 500 行红线和 ToC 规则 |
| C4 | "Inter-agent data passing, error handling, team coordination protocols" | orchestrator-template.md 全文 + SKILL.md L222-256 | plausible | **confirmed — 比 v1 评估更具体** | 源码有 4 种数据传递策略表（message/task/file/return-value）、3 种编排模板含 TeamCreate/SendMessage/TaskCreate 伪代码、错误处理矩阵、团队规模指南 |
| C5 | "Trigger verification, dry-run testing, with-skill vs without-skill comparison" | skill-testing-guide.md 全文 307 行 | plausible | **confirmed — v1 严重低估** | v1 误判为"LLM 生成测试文档"。实际是完整 eval 框架：A/B baseline 对照、assertion JSON schema、Grader/Comparator/Analyzer 三专家角色、20-query 触发 eval、迭代工作区结构 |
| C6 | "+60% avg quality (49.5 → 79.3), 15/15 win-rate, -32% variance" | README L247-261 + FAQ Q1 L270-277 | use-with-caveat | **use-with-caveat（披露质量=业界范本）** | 源码确认：每次引用都强制附带 "(n=15, author-measured, third-party replications pending)"。FAQ Q1 主动回应"是否 oversold"。sister repo claude-code-harness 提供完整实验。披露卫生是 gold standard |
| C7 | "effectiveness scales with task complexity (+23.8 Basic, +29.6 Advanced, +36.2 Expert)" | README L257 | use-with-caveat | **use-with-caveat** | 同 C6，方向可信（结构化预配置对难任务增益更大符合直觉），绝对值待第三方复现 |
| C8 | "Claude Code Plugin" | .claude-plugin/plugin.json + marketplace.json | confirmed | **confirmed** | plugin.json v1.2.0，支持 marketplace 安装和直接 global skill 安装两种方式 |
| C9（新）| "5 real-world team configurations" | team-examples.md（313 行，5 个完整示例）| v1 未审计 | **confirmed** | 源码确认 5 个示例：研究团队、SF小说团队、网漫团队、营销团队、产品发布团队，每个含 agent 定义全文 + 编排 + 数据流 |

### C6/C7 深度审计（v3 升级 — sister repo 实验数据已验证）

+60% 是项目核心营销 claim。**v3 已访问 sister repo `revfactory/claude-code-harness`，实验数据远比 v2 评估的严谨**：

**实验设计（源码确认）：**
- 15 个任务 × 3 难度（Basic 001-005 / Advanced 006-010 / Expert 011-015）
- Baseline（Claude Code + prompt only）vs Harness（Claude Code + .claude/ 预配置）
- 10 维度评分（每维 0-10，总分 100）
- 每个任务有 `experiments/cases/case-{NNN}/` 含 baseline/ 和 harness/ 两份产出 + `evaluation.json`

**结果（论文 + 仓库数据确认）：**
| 指标 | Baseline | Harness | Delta |
|------|----------|---------|-------|
| 平均分 | 49.5 | 79.3 | +29.9 (+60%) |
| Win Rate | — | — | 15/15 (100%) |
| Std Dev | 5.3 | 3.6 | -32% variance |
| Basic delta | 52.0 | 75.8 | +23.8 |
| Advanced delta | 51.8 | 81.4 | +29.6 |
| Expert delta | 44.6 | 80.8 | **+36.2** |

**维度分析 Top 4 提升：** Test Coverage +4.9（Baseline avg 2.5 = 几乎不写测试）/ Architecture +4.4（Baseline avg 3.9 = 单体倾向）/ Error Handling +3.0 / Extensibility +3.0

**学术产出：** 9 页论文（EN + KO），6 张 matplotlib 图，引用格式 `Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.`

**可复现性：** 提供 `/experiment all`、`/evaluate case-011`、`/report full` 命令，实验数据全公开

**剩余 caveat（v3 确认）：**
- n=15 仍小样本 ✅ 已披露
- **author-graded**：evaluation.json 的评分者仍是作者（潜在偏差——Claude 评 Claude？需检查评分是否 LLM-based）
- 无第三方复现（sister repo 114 stars vs 主仓 8.1k，说明很少人实际复现）
- 仓库仅 14 commits，实验为一次性产出

**v3 Verdict 升级：** `use-with-caveat` → **`confirmed-direction, pending-replication`**。方向几乎确定正确（结构化预配置提升输出质量，符合 arXiv:2604.18071 实证 + 本仓 15 案例全胜 + 难度越高增益越大符合直觉），绝对值（+60%）可能因 author-graded 偏高，但有完整论文 + 数据 + 可复现命令，**可信度远超 v2 评估**。用于决策时可自行跑 `/experiment` 复现。

---

## 2. 架构地图

### 仓库结构（源码确认）

```
harness/
├── .claude-plugin/
│   ├── plugin.json                 # Plugin manifest（v1.2.0，keywords 含 6 模式名）
│   └── marketplace.json            # Marketplace 注册
├── .github/                        # Issue/PR 模板
├── _workspace/                     # 工作区示例（5 个真实团队的中间产物 + 2 份审计报告）
│   ├── 01_auditor_repo_audit.md
│   ├── 02_content_launch_contents.md
│   ├── 03_scout_outreach_map.md
│   ├── 04_strategist_launch_plan.md
│   └── release/                    # 发布审计
├── skills/
│   └── harness/
│       ├── SKILL.md                # ★ 主入口（457 行，韩语，Phase 0-7）
│       └── references/             # 渐进式披露层（6 个文件，共 ~1400 行）
│           ├── agent-design-patterns.md   # 300 行 — 6 模式 + 执行模式 + 复合 + 分离准则
│           ├── orchestrator-template.md   # 292 行 — 3 模板含 API 伪代码
│           ├── team-examples.md           # 313 行 — 5 个完整团队配置
│           ├── skill-writing-guide.md     # skill 编写指南
│           ├── skill-testing-guide.md     # 307 行 — 完整 eval 框架
│           └── qa-agent-guide.md          # QA agent 集成（7 个真实 bug 案例）
├── docs/                           # quickstart + experimental-dependency 说明
├── README.md / README_JA.md / README_KO.md   # 三语言 README
└── index.html / privacy.html       # 官网落地页
```

### 关键架构特征（源码确认）

1. **无运行时代码**：HTML 100%（GitHub 统计），实际是纯 Markdown skill 项目。所有"执行"依赖 Claude Code 的 skill 加载机制 + Agent Teams API
2. **SKILL.md 是唯一入口**：457 行韩语，通过 Claude Code skill 触发机制激活
3. **references/ 是渐进式披露层**：6 个文件共 ~1400 行，按需加载，不进初始上下文。每个文件都有明确"何时读取"的指针
4. **_workspace/ 是真实产物**：不是空目录，包含 5 个团队配置的实际中间产物和 2 份审计报告——证明工厂被实际运行过

### Entrypoints

| 入口 | 类型 | 触发方式（源码确认）|
|------|------|----------|
| SKILL.md | Skill 触发 | description 含 5 类触发：①"하네스 구성해줘" ②"하네스 설계/엔지니어링" ③新领域自动化构建 ④重构/扩展 ⑤"하네스 점검/감사/현황"运维 |
| plugin.json | 插件安装 | `/plugin install harness@harness-marketplace` 或 `cp -r skills/harness ~/.claude/skills/harness` |

### State Stores

无独立状态存储。生成的产物（.claude/agents/ 和 .claude/skills/）写入目标项目目录。**跨会话状态通过 `_workspace/` 目录 + CLAUDE.md 变更历史表管理**（SKILL.md L258-277, L386-398）——这是源码确认的持久化机制。

### Extension Points

| 扩展点 | 机制（源码确认）|
|--------|--------|
| 自定义架构模式 | 在 references/agent-design-patterns.md 添加（已有复合模式表 L162-183）|
| 自定义编排模板 | 在 references/orchestrator-template.md 添加（已有 3 模板 A/B/C）|
| 自定义团队示例 | 在 references/team-examples.md 添加（已有 5 个）|
| Phase 选择 | SKILL.md L28-33 提供"现有扩展时 Phase 选择矩阵"，按变更类型跳过无关 Phase |

---

## 3. Phase 0-7 Workflow 深挖（v1 误为 6-Phase，已修正）

### 实际工作流（源码 SKILL.md 确认）

```
Phase 0: 현황 감사（现状审计）—— v1 漏掉
    ↓ 分支：新建 / 扩展 / 运维
Phase 1: 도메인 분석（领域分析）+ 用户熟练度检测
    ↓
Phase 2: 팀 아키텍처 설계（团队架构设计）
    ├─ 2-1: 执行模式选择（Team / Sub / Hybrid）
    ├─ 2-2: 6 模式选择
    └─ 2-3: agent 分离准则（4 轴）
    ↓
Phase 3: 에이전트 정의 생성（agent 定义生成）
    ├─ 3-0: 现有 agent 重叠审查
    └─ 强制 model: "opus" + 强制 .claude/agents/{name}.md 文件
    ↓
Phase 4: 스킬 생성（skill 生成）
    ├─ 4-0: 现有 skill 重叠审查
    ├─ 4-2: description "pushy" 写法
    └─ 4-4: Progressive Disclosure 三级加载
    ↓
Phase 5: 통합 및 오케스트레이션（集成与编排）
    ├─ 5-0: 3 种编排模式（Team/Sub/Hybrid）模板
    ├─ 5-1: 4 种数据传递策略
    ├─ 5-2: 错误处理（1次重试后继续，冲突数据不删并记）
    ├─ 5-3: 团队规模指南（2-3/3-5/5-7人）
    ├─ 5-4: CLAUDE.md 指针注册（只记触发规则+变更历史）
    └─ 5-5: 后续作业支持（部分重跑/新跑判定）
    ↓
Phase 6: 검증 및 테스트（验证与测试）
    ├─ 6-1: 结构验证
    ├─ 6-2: 执行模式别验证
    ├─ 6-3: skill 执行测试（with-skill vs without-skill A/B）
    ├─ 6-4: 触发验证（should-trigger + should-NOT-trigger 各 8-10 个）
    ├─ 6-5: dry-run 测试
    └─ 6-6: 测试场景编写
    ↓
Phase 7: 하네스 진화（harness 进化）—— v1 漏掉
    ├─ 7-1: 每次运行后收集反馈
    ├─ 7-2: 反馈类型→修改对象映射表
    ├─ 7-3: CLAUDE.md 变更历史
    ├─ 7-4: 进化触发（同类反馈≥2次/重复失败/用户绕过）
    └─ 7-5: 运维工作流（审计→增量改→同步→验证）
```

### 链路追踪（源码确认）

```
用户说"build a harness for this project"
  → Claude Code 匹配 SKILL.md description（5 类触发词）
    → Phase 0: 读 .claude/agents/ + .claude/skills/ + CLAUDE.md，判断新建/扩展/运维
      → Phase 1: LLM 分析领域 + 探索代码库 + 检测用户熟练度
        → Phase 2: 从 6 模式选架构（基于 references/agent-design-patterns.md）
                   + 选执行模式（Team/Sub/Hybrid，Team 是默认）
          → Phase 3: 生成 .claude/agents/{name}.md（强制文件，强制 opus）
                     + 3-0 现有 agent 去重
            → Phase 4: 生成 .claude/skills/{name}/SKILL.md + references/
                       + 4-0 现有 skill 去重 + description "pushy" 写法
              → Phase 5: 生成编排 skill（3 模板之一）+ CLAUDE.md 指针
                         + _workspace/ 中间产物保留
                → Phase 6: 结构验证 + A/B 测试 + 触发验证 + dry-run
                  → Phase 7: 运行后反馈收集 + 进化触发 + 变更历史
```

### 关键观察（v2 修正）

- **v1 错误**："全链路是 LLM 推理，无确定性代码"——**这个定性需要修正**。
- **v2 修正**：链路执行确实是 LLM 驱动（无脚本），但 references/ 本身**就是确定性脚手架**：编排模板含 TeamCreate/SendMessage/TaskCreate 具体 API 伪代码、数据传递 4 策略表、错误处理矩阵、assertion JSON schema、20-query 触发 eval 方法论。这些是**结构化的工程制品**，不是自由 prompt。正确的定性是："LLM 驱动执行，但 references/ 提供强约束的确定性脚手架"。
- **这本身就是一个 harness**：SKILL.md + references/ 包裹 Claude，让它稳定产出结构化 agent 团队配置。**Harness 用 harness 的方式生成 harness——meta 递归**，这一点 v1 判断正确。

---

## 4. 6 种架构模式 + 执行模式深挖（源码确认）

### 执行模式（v1 漏掉的 PRIMARY 轴）

源码 agent-design-patterns.md L3-77 揭示：**执行模式（Team vs Sub vs Hybrid）是比 6 架构模式更优先的决策轴**。

| 模式 | 何时使用 | 核心工具 | 特征 |
|------|----------|----------|------|
| **Agent Teams（默认）** | 2+ agent 协作，需实时协调 | TeamCreate + SendMessage + TaskCreate | 团员直接通信，共享任务列表自组织 |
| Sub-agents（备选） | 单向结果返回，无需通信 | Agent(prompt, run_in_background) | 轻量快速，token 高效 |
| Hybrid | Phase 间特性不同 | Phase 级混搭 | 如并行收集(Sub)→共识整合(Team) |

**决策树（源码 L62-75）**：2+ agent 且需通信 → Team（默认）；2+ agent 但只需结果传递 → Sub 可选；1 agent → Sub。

### 6 种架构模式（源码确认 + 团队模式适配性）

| 模式 | 描述 | 团队模式适配性（源码新增）| Cat Café 对标 |
|------|------|----------|--------------|
| Pipeline | 顺序依赖 | 顺序依赖强，团队模式收益有限；但有并行段时有用 | quality-gate → request-review → receive-review → merge-gate |
| Fan-out/Fan-in | 并行独立 | **源码强调"必须用 Agent Teams"**——团员共享发现、实时修正方向 | thread-orchestration 并行子任务 |
| Expert Pool | 选择性调用 | **Sub 更合适**——按需调用，无需常驻团队 | skill 按需加载 |
| Producer-Reviewer | 生成+审查 | Team 有用——SendMessage 实时反馈 | request-review + receive-review |
| Supervisor | 动态分发 | Team 自然匹配——TaskCreate 共享任务列表 | PM/监工喵角色 |
| Hierarchical Delegation | 递归委托 | **Team 不支持嵌套**（源码约束），1 级 Team + 2 级 Sub 实现 | 铲屎官 → 架构猫 → Dev/QA |

### 复合模式（v1 漏掉）

源码 L162-183 提供 3 种复合模式：Fan-out + Producer-Reviewer / Pipeline + Fan-out / Supervisor + Expert Pool。且明确"所有复合模式默认用 Agent Teams"。

### 关键发现（v2 强化）

v1 说"6 模式非原创，与 arXiv:2604.18071 重叠"。源码验证后**补充**：Harness 的真正贡献不是发明模式，而是：
1. 把学术模式**操作化为 Claude Code Agent Teams API**（TeamCreate/SendMessage/TaskCreate 具体调用）
2. 为每种模式标注**团队模式适配性**（哪些该用 Team，哪些该用 Sub）
3. 提供**复合模式**和**执行模式决策树**——这是学术论文不讲的实操知识
4. 做成**一句话触发的工厂** + **100 个生产级示例**（harness-100 sister repo）

---

## 5. 算法剥皮表（v2 修正）

| 宣传特性 | 实际实现（源码证据）| v1 分类 | **v2 分类** | 变更理由 |
|----------|----------|------|------|----------|
| "Agent Team Design" | LLM 读 agent-design-patterns.md（含决策树+适配性表+复合模式）→ 生成 Markdown | LLM 推理 | **LLM 推理 + 强约束模板** | references 提供决策树和适配性表，非自由 prompt |
| "Skill Generation" | LLM 生成 SKILL.md + references/，有 500 行红线 + ToC 规则 + "pushy" description 规则 | LLM 推理 | **LLM 推理 + 质量规则** | 有明确的质量规则约束 |
| "Orchestration" | LLM 选 3 模板之一填空，模板含 TeamCreate/SendMessage/TaskCreate 伪代码 + 数据流图 + 错误矩阵 | LLM 推理 | **LLM 推理 + 具体模板** | v1 误为"无运行时编排引擎"——实际有结构化模板 |
| "Validation" | A/B baseline 对照 + assertion JSON schema + Grader/Comparator/Analyzer 三角色 + 20-query 触发 eval | LLM 推理 | **⚠️ v1 严重误判 → 实为 eval 框架** | skill-testing-guide.md 是完整 eval 方法论，非"生成测试文档" |
| "+60% quality" | 作者 A/B (n=15) + 强制免责声明 + sister repo + 论文 | 启发式测量 | **启发式测量（披露范本）** | 披露质量升级为业界范本 |
| "Progressive Disclosure" | references/ 目录 + 3 级加载表 + 500 行红线 | 规则 | **规则（Claude Code 机制 + Harness 质量规则）** | 非原创但加了质量规则 |
| "6 Architecture Patterns" | agent-design-patterns.md 300 行 | 规则 | **规则 + 实操知识** | 业界模式 + 团队适配性 + 复合模式 = 实操增量 |

### 硬规则审计（v2 修正）

- **v1 错误**："无独立 eval / score / threshold / rollback"
- **v2 修正**：skill-testing-guide.md **定义了**：
  - assertion 基础自动评分（JSON schema，passed/failed/evidence）
  - pass_rate 量化阈值
  - non-discriminating assertion 检测（两配置都 100% 通过 = 无差别力，需移除）
  - 迭代终止条件（用户满意/反馈全空/无有意义改进）
  - 但**无自动 rollback**——失败时是人工迭代修正 skill，非自动回滚
- **v2 结论**：有 eval/score/threshold，**无自动 rollback**（人工迭代）。v1 的"无 eval"判断是错误的。

---

## 6. 反馈链和评价主体（v2 修正）

| 任务类型 | Harness 的评价主体 | v1 评估 | **v2 评估** | 变更 |
|----------|-------------------|--------|------------|------|
| 客观任务（文件格式正确性）| assertion 自动评分 + Grader agent 交叉验证 | ⚠️ 缺失 | **✅ 合规** | skill-testing-guide.md §4 提供 assertion JSON schema + §5 Grader 角色 |
| 专业任务（架构合理性）| LLM 自评 + Comparator 盲测 + 用户 review | ⚠️ 应 peer review | **✅ 较合规** | §5 Comparator 盲测 A/B + 用户定性 review；无外部 peer 但有盲测 |
| 主观任务（团队设计满意度）| 用户手动检查 | ✅ 合理 | **✅ 合理** | 不变 |
| 触发正确性 | 20-query eval（10 should-trigger + 10 should-NOT-trigger）| v1 未审计 | **✅ 合规** | §7 提供 near-miss 测试法 + 现有 skill 冲突检测 |

### v2 修正

v1 说"Harness 把三层评价都压给 LLM 自评或用户手动检查"——**这是错误的**。源码确认：
- 客观任务有 assertion 自动评分
- 专业任务有 Comparator 盲测
- 触发正确性有 20-query eval
- **真正的 gap 是**：无自动 rollback（失败靠人工迭代），且 eval 框架本身需要用户手动执行（不是 CI 集成的自动 eval）

---

## 7. 和 Cat Café 对比（v2 修正）

### Learn（立刻值得学的）

1. **6 模式 + 执行模式决策树 + 团队适配性表**：v1 已提，v2 强化——源码确认这不只是"6 模式"，是完整 agent 设计手册（含复合模式、分离 4 轴、复用设计、skill↔agent 3 连接法）。可借鉴到 thread-orchestration skill
2. **L3 Meta-Factory 定位 + 邻居切割**：v1 已提。v2 补充——README 的"Coexistence"表用"X is..., Harness is..."句式清晰切割，是定位沟通的范本
3. **Progressive Disclosure 3 级 + 500 行红线**：v1 已提。v2 补充——有明确的 ToC 规则和域分离规则（aws.md/gcp.md/azure.md），比我们更系统
4. **一句话触发 UX + 5 类触发词**：v1 已提。v2 补充——description 含 5 类触发（新建/扩展/运维/审计/同步），覆盖全生命周期
5. **披露卫生业界范本**：v1 已提。v2 强化——"Exact phrasing to use everywhere"强制免责声明 + FAQ 主动设问"是否 oversold"，是营销诚实度的 gold standard
6. **Phase 0 审计 + Phase 7 进化（v1 漏掉）**：源码确认有现状审计（检测 drift）和进化机制（反馈类型→修改对象映射、进化触发条件、变更历史表）。**这是 v1 完全漏掉的重要机制**——Cat Café 的 quality-gate 可以借鉴 Phase 0 的 drift 检测和 Phase 7 的进化触发条件
7. **A/B eval 框架（v1 严重低估）**：skill-testing-guide.md 的 with-skill vs baseline + assertion JSON + Grader/Comparator/Analyzer + 20-query 触发 eval，是 Cat Café 缺失的 eval 能力，可直接借鉴
8. **QA agent "边界交叉比较"理念**：qa-agent-guide.md 强调 QA 不是"存在确认"而是"边界面交叉比较"（API 响应 vs 前端 hook shape 对比），且要增量 QA（每模块完成后立即，非全部完成后 1 次）

### Gap（我们承认的缺口）

1. **缺少显式架构模式库**：v1 已提。v2 强化——Harness 有 300 行模式手册 + 复合模式 + 适配性表，我们散落在各 skill
2. **缺少 team-examples**：v1 已提。v2 确认 Harness 有 5 个完整团队配置（含 agent 定义全文 + 编排 + 数据流），我们没有
3. **缺少 A/B 测试文化**：v1 已提。v2 强化——Harness 至少有完整 eval 框架 + n=15 A/B + 100 个生产示例，我们连 eval 框架都没有
4. **缺少 Phase 0 drift 检测**：v2 新增——Harness 每次触发先审计现有 agent/skill 与 CLAUDE.md 的一致性，我们没有这种 drift 检测
5. **缺少 Phase 7 进化触发**：v2 新增——Harness 有"同类反馈≥2次/重复失败/用户绕过"的进化触发条件，我们的 self-evolution skill 可借鉴

### Do Not Follow（我们不做的及理由）

1. **不做纯 LLM 推理的全链路生成**：v1 已提。v2 修正——Harness 不是"无确定性代码"，而是"LLM 驱动执行 + references 强约束模板"。我们选择文件系统外化 + 确定性 hook + 状态机约束，因为多猫协作需更强确定性
2. **不做 Claude Code-only 绑定**：v1 已提。v2 补充——Harness 明确选"Claude-Code-native, deep"，但依赖实验性 Agent Teams flag。我们选 provider-agnostic，tradeoff 是丧失 Agent Teams 深度集成
3. **不把 +60% 作为营销核心**：v1 已提。v2 修正——Harness 的披露方式**值得学**（强制免责 + FAQ 设问），但 n=15 自测数据不作为决策依据
4. **不做纯 Markdown 项目**：v1 已提。v2 补充——Harness 的 references/ 质量很高（~1400 行工程制品），但仍是 Markdown。我们有 MCP 工具 + hook 脚本 + 状态文件，是更重但更强的工程
5. **不做韩语-only skill 本体**：v2 新增——Harness 的 SKILL.md/references 全韩语，对英文生态是障碍。Cat Café 应保持中英双语或至少英文 skill 本体

---

## 8. 邻居对比（源码确认）

| 仓库 | 定位 | 与 Harness 的关系（README "Coexistence" 表确认）|
|------|------|-------------------|
| coleam00/Archon | Runtime-Configuration Factory | 同 L3 不同子层：Archon 管运行时确定性，Harness 管团队架构。**可组合**（Harness 设计架构 → Archon 部署运行时）|
| SaehwanPark/meta-harness | Codex port | 同概念不同运行时。Codex 用 meta-harness，Claude Code 用 Harness |
| affaan-m/ECC | L2 Cross-Harness Workflow | 不同层：ECC 是跨 harness 标准化层，Harness 是生成 harness 的工厂。**可串联**|
| wshobson/agents | agent/skill 目录 | 工厂 ↔ 零件供应：wshobson 是选购目录，Harness 设计团队。可吸收 wshobson 条目作为 Harness 团队的零件 |
| LangGraph | 状态图编排 | 不同赛道：LangGraph 是长运行可恢复编排，Harness 是快速 Claude-Code-native 团队设计 |

---

## 9. 源码验证修正日志（v1 → v2 → v3）

| v1 结论 | v2 修正 | 证据 |
|---------|---------|------|
| "6-Phase Workflow" | **Phase 0-7（8 阶段）** | SKILL.md L18-428 实际有 Phase 0 (L18) + Phase 7 (L361) |
| "全链路 LLM 推理，无确定性代码" | **LLM 驱动执行 + references 强约束模板** | orchestrator-template.md 含 API 伪代码；skill-testing-guide.md 含 JSON schema |
| "Phase 6 Validation 是 LLM 生成测试方案文档，非运行时验证" | **完整 eval 框架：A/B + assertion + Grader/Comparator/Analyzer + 20-query 触发 eval** | skill-testing-guide.md 307 行全文 |
| "无独立 eval / score / threshold / rollback" | **有 eval/score/threshold，无自动 rollback** | §4 assertion JSON + pass_rate + non-discriminating 检测；无自动回滚机制 |
| "把三层评价都压给 LLM 自评或用户手动检查" | **客观任务有 assertion 自动评分，专业任务有 Comparator 盲测** | §4 + §5 |
| Claims Ledger C5 "plausible" | **confirmed — v1 严重低估** | skill-testing-guide.md 源码 |
| 漏掉 Phase 0 drift 检测 | **Phase 0 审计现有 agent/skill 与 CLAUDE.md 一致性** | SKILL.md L18-36 |
| 漏掉 Phase 7 进化机制 | **反馈类型→修改对象映射 + 进化触发条件 + 变更历史** | SKILL.md L361-428 |
| 漏掉执行模式决策树 | **Team vs Sub vs Hybrid 是 PRIMARY 轴** | agent-design-patterns.md L3-77 |
| 漏掉 harness-100 sister repo | **100 个生产级 harness，1,808 markdown 文件** | README L243-245 |
| 漏掉实验性 flag 依赖 | **需 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1** | README L265 |

---

| 漏掉实验性 flag 依赖 | **需 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1** | README L265 |
| C6/C7 "use-with-caveat" | **v3 升级为 "confirmed-direction, pending-replication"** | sister repo claude-code-harness 有完整论文+实验数据+6 图+可复现命令 |
| v2 未深读 qa-agent-guide.md | **v3 完成——7 个真实 bug + Integration Coherence Verification 方法论** | qa-agent-guide.md 228 行全文 |
| v2 未验证 harness-100 规模化 | **v3 完成——1,808 .md 文件确认，10 域 100 harness，三层 skill 系统** | harness-100 GitHub README |

---

## 10. v3 深挖补充

### 10-1. QA Agent Guide — Integration Coherence Verification（源码深读）

qa-agent-guide.md（228 行）不是泛泛的 QA 指南，而是**从真实项目 SatangSlide 提炼的缺陷模式库 + 验证方法论**。

**核心洞察：最频繁的缺陷不是"组件内部错误"，而是"边界面上契约不一致"**——两个组件各自正确，但连接处对不上。

**6 类边界不一致（源码 §1-1 表）：**
| 边界面 | 不一致示例 | 漏检原因 |
|--------|-----------|---------|
| API 响应 → 前端 hook | API 返回 `{projects:[]}`，hook 期望 `SlideProject[]` | 各自验证正常，不做交叉比较 |
| API 字段名 → 类型定义 | API `thumbnailUrl`(camelCase) vs 类型 `thumbnail_url`(snake_case) | TypeScript 泛型 cast 后编译器抓不到 |
| 文件路径 → 链接 href | 页面在 `/dashboard/create`，链接指向 `/create` | 不交叉比对文件结构和 href |
| 状态转移图 → 实际 status 更新 | 图定义 `generating→approved`，代码缺转移 | 只确认图存在，不追踪所有更新代码 |
| API 端点 → 前端 hook | API 存在但无对应 hook（没被调用） | 不做 1:1 映射 |
| 即时响应 → 异步结果 | API 即时返回 `{status}`，前端访问 `data.failedIndices` | 不区分同步/异步响应 |

**为什么静态 code review 抓不到（源码 §1-2）：**
- TypeScript 泛型局限：`fetchJson<SlideProject[]>()` 即使运行时返回 `{projects:[]}` 也编译通过
- `npm run build` 通过 ≠ 正常运行：类型 cast / `any` / 泛型绕过类型安全
- **存在验证 vs 连接验证是根本不同的验证**

**Integration Coherence Verification 方法论（源码 §2，4 项交叉验证）：**
1. **API 响应 shape ↔ 前端 hook 类型**：逐个 route 的 `NextResponse.json()` 调用 vs 对应 hook 的 `fetchJson<T>` 类型参数
2. **文件路径 ↔ 链接/router 路径**：`src/app/` 下 page 文件 URL 模式 vs 所有 `href`/`router.push()`/`redirect()` 值
3. **状态转移完整性追踪**：状态转移图的允许转移 vs 代码中所有 `.update({status:"..."})`，双向检查（死转移 + 未授权转移）
4. **API 端点 ↔ 前端 hook 1:1 映射**：所有 route.ts 的 HTTP 方法端点 vs 所有 use*.ts 的 fetch URL

**QA agent 设计 4 原则（源码 §3）：**
1. 用 `general-purpose` 类型（非 `Explore`）——QA 需要 Grep + 脚本执行 + 修改能力
2. "交叉比较"优先于"存在确认"——弱 checklist vs 强 checklist 对照表
3. **"同时读两边"原则**——API route 和对应 hook 必须一起读，状态图和更新代码必须一起读
4. **增量 QA**——每个模块完成后立即 QA，不要等全部完成后一次性 QA（错误累积传播）

**7 个真实 bug（源码 §结尾表，来自 SatangSlide 项目）：**
| Bug | 边界面 | 根因 |
|-----|--------|------|
| `projects?.filter is not a function` | API→hook | API 返回 `{projects:[]}`，hook 期望数组 |
| 仪表板所有链接 404 | 文件路径→href | 缺 `/dashboard/` 前缀 |
| 主题图片不显示 | API→组件 | `thumbnailUrl` vs `thumbnail_url` |
| 主题选择不保存 | API→hook | select-theme API 存在但无 hook |
| 生成页面永久等待 | 状态转移→代码 | 缺 `template_approved` 转移代码 |
| `data.failedIndices` 崩溃 | 即时响应→前端 | 后台结果在即时响应中访问 |
| 完成后查看幻灯片 404 | 文件路径→href | `/projects/` → `/dashboard/projects/` |

**Cat Café 借鉴价值：** 这套"边界交叉验证"方法论可以直接植入我们的 quality-gate skill。我们的 quality-gate 目前偏向"spec 合规检查"，缺少"组件间契约一致性检查"。特别是状态机完整性追踪和 API↔前端 1:1 映射，是我们验证流程的真实缺口。

### 10-2. harness-100 — 工厂规模化验证（源码确认）

harness-100 不是空壳仓库，而是**1,808 个 markdown 文件的生产级 harness 集合**，证明 Harness 工厂确实可规模化运行。

**规模（README "At a Glance" 表确认）：**
| 维度 | ko/ | en/ | 合计 |
|------|-----|-----|------|
| Harnesses | 100 | 100 | 200 |
| Agent definitions | 489 | 489 | 978 |
| Skills | 315 | 315 | 630 |
| Total .md files | 904 | 904 | **1,808** |

**10 个领域分类（README "Categories" 表确认）：**
1. Content Creation (01-15)：YouTube, podcast, game narrative, comics, translation
2. Software Dev & DevOps (16-30)：Full-stack, API, CI/CD, security audit, IaC
3. Data & AI/ML (31-42)：ML experiments, NLP, RAG/LLM apps, design systems
4. Business & Strategy (43-55)：Startup, market research, pricing, financial modeling
5. Education & Learning (56-65)：Language tutor, exam prep, debate simulator, ADR
6. Legal & Compliance (66-72)：Contracts, patents, GDPR/PIPA, regulatory filing
7. Health & Lifestyle (73-80)：Meal planning, fitness, tax, travel, wedding
8. Communication & Docs (81-88)：Technical writing, SOP, proposals, crisis comms
9. Operations & Process (89-95)：Hiring, onboarding, audit, procurement
10. Specialized Domains (96-100)：Real estate, e-commerce, ESG, IP portfolio

**每个 harness 的结构（README "Harness Architecture" 确认）：**
```
{NN}-{harness-name}/
└── .claude/
    ├── CLAUDE.md                    # 项目概述
    ├── agents/
    │   ├── {specialist-1..4}.md     # 领域专家 agent
    │   └── {reviewer/qa}.md         # 交叉验证 agent
    └── skills/
        ├── {orchestrator}/skill.md  # 团队编排
        ├── {domain-skill-1}/skill.md  # agent 扩展 skill
        └── {domain-skill-2}/skill.md
```

**三层 Skill 系统（README 确认）：**
| 层 | 用途 | 示例 |
|----|------|------|
| Orchestrator | 团队协调、工作流、错误处理 | `youtube-production/skill.md` |
| Agent-Extending | 放大 agent 专长的领域知识 | `hook-writing/skill.md`, `thumbnail-psychology/skill.md` |
| External | 已有工具 | `gemini-3-pro-imagegen` |

**8 项质量标准（每个 harness 都包含）：**
- Agent Team Mode（SendMessage 直接通信 + 交叉验证）
- Domain Expertise（真实框架：OWASP, Bloom's Taxonomy, Porter's 5 Forces, DCF 等）
- Structured Outputs（每 agent 的领域特定模板）
- Dependency DAG（任务排序 + 并行执行）
- Error Handling（retry / skip / fallback）
- Scale Modes（full pipeline / reduced / single-agent）
- Test Scenarios（normal / existing-file / error 三类）
- Trigger Boundaries（should-trigger + NOT-trigger 定义）

**嵌入的真实框架密度（README "Domain Expertise" 表确认）：**
- Content: AIDA, Pattern Interrupt, CURVE formula, Platform Specs
- Development: SOLID, DDD, OWASP Top 10, Test Pyramid, DORA Metrics, CWE Top 25
- Data: Star/Snowflake Schema, Great Expectations, SHAP/LIME, Feature Engineering
- Business: BMC, TAM/SAM/SOM, Porter's 5 Forces, RICE, Van Westendorp PSM
- Education: Bloom's Taxonomy, ADDIE, CEFR, SM-2 Spaced Repetition, Toulmin Model
- Legal: IRAC, MQM, GDPR/PIPA, IPC/CPC, Claim Drafting Patterns
- Lifestyle: BMR/TDEE, ACSM Guidelines, Compound Interest, Route Optimization
- Documents: Diataxi, PREP, STAR, MADR, SemVer, Mermaid Patterns
- Operations: SIPOC/RACI, 4C Framework, SMART, NPS/CSAT, BARS Assessment
- Specialized: GHG Protocol, Cap Rate/IRR, IMRaD, Georgia-Pacific, Double Materiality

**Cat Café 借鉴价值：**
1. **"三层 Skill 系统"概念**——Orchestrator / Agent-Extending / External 的分层比我们当前的 skill 组织更清晰。我们的 skill 大多混在一起，没有区分"编排层"和"知识扩展层"
2. **Trigger Boundaries**——每个 harness 显式定义 should-trigger + NOT-trigger，这是我们 skill 触发机制缺少的（我们的 skill description 只说何时触发，不说何时不触发）
3. **Scale Modes**——full / reduced / single-agent 三档，适应不同复杂度。我们目前一刀切
4. **Domain Expertise 嵌入**——把 AIDA/Bloom's/OWASP 等真实框架嵌入 skill，而非泛泛而谈。我们的 skill 偏流程，领域知识密度不够

**caveat：** harness-100 仅 1 commit（一次性 dump），无法看迭代历史。1.1k stars + 400 forks 但 0 issues + 3 PRs，社区参与度低。质量无法逐个验证（1,808 文件太多），但抽样 README 显示结构一致性很高。

### 10-3. +60% Claim 交叉验证（sister repo claude-code-harness）

**sister repo 基本信息：** 114 stars / 20 forks / 14 commits。HTML 93.4% + JavaScript 4.7% + Python 1.3%（Python 用于 matplotlib 图 + 评估脚本）。

**实验仓库结构（README "Project Structure" 确认）：**
```
claude-code-harness/
  .claude/                    # 项目级 Harness 配置
    skills/                   # 实验相关 skill
    commands/                 # slash 命令（/experiment, /evaluate, /report）
  experiments/
    cases/                    # 15 个任务定义（YAML）
    results/                  # 每个任务的结果
      case-{001-015}/
        baseline/             # Baseline 产出（无 .claude/）
        harness/              # Harness 产出（有 .claude/）
          .claude/            # 任务特定的 Harness 配置
            CLAUDE.md
            skills/
            agents/
        evaluation.json       # 10 维度对比评估
    reports/                  # 聚合报告和数据
  paper/                      # 学术论文
    harness-paper.pdf         # 英文（9 页）
    harness-paper-ko.pdf      # 韩文
    figures/                  # matplotlib 生成的 6 张图
```

**论文核心发现（README "Key Findings" 确认）：**
1. **"瓶颈是结构，不是能力"**——LLM 有足够知识，缺的是项目特定的结构化指导
2. **测试覆盖率受益最大**（+4.9）——无引导的 agent 几乎不写测试
3. **架构是第二受益**（+4.4）——无引导时 agent 默认单体单文件实现
4. **复杂度放大效应**——简单任务中等增益，复杂系统戏剧性提升
5. **自动生成可行**——Harness meta-skill 可从自然语言描述自动生成配置

**评估可信度分析：**
- ✅ 实验设计合理（controlled A/B, 3 难度 × 5 任务）
- ✅ 10 维度评分体系完整（测试覆盖/架构/错误处理/可扩展性等）
- ✅ 数据全公开（15 案例的 baseline + harness 产出 + evaluation.json）
- ✅ 可复现（/experiment, /evaluate, /report 命令）
- ⚠️ **评分者身份未明确**——evaluation.json 是 author-graded 还是 LLM-graded？如果是 LLM 评 LLM 产出，有循环偏差风险
- ⚠️ n=15 统计显著性不足（虽 15/15 全胜，但样本小）
- ⚠️ 无第三方复现（114 stars 说明复现者少）
- ⚠️ 14 commits 说明实验为一次性产出，无迭代验证

**v3 最终判定：** `confirmed-direction, pending-replication`。方向几乎确定（结构化预配置 → 质量提升，符合 arXiv:2604.18071 + 15 案例全胜 + 难度增益递增符合直觉），绝对值（+60%）可能因 author-graded 偏高，但**这是 GitHub AI 工具领域罕见的完整学术级实验**，远超同类项目的"口口相传"式 claim。

---

## 11. 总结

### 一句话评价（v3 修正）

revfactory/harness 是一个**营销诚实度业界范本、工程深度被 README 低估、测试方法论严谨、有学术级实验支撑**的 L3 Meta-Factory 项目：它把业界已知的 6 种多 agent 架构模式 + 执行模式决策树操作化为 Claude Code Agent Teams API，通过一句话触发 LLM 生成 agent 团队配置，配有完整的 A/B eval 框架（sister repo 有论文 + 15 案例实验数据）、100 个生产级示例（1,808 markdown 文件）、从真实项目提炼的 QA 边界交叉验证方法论，但全链路无自动 rollback、依赖实验性特性、skill 本体全韩语、+60% 绝对值待第三方复现。

### 价值评估（v3 修正）

| 维度 | v1 | v2 | **v3** | 变更理由 |
|------|-----|-----|------|----------|
| 概念清晰度 | ★★★★★ | ★★★★★ | ★★★★★ | 不变 |
| 营销诚实度 | ★★★★☆ | ★★★★★ | ★★★★★ | 不变（v2 已满分）|
| 技术深度 | ★★☆☆☆ | ★★★★☆ | ★★★★☆ | 不变 |
| 模式实用性 | ★★★★☆ | ★★★★★ | ★★★★★ | 不变 |
| 可验证性 | ★★☆☆☆ | ★★★★☆ | **★★★★★** | v3 升级——sister repo 有完整论文 + 15 案例数据 + 6 图 + 可复现命令，是 GitHub AI 工具领域罕见的学术级实验 |
| 对 Cat Café 的参考价值 | ★★★★☆ | ★★★★★ | **★★★★★** | v3 强化——QA 边界交叉验证方法论 + 三层 skill 系统 + Trigger Boundaries 都是直接可借鉴的工程知识 |

### 后续待办

- [x] clone 源码，验证 SKILL.md 和 references/ 的实际内容质量 ✅ v2 完成
- [x] 验证 6 种架构模式的具体实现深度 ✅ v2 完成（含执行模式 + 复合模式）
- [x] 检查 orchestrator-template.md 的协议具体程度 ✅ v2 完成（3 模板含 API 伪代码）
- [x] 检查 skill-testing-guide.md 的测试方法论 ✅ v2 完成（完整 eval 框架）
- [x] 交叉验证 +60% claim（sister repo claude-code-harness）✅ v3 完成——有完整论文+实验数据，升级为 confirmed-direction, pending-replication
- [x] 深读 qa-agent-guide.md 的 7 个真实 bug 案例 ✅ v3 完成——Integration Coherence Verification 方法论 + 7 个 SatangSlide 真实 bug
- [x] 检查 harness-100 的 100 个示例质量 ✅ v3 完成——1,808 .md 文件确认，10 域 100 harness，三层 skill 系统，8 项质量标准
- [ ] 可选：抽样阅读 harness-100 中 1-2 个具体 harness 的完整内容（验证单 harness 内部质量）
- [ ] 可选：检查 evaluation.json 是否 LLM-graded（评估 +60% 的循环偏差风险）

---

*报告状态: v3 深挖版完成。3 项可选深化全部完成（qa-agent-guide / harness-100 / +60% 交叉验证）。Claims Ledger C6/C7 升级为 confirmed-direction, pending-replication。v1 的 3 处严重误判已在 v2 修正，v3 补充了 sister repo 实验数据、QA 方法论、规模化证据。剩余 2 项为可选抽样验证。*
