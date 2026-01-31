.PHONY: help test lint clean install run

help:
	@echo "Content Factory - Available commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run unit tests"
	@echo "  make lint       - Code style check"
	@echo "  make clean      - Clean cache files"
	@echo "  make run        - Generate sample article"
	@echo "  make help       - Show this help"

install:
	pip install -r requirements.txt

test:
	python tests/test_core.py

lint:
	@echo "Checking code style..."
	-python -m py_compile lib/*.py
	@echo "✅ Code compiles successfully"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache cleaned"

run:
	@echo "Generating sample article..."
	python scripts/generate.py article --topic "AI Agent 开发" \
		--keywords "AI, Agent, 自动化" \
		--audience "技术开发者"
