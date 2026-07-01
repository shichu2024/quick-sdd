# SDD Harness Profile（可选质量画像）契约

Profile 是可选质量覆盖层，不是 core 的依赖。

## 必需元数据（Frontmatter）

```yaml
---
profile_id:
optional: true
applies_when: []
not_for: []
core_compatibility:
  changes_state_machine: false
  changes_role_ownership: false
---
```

## 允许内容

- 本地术语表
- 模块或边界地图
- 额外 QA 检查
- 推荐 verify 命令
- 已知本地失败模式
- 触发和非触发示例
- 本地权威文档链接

## 禁止内容

- 新增 core 阶段
- 改变角色归属
- 添加必需领域假设
- 隐藏写权限
- 产品验收决策

## 健康检查

删除 profile 后，只应该减少本地质量提示，而不能阻止一个普通 feature 完成 SDD 生命周期。
