# Superpowers 学习笔记

> Simon Tatham (PuTTY 作者) 的 agentic software development 框架
> https://github.com/obra/superpowers

## 核心原则

| 原则 | 含义 |
|------|------|
| **TDD** | Write tests first, always |
| **Systematic over ad-hoc** | Process over guessing |
| **YAGNI** | You Aren't Gonna Need It - 不要过度工程 |
| **DRY** | Don't Repeat Yourself |
| **Evidence over claims** | Verify before declaring success |

## 工作流程 (7 步)

```
1. Brainstorming      → 设计讨论，不急于写代码
2. using-git-worktrees → 创建隔离工作空间
3. Writing Plans     → 拆解为 2-5 分钟的小任务
4. executing-plans   → 批量执行，有人类检查点
5. test-driven-development → RED-GREEN-REFACTOR
6. requesting-code-review → 审查，按严重性报告
7. finishing-a-branch → 验证测试，决定 merge/PR
```

## Skills Library

### Testing
- `test-driven-development` - RED-GREEN-REFACTOR cycle

### Debugging  
- `systematic-debugging` - 4-phase root cause process
- `verification-before-completion` - 确保真的修复了

### Collaboration
- `brainstorming` - Socratic design refinement
- `writing-plans` - Detailed implementation plans
- `executing-plans` - Batch execution with checkpoints
- `subagent-driven-development` - 两阶段审查
- `requesting-code-review` - Pre-review checklist

### Meta
- `writing-skills` - Create new skills

## 与我的系统的共鸣

| Superpowers | 我的系统 |
|-------------|----------|
| Skills system | Skills folder |
| TDD | Self-review + testing |
| Systematic process | Memory decay + reflection |
| Subagent workflow | Cron jobs + isolated sessions |
| Evidence over claims | Memory + logs |

## 可借鉴的点

1. **强制工作流** - Skills trigger automatically, mandatory not suggestions
2. **两阶段审查** - spec compliance → code quality
3. **小任务拆解** - 2-5 minutes each, exact file paths
4. **Git worktrees** - Parallel development branches
5. **验证文化** - Verify before completion

## 下一步

考虑将 Superpowers 的原则整合到我的：
- Cron job 任务设计
- Self-review 流程
- Skill 创建方法
