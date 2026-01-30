# AI Subtitle Sync

AI字幕同步工具，使用Whisper进行语音识别，自动生成SRT/VTT字幕文件，并支持音画同步和多语言支持。

## 功能特性

- **语音识别 (ASR)**：使用OpenAI Whisper模型
- **字幕生成**：支持SRT/VTT格式
- **时间轴对齐**：精确的音画同步
- **多语言字幕**：支持中文、英文、日文等多语言
- **视频内嵌字幕**：将字幕烧录到视频中

## 快速开始

### 安装依赖

```bash
cd /home/zous/clawd/skills/ai-subtitle-sync
pip install -r requirements.txt
```

### 提取字幕

```bash
# 从视频提取字幕
python scripts/extract.py \
    --input "path/to/video.mp4" \
    --output "path/to/subtitles.srt" \
    --model medium \
    --language zh
```

### 音画同步

```bash
# 调整字幕时间轴
python scripts/sync.py \
    --input "subtitles.srt" \
    --output "subtitles_synced.srt" \
    --offset 1.5 \
    --factor 1.0
```

## 使用方法

### Python API

```python
from lib.subtitle import SubtitleGenerator, SubtitleEditor

# 初始化生成器
generator = SubtitleGenerator(model="medium")

# 从视频生成字幕
subtitles = generator.generate(
    video_path="video.mp4",
    language="zh",
    format="srt"
)

# 保存字幕
generator.save(subtitles, "subtitles.srt")

# 编辑字幕
editor = SubtitleEditor("subtitles.srt")

# 调整时间轴
editor.adjust_timing(offset=1.5, factor=1.0)

# 合并字幕块
editor.merge_lines(max_chars=50)

# 保存编辑后的字幕
editor.save("subtitles_edited.srt")
```

### 批量处理

```python
from lib.subtitle import BatchProcessor

processor = BatchProcessor(model="medium")

# 批量处理多个视频
results = processor.process_batch(
    video_files=["video1.mp4", "video2.mp4"],
    language="zh",
    output_dir="output/"
)

# 生成ASS高级字幕
processor.generate_ass(
    subtitles,
    style={
        "font": "SimHei",
        "size": 24,
        "color": "&H00FFFFFF"
    }
)
```

### 视频内嵌字幕

```python
from lib.subtitle import VideoBurner

burner = VideoBurner()

# 烧录字幕到视频
burner.burn_subtitles(
    video="input.mp4",
    subtitles="subtitles.srt",
    output="output.mp4",
    style={
        "font": "SimHei",
        "size": 24,
        "y": "bottom"
    }
)
```

## 脚本说明

### extract.py - 从视频提取字幕

```bash
python scripts/extract.py [OPTIONS]

选项:
  --input, -i          输入视频路径 (必需)
  --output, -o         输出字幕路径 (必需)
  --model, -m          Whisper模型 (tiny/base/small/medium/large, 默认: medium)
  --language, -l       语言 (zh/en/ja/ko, 默认: auto)
  --format, -f         字幕格式 (srt/vtt/ass, 默认: srt)
  --beam-size          Beam大小 (默认: 5)
  --threads            CPU线程数 (默认: 4)
```

### sync.py - 音画同步

```bash
python scripts/sync.py [OPTIONS]

选项:
  --input, -i          输入字幕路径 (必需)
  --output, -o         输出字幕路径 (必需)
  --offset, -t         时间偏移 (秒, 默认: 0)
  --factor, -s         时间缩放因子 (默认: 1.0)
  --merge, -m          合并短行 (最大字符数, 默认: 50)
  --split, -p          拆分长行 (最大字符数, 默认: 42)
```

## 字幕格式

### SRT格式

```
1
00:00:01,000 --> 00:00:04,000
这是第一条字幕

2
00:00:04,500 --> 00:00:08,000
这是第二条字幕
```

### VTT格式

```
WEBVTT

00:01.000 --> 00:04.000
这是第一条字幕

00:04.500 --> 00:08.000
这是第二条字幕
```

### ASS格式

```
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,这是第一条字幕
Dialogue: 0,0:00:04.50,0:00:08.00,Default,,0,0,0,,这是第二条字幕
```

## 配置文件

### 格式配置 (configs/formats.yaml)

```yaml
formats:
  srt:
    extension: .srt
    time_format: "HH:MM:SS,mmm"
    encoding: utf-8
    
  vtt:
    extension: .vtt
    time_format: "HH:MM:SS.mmm"
    header: "WEBVTT"
    encoding: utf-8
    
  ass:
    extension: .ass
    header: |
      [Script Info]
      ScriptType: v4.00+
      PlayResX: 1920
      PlayResY: 1080
    encoding: utf-8

whisper_models:
  tiny:
    params: 39M
    speed: fastest
    vramb: 1GB
    
  base:
    params: 74M
    speed: very_fast
    vramb: 1GB
    
  small:
    params: 244M
    speed: fast
    vramb: 2GB
    
  medium:
    params: 769M
    speed: medium
    vramb: 5GB
    
  large:
    params: 1550M
    speed: slow
    vramb: 10GB

subtitle_styles:
  default:
    font: "SimHei"
    size: 24
    color: "&H00FFFFFF"
    outline: 2
    
  anime:
    font: "FZMiaoWu"
    size: 28
    color: "&H00FFFFFF"
    outline: 3
    shadow: 1
```

## 工作流集成

### 与视频生成器集成

```python
from lib.subtitle import SubtitleGenerator
from anime_video_generator import VideoGenerator

# 生成视频
video = VideoGenerator()
result = video.generate(
    script="剧本",
    audio="dialogue.wav"
)

# 生成字幕
subtitle = SubtitleGenerator(model="medium")
subs = subtitle.generate(
    video_path=result.path,
    language="zh"
)

# 烧录字幕
burner = VideoBurner()
burner.burn_subtitles(
    video=result.path,
    subtitles=subs,
    output="final_video.mp4"
)
```

### 批量处理

```python
from lib.subtitle import BatchProcessor

processor = BatchProcessor(model="medium")

# 处理整个文件夹
results = processor.process_directory(
    input_dir="videos/",
    output_dir="subtitles/",
    language="zh",
    format="srt"
)
```

## 故障排除

### 常见问题

**识别准确率低:**
- 使用更大的Whisper模型
- 明确指定语言
- 预处理音频（降噪）

**时间轴不同步:**
- 调整offset参数
- 检查视频帧率设置
- 手动校准关键帧

**乱码问题:**
- 确保使用UTF-8编码
- 检查字体支持

### 性能优化

1. 使用GPU加速（transformers版本）
2. 批量处理多个文件
3. 使用small模型加速
4. 启用实时转录

## 依赖

```
openai-whisper>=20231106
torch>=2.0.0
ffmpeg-python>=0.2.0
numpy>=1.24.0
Pillow>=10.0.0
PyYAML>=6.0
ass>=0.6.0
```

## 参考资料

- [OpenAI Whisper](https://github.com/openai/whisper)
- [SRT格式规范](https://www.matroska.org/technical/specs/subtitles/srt.html)
- [WebVTT格式](https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API)
- [ASS字幕格式](https://docs.aegisub.org/master/ASS_Tags/)

## 限制

### 当前限制
- 需要ffmpeg支持
- 长视频需要更多内存
- 暂不支持说话人分离

### 计划功能
- [x] Whisper ASR支持
- [x] SRT/VTT导出
- [x] 视频烧录
- [ ] 说话人分离
- [ ] 实时字幕
- [ ] 翻译集成
