---
name: superpowers-workflow
description: Superpowers-style software development workflow - systematic, test-driven, iterative development
author: lutra
metadata:
  lutra:
    emoji: 🦦
    workflow:
      phases:
        - brainstorm
        - plan
        - implement
        - test
        - review
        - finish
---

# Superpowers Workflow 🦦

Systematic software development workflow inspired by Simon Tatham's Superpowers framework.

## Philosophy

| Principle | Meaning |
|-----------|---------|
| **TDD** | Write tests first, always |
| **YAGNI** | You Aren't Gonna Need It |
| **DRY** | Don't Repeat Yourself |
| **Evidence over claims** | Verify before declaring success |
| **Systematic over ad-hoc** | Process over guessing |

## Workflow Phases

### 1. Brainstorming (设计阶段)

**Before writing any code:**

```
Questions to ask:
1. What problem are we solving?
2. Who is this for?
3. What is the simplest solution?
4. What are the success criteria?
5. What could go wrong?
```

**Output:** Rough spec document (1-2 paragraphs)

---

### 2. Planning (任务拆解)

**After design approval:**

Break work into **bite-sized tasks** (2-5 minutes each):

```markdown
## Task 1: [File: src/auth.py]
- Create User model
- Add password hashing
- Verification: run tests

## Task 2: [File: src/auth.py]
- Add login endpoint
- Add JWT token generation
- Verification: curl test endpoint
```

**Rules:**
- Each task has exact file paths
- Each task has verification steps
- No task requires more than one commit

---

### 3. Implementation (实现)

**During implementation, follow TDD:**

```
1. RED: Write failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Clean up
4. COMMIT: Only after test passes
```

**If code is written before tests → DELETE IT**

---

### 4. Testing (测试)

**Test-driven cycle:**

```bash
# 1. Write test
pytest test_feature.py -v

# 2. Watch it fail (RED)
# 3. Write minimal code
# 4. Watch it pass (GREEN)
# 5. Refactor
# 6. Commit
```

---

### 5. Code Review (审查)

**Before moving to next task:**

| Severity | Action |
|----------|--------|
| Critical | Block progress, fix immediately |
| Major | Fix before merge |
| Minor | Note for future |
| Nitpick | Optional |

**Review checklist:**
- [ ] Matches implementation plan?
- [ ] Tests pass?
- [ ] No TODO comments left?
- [ ] Code follows style?
- [ ] Error handling?

---

### 6. Finishing (完成)

**When all tasks complete:**

1. Verify all tests pass
2. Present options:
   - Merge to main
   - Create PR
   - Keep branch open
   - Discard branch
3. Clean up worktree if needed

---

## Quick Reference

### Before starting a task:
```
1. Am I clear on what to build?
2. Is there an approved plan?
3. Do I have tests written?
```

### During implementation:
```
1. Did tests pass?
2. Did I commit after each test pass?
3. Did I avoid YAGNI violations?
```

### Between tasks:
```
1. Did I review my own code?
2. Are critical issues fixed?
3. Is the task complete?
```

---

## Integration with Clawdbot

### Cron Jobs (existing)
```yaml
- Nightly Project Builder (2 AM): Build small tools
- Code Quality Scan (6 AM): Check TODOs and errors
- System Health Check (6 AM): Verify everything works
```

### Memory System
- **brainstorming** → `memory/YYYY-MM-DD.md`
- **plans** → `.plans/` folder
- **reviews** → `.learnings/SELF-REVIEW.md`
- **completed work** → `MEMORY.md`

---

## Example Workflow

### Task: Add user authentication

```markdown
## Plan
- [ ] Create User model with email/password
- [ ] Add bcrypt hashing
- [ ] Create login endpoint
- [ ] Add JWT generation
- [ ] Write unit tests

## Task 1: User Model
File: src/models/user.py
Test: tests/test_user.py
Verification: pytest tests/test_user.py -v
```

---

## Commands

### Start a workflow
```bash
# Brainstorming phase
Write design spec to .plans/PROJECT.md

# Planning phase
Split into tasks: .plans/tasks/NAME-001.md

# Implementation phase  
For each task:
  1. Write test
  2. Implement
  3. Verify
  4. Commit

# Review phase
Review against .plans/PROJECT.md

# Finish phase
Verify all tests, create PR or merge
```

### Verify current state
```bash
# Check pending tasks
ls .plans/tasks/

# Check tests status
pytest --collect-only -q

# Check git status
git status --short
```

---

## Anti-Patterns to Avoid

| Anti-pattern | Instead |
|--------------|---------|
| Writing code without tests | Write test first |
| Big commits | Small, focused commits |
| Skipping code review | Always review |
| YAGNI violations | Simplest solution first |
| Skipping verification | Always test |

---

## Resources

- Original: https://github.com/obra/superpowers
- Blog: https://blog.fsck.com/2025/10/09/superpowers/
- This adaptation: skills/superpowers-workflow/SKILL.md
