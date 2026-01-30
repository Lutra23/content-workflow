# AI Storyboard Generator

AI分镜生成工具，自动从剧本解析生成专业的动漫分镜。包括场景分割、画面构图、镜头语言设计和导出功能。

## 功能特性

- **剧本解析**：自动识别场景、角色、动作、对话
- **画面构图建议**：基于电影语言提供构图建议
- **分镜草图生成**：生成简化的分镜草图
- **镜头语言设计**：景别、运镜、角度设计
- **导出PDF/PNG**：专业分镜文档导出

## 快速开始

### 安装依赖

```bash
cd /home/zous/clawd/skills/ai-storyboard-gen
pip install -r requirements.txt
```

### 生成分镜

```bash
python scripts/generate.py \
    --script "path/to/script.txt" \
    --output "path/to/output/" \
    --style anime \
    --format pdf
```

## 使用方法

### Python API

```python
from lib.storyboard import StoryboardGenerator

# 初始化
generator = StoryboardGenerator()

# 从剧本生成分镜
storyboard = generator.generate(
    script="剧本文本内容",
    num_panels=20,
    style="anime"
)

# 从文件生成分镜
storyboard = generator.generate_from_file(
    script_path="script.txt",
    style="anime",
    format="long"
)

# 导出分镜
storyboard.export(
    output="storyboard.pdf",
    format="pdf",
    quality="high"
)

# 导出PNG序列
storyboard.export_frames(
    output_dir="frames/",
    format="png"
)
```

### 场景解析

```python
from lib.storyboard import ScriptParser

parser = ScriptParser()

# 解析剧本
result = parser.parse("""
场景1: 教室 - 日

角色: 小明, 老师

[镜头1] 全景
老师走进教室。

[镜头2] 中景
小明坐在窗边。

[镜头3] 特写
小明看向窗外。
""")

# 获取解析结果
scenes = result["scenes"]
shots = result["shots"]
characters = result["characters"]
```

### 镜头设计

```python
from lib.storyboard import ShotDesigner

designer = ShotDesigner()

# 设计镜头
shot = designer.design_shot(
    scene_type="classroom",
    action="walking",
    emotion="calm",
    shot_size="medium",  # 全景, 中景, 近景, 特写
    camera_angle="eye_level",  # 平视, 俯视, 仰视
    movement="static"  # 固定, 推, 拉, 摇, 移
)

# 获取构图建议
composition = designer.get_composition(
    shot_type=shot,
    aspect_ratio="16:9",
    rule_of_thirds=True
)
```

### 分镜草图生成

```python
from lib.storyboard import SketchGenerator

sketcher = SketchGenerator()

# 生成草图
sketch = sketcher.generate(
    prompt="教室场景，学生坐在窗边，阳光透过窗户",
    style="simple_sketch",  # simple_sketch, detailed, anime
    size=(1920, 1080)
)

# 保存草图
sketch.save("panel_01.png")
```

## 脚本说明

### generate.py - 生成分镜

```bash
python scripts/generate.py [OPTIONS]

选项:
  --script, -s          剧本路径或文本 (必需)
  --output, -o          输出目录 (必需)
  --style, -t           风格 (默认: anime)
  --format, -f          输出格式 (pdf/png, 默认: pdf)
  --num-panels, -n      分镜格数量 (默认: 自动)
  --aspect-ratio        宽高比 (16:9/4:3/1:1, 默认: 16:9)
  --resolution          分辨率 (默认: 1920x1080)
```

### export.py - 导出分镜

```bash
python scripts/export.py [OPTIONS]

选项:
  --input, -i           分镜JSON文件 (必需)
  --output, -o          输出文件 (必需)
  --format, -f          格式 (pdf/png, 默认: pdf)
  --template, -t        模板 (default/anime/comic)
  --quality, -q         质量 (draft/mid/high, 默认: high)
```

## 配置文件

### 模板配置 (configs/templates.yaml)

```yaml
templates:
  default:
    panel_size: [1920, 1080]
    margin: 40
    spacing: 20
    font_size: 16
    show_frame_number: true
    show_action: true
    show_dialogue: true
    
  anime:
    panel_size: [1920, 1080]
    margin: 50
    spacing: 30
    font_size: 18
    show_camera_info: true
    show_timing: true
    style: "anime_storyboard"
    
  comic:
    panel_size: [1200, 1600]
    margin: 30
    spacing: 15
    font_size: 14
    panels_per_page: 4
```

### 镜头语言预设

```yaml
shot_presets:
  establishing_shot:
    shot_size: "wide"
    camera_angle: "high_angle"
    movement: "static"
    duration: 5
    
  character_intro:
    shot_size: "medium"
    camera_angle: "eye_level"
    movement: "static"
    duration: 3
    
  dialogue:
    shot_size: "close_up"
    camera_angle: "eye_level"
    movement: "static"
    duration: 2
    
  action_sequence:
    shot_size: "medium"
    camera_angle: "low_angle"
    movement: "pan"
    duration: 2
```

## 分镜格信息

每个分镜格包含：

| 字段 | 描述 | 示例 |
|------|------|------|
| panel_id | 分镜格编号 | "1-3" (场景1第3格) |
| scene | 场景名称 | "教室" |
| shot_type | 镜头类型 | "中景" |
| camera_angle | 拍摄角度 | "平视" |
| composition | 构图建议 | "三分法" |
| description | 画面描述 | "学生坐在窗边" |
| dialogue | 对话内容 | "小明: 今天天气真好" |
| duration | 预计时长(秒) | 3 |
| notes | 备注 | "阳光从左侧照射" |

## 工作流集成

### 与角色一致性集成

```python
from lib.storyboard import StoryboardGenerator
from lib.character_consistency import CharacterConsistency

# 初始化
storyboard = StoryboardGenerator()
character = CharacterConsistency()

# 加载角色
char_ref = character.load_reference("character_ref.yaml")

# 生成分镜（带角色一致性）
board = storyboard.generate(
    script="剧本内容",
    character_ref=char_ref
)
```

### 与图像生成集成

```python
from lib.storyboard import StoryboardGenerator
from anime_image_generator import AnimeImageGenerator

storyboard = StoryboardGenerator()
generator = AnimeImageGenerator()

# 生成分镜
board = storyboard.generate(script="剧本")

# 生成关键帧
for panel in board.panels:
    image = generator.generate(
        prompt=panel.description,
        style="anime",
        size=(1920, 1080)
    )
    panel.image = image
```

## 导出格式

### PDF导出

```python
# 导出为PDF分镜文档
storyboard.export(
    output="storyboard.pdf",
    format="pdf",
    template="anime",
    include_images=True
)
```

### PNG序列

```python
# 导出为PNG序列
storyboard.export_frames(
    output_dir="panels/",
    format="png",
    quality="high"
)
```

### JSON导出

```python
# 导出为JSON数据
storyboard.export(
    output="storyboard.json",
    format="json"
)
```

## 故障排除

### 常见问题

**剧本解析不准确:**
- 确保剧本格式规范
- 使用场景标记 [场景X]
- 明确标注角色名称

**构图建议不合适:**
- 调整场景类型参数
- 手动覆盖自动建议
- 使用自定义模板

**导出图像质量差:**
- 提高分辨率设置
- 使用高质量模板
- 检查源图像质量

### 性能优化

1. 使用批量处理
2. 缓存解析结果
3. 使用低分辨率预览
4. 并行导出

## 依赖

```
torch>=2.0.0
diffusers>=0.25.0
transformers>=4.35.0
Pillow>=10.0.0
PyYAML>=6.0
reportlab>=4.0.0
jinja2>=3.1.0
numpy>=1.24.0
opencv-python>=4.8.0
```

## 参考资料

- [分镜设计基础](https://en.wikipedia.org/wiki/Storyboard)
- [电影镜头语言](https://www.studiobinder.com/blog/camera-shots-types/)
- [动漫分镜技法](https://www.anime-planet.com/guides/storyboarding)

## 限制

### 当前限制
- 仅支持中文/英文剧本
- 草图为简化版本
- 不支持动画预览

### 计划功能
- [x] 剧本解析
- [x] 镜头设计
- [x] PDF导出
- [ ] 动画预览
- [ ] 协作功能
- [ ] 视频预览
