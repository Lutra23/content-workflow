# AI Storyboard Generator

AI分镜生成工具，从剧本自动生成分镜。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 生成分镜
python scripts/generate.py \
    --script "path/to/script.txt" \
    --output "output/" \
    --style anime \
    --format pdf
```

## 主要功能

- 剧本解析，自动分割场景
- 画面构图建议
- 分镜草图生成
- 镜头语言设计
- 导出PDF/PNG分镜文档

## 文档

见 [SKILL.md](SKILL.md)
