> Reference 链路：执行本文件前，先读取本 skill 的 `references/data-query-order.md`、`references/cn-markdown-formatting.md`；本文件只描述业务 workflow 或参考口径，不承载新增中文格式正文。

# 工作流模式

## 顺序型工作流

对于复杂任务，将操作拆分为清晰的连续步骤。通常建议在 `SKILL.md` 开头附近给 Codex 一个流程概览：

```markdown
填写 PDF 表单包含以下步骤：

1. 分析表单（运行 analyze_form.py）
2. 创建字段映射（编辑 fields.json）
3. 验证映射（运行 validate_fields.py）
4. 填写表单（运行 fill_form.py）
5. 验证输出（运行 verify_output.py）
```

## 条件型工作流

对于带分支逻辑的任务，引导 Codex 经过决策节点：

```markdown
1. 判断修改类型：
   **创建新内容？** → 按下面“创建工作流”执行
   **编辑已有内容？** → 按下面“编辑工作流”执行

2. 创建工作流：[步骤]
3. 编辑工作流：[步骤]
```
