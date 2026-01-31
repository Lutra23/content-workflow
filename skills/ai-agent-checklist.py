#!/usr/bin/env python3
"""AI Agent 项目配置检查工具"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# 颜色定义
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_check(name: str, passed: bool, suggestion: str = ""):
    status = f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"
    print(f"  {status} {name}")
    if not passed and suggestion:
        print(f"     {YELLOW}→ {suggestion}{RESET}")


def check_env(path: Path) -> Tuple[bool, str]:
    """检查 .env 配置"""
    env_files = [".env", ".env.example", ".env.template"]
    for f in env_files:
        if (path / f).exists():
            return True, ""
    return False, "创建 .env.example 模板文件"


def check_dependencies(path: Path) -> Tuple[bool, str]:
    """检查依赖文件"""
    if (path / "requirements.txt").exists():
        return True, ""
    if (path / "package.json").exists():
        return True, ""
    if (path / "pyproject.toml").exists():
        return True, ""
    return False, "创建 requirements.txt 或 package.json"


def check_readme(path: Path) -> Tuple[bool, str]:
    """检查 README.md"""
    if (path / "README.md").exists():
        return True, ""
    return False, "创建 README.md 文档"


def check_version_control(path: Path) -> Tuple[bool, str]:
    """检查版本控制"""
    if (path / ".git").exists():
        return True, ""
    return False, "初始化 git 仓库: git init"


def check_logging(path: Path) -> Tuple[bool, str]:
    """检查日志配置"""
    py_files = list(path.glob("*.py"))
    for pf in py_files:
        content = pf.read_text()
        if re.search(r'import logging|from logging|logger =|logging\.config', content):
            return True, ""
    return False, "添加 logging 配置"


def check_error_handling(path: Path) -> Tuple[bool, str]:
    """检查错误处理"""
    py_files = list(path.glob("*.py"))
    for pf in py_files:
        content = pf.read_text()
        if re.search(r'try:|except|raise|@retry|tenacity', content):
            return True, ""
    return False, "添加 try/except 错误处理或重试机制"


def check_langgraph_state(path: Path) -> Tuple[bool, str]:
    """检查 LangGraph state 定义"""
    py_files = list(path.glob("*.py"))
    for pf in py_files:
        content = pf.read_text()
        if re.search(r'class.*State|StateDict|TypedDict', content):
            return True, ""
    return False, "添加 State 定义 (TypedDict 或 dataclass)"


def check_langgraph_tools_condition(path: Path) -> Tuple[bool, str]:
    """检查 LangGraph tools_condition"""
    py_files = list(path.glob("*.py"))
    for pf in py_files:
        content = pf.read_text()
        if re.search(r'tools_condition|tools_condition_fn|should_continue', content):
            return True, ""
    return False, "添加 tools_condition 路由逻辑"


def is_langgraph_project(path: Path) -> bool:
    """判断是否为 LangGraph 项目"""
    py_files = list(path.glob("*.py"))
    for pf in py_files:
        content = pf.read_text()
        if re.search(r'from langgraph|import langgraph|StateGraph|compile_graph', content):
            return True
    return False


def check_project(path: Path):
    """检查项目"""
    path = Path(path).resolve()
    
    print(f"\n📁 检查项目: {path}\n")
    
    # 基础检查
    print_check(".env 配置", *check_env(path))
    print_check("依赖文件 (requirements.txt/package.json)", *check_dependencies(path))
    print_check("README.md 文档", *check_readme(path))
    print_check("版本控制 (.git)", *check_version_control(path))
    print_check("日志配置", *check_logging(path))
    print_check("错误处理", *check_error_handling(path))
    
    # LangGraph 专项检查
    if is_langgraph_project(path):
        print(f"\n  {YELLOW}🔍 LangGraph 专项检查{RESET}")
        print_check("State 定义", *check_langgraph_state(path))
        print_check("tools_condition 路由", *check_langgraph_tools_condition(path))
    
    print()


def main():
    if len(sys.argv) < 2:
        path = Path.cwd()
    else:
        path = Path(sys.argv[1])
    
    if not path.exists():
        print(f"错误: 路径不存在: {path}")
        sys.exit(1)
    
    if path.is_file():
        path = path.parent
    
    check_project(path)


if __name__ == "__main__":
    main()
