#!/bin/bash
# 自动化测试运行 - 每周 3 次运行测试

echo "=== $(date) Automated Test Run ==="

cd /home/zous/clawd

# 检查是否有测试文件
TEST_FILES=$(find . -name "*test*.py" -o -name "test_*" 2>/dev/null | wc -l)
echo "Test files found: $TEST_FILES"

# 运行简单的 Python 语法检查
echo "=== Python Syntax Check ==="
PYTHON_ERRORS=0
for f in $(find . -name "*.py" 2>/dev/null); do
  if ! python3 -m py_compile "$f" 2>/dev/null; then
    echo "Syntax error in: $f"
    ((PYTHON_ERRORS++))
  fi
done
echo "Python syntax errors: $PYTHON_ERRORS"

# 检查 shell 脚本
echo "=== Shell Script Check ==="
SHELL_ERRORS=0
for f in $(find . -name "*.sh" 2>/dev/null); do
  if ! bash -n "$f" 2>/dev/null; then
    echo "Shell error in: $f"
    ((SHELL_ERRORS++))
  fi
done
echo "Shell script errors: $SHELL_ERRORS"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Tests: $TEST_FILES | Python errors: $PYTHON_ERRORS | Shell errors: $SHELL_ERRORS" >> /home/zous/clawd/.logs/test-run.log

echo "=== Test Run Complete ==="
