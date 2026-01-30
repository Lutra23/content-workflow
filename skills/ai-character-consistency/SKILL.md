# AI Character Consistency

角色一致性保持工具，用于在AI动漫制作中确保同一角色在不同场景、姿态、表情下保持一致的外观。基于IP-Adapter、InstantID和LoRA技术。

## 功能特性

- **IP-Adapter风格迁移**：保持角色风格一致性
- **InstantID身份保持**：精确保持角色面部特征
- **简化版LoRA训练**：快速训练角色专属模型
- **多姿态生成**：生成角色不同姿态的图像
- **表情变化生成**：生成角色不同表情的图像

## 快速开始

### 安装依赖

```bash
cd /home/zous/clawd/skills/ai-character-consistency
pip install -r requirements.txt
```

### 环境配置

```bash
# 基础配置
export CUDA_VISIBLE_DEVICES=0
export DIFFUSERS_CACHE=/home/zous/.cache/huggingface/diffusers

# 可选：ControlNet模型路径
export CONTROLNET_CACHE=/home/zous/.cache/controlnet
```

### 创建角色参考

```bash
python scripts/create-ref.py \
    --reference "path/to/character_image.jpg" \
    --output "path/to/character_ref.yaml" \
    --num-images 5
```

### 生成不同姿态

```bash
python scripts/generate-pose.py \
    --reference "path/to/character_ref.yaml" \
    --pose "walking" \
    --output "path/to/output/" \
    --num-samples 3
```

## 使用方法

### Python API

```python
from lib.character_consistency import CharacterConsistency

# 初始化
consistency = CharacterConsistency()

# 创建角色参考
ref = consistency.create_reference(
    reference_images=["char1.jpg", "char2.jpg"],
    name="my_character",
    save_path="character_ref.yaml"
)

# 生成新姿态
results = consistency.generate_pose(
    reference=ref,
    pose="running",
    num_samples=2,
    output_dir="output/"
)

# 生成表情变化
expressions = consistency.generate_expression(
    reference=ref,
    expression="happy",
    num_samples=1
)

# 使用InstantID保持身份
id_result = consistency.apply_instantid(
    reference_face="char_face.jpg",
    target_image="pose_image.jpg",
    identity_strength=0.8
)
```

### InstantID身份保持

```python
from lib.character_consistency import InstantID

id_handler = InstantID()

# 加载身份
identity = id_handler.load_identity("character_ref.yaml")

# 保持身份生成
result = id_handler.generate_with_identity(
    identity=identity,
    prompt="same character, different pose",
    negative_prompt="different person",
    num_samples=4
)
```

### LoRA训练（简化版）

```python
from lib.character_consistency import SimpleLoraTrainer

trainer = SimpleLoraTrainer()

# 准备训练数据
trainer.prepare_data(
    images_folder="character_images/",
    output_folder="processed_images/",
    size=512
)

# 训练LoRA
trainer.train(
    base_model="runwayml/stable-diffusion-v1-5",
    output_lora="character_lora.safetensors",
    learning_rate=1e-4,
    max_steps=500,
    batch_size=4
)
```

## 配置文件

### 模型配置 (configs/models.yaml)

```yaml
models:
  base:
    name: "runwayml/stable-diffusion-v1-5"
    path: "/models/sd-v1-5"
    
  instantid:
    name: "InstantID/InstantID"
    path: "/models/instantid"
    face_encoder: "antelopev2"
    
  ip_adapter:
    name: "h94/IP-Adapter"
    path: "/models/ip-adapter"
    scales:
      style: 0.8
      structure: 1.0

controlnet:
  openpose:
    name: "lllyasviel/ControlNet-v1-1"
    path: "/models/controlnet/openpose"
    
  canny:
    name: "lllyasviel/ControlNet-v1-1"
    path: "/models/controlnet/canny"
```

## 脚本说明

### create-ref.py - 创建角色参考

```bash
python scripts/create-ref.py [OPTIONS]

选项:
  --reference, -r     参考图像路径 (必需)
  --output, -o        输出配置文件路径 (必需)
  --num-images, -n    生成参考图数量 (默认: 5)
  --style, -s         风格预设 (默认: anime)
  --resolution        输出分辨率 (默认: 512x512)
```

### generate-pose.py - 生成不同姿态

```bash
python scripts/generate-pose.py [OPTIONS]

选项:
  --reference, -r     角色参考配置 (必需)
  --pose, -p          姿态类型 (必需)
  --output, -o        输出目录 (必需)
  --num-samples, -n   生成数量 (默认: 1)
  --controlnet, -c    ControlNet类型 (openpose/canny)
  --strength          生成强度 (默认: 0.8)
```

### generate-expression.py - 生成表情

```bash
python scripts/generate-expression.py [OPTIONS]

选项:
  --reference, -r     角色参考配置 (必需)
  --expression, -e    表情类型 (必需)
  --output, -o        输出目录 (必需)
  --num-samples, -n   生成数量 (默认: 1)
```

## 姿态类型

| 姿态 | 描述 | ControlNet |
|------|------|------------|
| standing | 站立 | OpenPose |
| walking | 行走 | OpenPose |
| running | 跑步 | OpenPose |
| sitting | 坐着 | OpenPose |
| dancing | 舞蹈 | OpenPose |
| fighting | 战斗 | OpenPose |
| profile | 侧面 | OpenPose |
| hand_gesture | 手势 | OpenPose + Canny |

## 表情类型

| 表情 | 描述 | 参数 |
|------|------|------|
| happy | 开心 | smile=0.8 |
| sad | 悲伤 | tear=0.5 |
| angry | 愤怒 | brow_furrow=0.7 |
| surprised | 惊讶 | eye_widen=0.8 |
| calm | 平静 | neutral=1.0 |
| crying | 哭泣 | tear=1.0 |
| laughing | 大笑 | mouth_open=0.9 |
| wink | 眨眼 | eye_closed=0.7 |

## 输出格式

| 格式 | 用途 | 质量 |
|------|------|------|
| PNG | 透明背景 | 无损 |
| JPG | 预览/分享 | 高 |
| WEBP | 动画帧 | 高 |

## 工作流集成

### 与AI图像生成器集成

```python
from lib.character_consistency import CharacterConsistency
from anime_image_generator import AnimeImageGenerator

# 初始化
character = CharacterConsistency()
generator = AnimeImageGenerator()

# 创建角色参考
ref = character.create_reference(["char1.jpg", "char2.jpg"], "heroine")

# 生成场景
scene = generator.generate(
    prompt="heroine standing in cherry blossom garden",
    character_ref=ref,
    style="anime"
)
```

### 与分镜生成器集成

```bash
# 生成分镜时保持角色一致
python scripts/generate.py \
    --script story.txt \
    --character-ref character_ref.yaml \
    --output storyboard_frames/
```

## 故障排除

### 常见问题

**身份保持效果差:**
- 使用更高质量的参考图像
- 调整identity_strength参数
- 尝试不同的Face Parser模型

**姿态不自然:**
- 使用合适的ControlNet类型
- 调整controlnet_conditioning_scale
- 尝试参考真实姿态图像

**风格不一致:**
- 使用IP-Adapter style scale调整
- 确保参考图像风格统一
- 调整CLIP skip参数

### 性能优化

1. 使用GPU加速
2. 启用批处理
3. 缓存中间结果
4. 使用低分辨率预览

## 依赖

```
torch>=2.0.0
diffusers>=0.25.0
transformers>=4.35.0
accelerate>=0.25.0
controlnet-lora>=0.1.0
ip-adapter>=0.1.0
instantid>=0.1.0
opencv-python>=4.8.0
mediapipe>=0.10.0
Pillow>=10.0.0
PyYAML>=6.0
```

## 参考资料

- [InstantID](https://github.com/InstantID/InstantID)
- [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter)
- [ControlNet](https://github.com/lllyasviel/ControlNet)
- [LoRA](https://github.com/cloneofsimo/lora)

## 限制

### 当前限制
- 仅支持SD 1.5基础模型
- 需要至少4GB显存
- 暂不支持视频序列

### 计划功能
- [x] InstantID支持
- [x] IP-Adapter支持
- [x] 简化LoRA训练
- [ ] ControlNet完整支持
- [ ] 视频序列一致性
- [ ] 批量角色管理
