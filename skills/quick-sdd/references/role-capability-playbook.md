# Quick SDD 角色能力 Playbook

## 用途

这是 `quick-sdd` 五个核心角色共享的专业实践参考层。角色 `SKILL.md` 应保持短而可执行；跨角色共通的方法、检查表和术语放在这里复用。

## 共通原则

- 先规划再执行，先澄清再落盘，先验证再宣告完成。
- 协作不是自动驾驶，保留用户决策点。
- 证据不足时，不要假设已经完成。
- 角色边界优先于“顺手多做一点”。
- 并行只在依赖满足且写路径不重叠时成立。

## PM 速查

- 先分拣：闲聊/问答 vs 正式任务。
- 派发前先去噪并重述目标。
- 审议后必须继续推进到下一责任人。
- 关键路径优先，blocker 要可见。

## RA 速查

- 维护 `proposal.md`：问题、目标、范围、非目标、风险和 open questions。
- QA 完成后维护 `acceptance.md`：对照原始需求、用户价值、QA 证据和剩余风险做最终需求验收。
- 可以写验收意图，但不要代 TA 写 story 或 acceptance criteria。
- 可以接受 `conditional_pass` 的剩余风险，但必须在 `acceptance.md` 明确理由和后续责任。
- 区分 observed / inferred / to_confirm。
- 交给 TA 前，proposal 边界要足够稳定。

## TA 速查

- 维护 `stories.md`：story 按用户价值切，不按实现动作切。
- 维护 `architecture.md`：模块边界、关键决策、接口、数据/状态和风险。
- 审计 DEV 的 `tasks.md`：边界、ACL、依赖、verify 和架构一致性。
- 共享契约变化要回传给 PM。

## DEV 速查

- 先看 proposal、story、architecture，再写 `tasks.md`。
- task 经 TA 审计后，再进入代码实现。
- 优先 TDD；完成后执行 verification loop。
- 证据优先，没有证据不报完成。
- 不越权扩大改动范围。

## QA 速查

- 先审 proposal -> stories -> architecture -> tasks 的文档链，再看实现和证据。
- 结论必须基于行为、证据和风险，不基于感觉。
- 区分 `pass / conditional_pass / fail`。
- 明确 `root_cause_type / reroute_to / reroute_action`。
- QA 的 `validation-report.md` 是 RA 最终验收的输入，不直接替代 `acceptance.md`。
