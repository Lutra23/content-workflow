# AI Character Consistency

角色一致性保持工具，用于在AI动漫制作中保持角色外观一致性。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 创建角色参考
python scripts/create-ref.py \
    --reference "path/to/character.jpg" \
    --output "character_ref.yaml"

# 生成新姿态
python scripts/generate-pose.py \
    --reference "character_ref.yaml" \
    --pose "walking" \
    --output "output/"
```

## 主要功能

- 创建角色参考
- 生成不同姿态
- 生成不同表情
- InstantID身份保持
- 简化版LoRA训练

## 文档

见 [SKILL.md](SKILL.md)
