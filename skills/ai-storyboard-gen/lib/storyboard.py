"""
Storyboard Generator Module

提供分镜生成功能，包括剧本解析、镜头设计和导出。
"""

import os
import json
import yaml
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image
import numpy as np


@dataclass
class Panel:
    """分镜格数据类"""
    panel_id: str
    scene: str
    shot_type: str = "medium"  # wide/medium/close_up/extreme_close_up
    camera_angle: str = "eye_level"  # eye_level/high_angle/low_angle
    camera_movement: str = "static"  # static/pan/tilt/dolly/zoom
    composition: str = "center"
    description: str = ""
    dialogue: str = ""
    duration: float = 3.0
    notes: str = ""
    image: Optional[Image.Image] = None
    
    def to_dict(self) -> dict:
        return {
            "panel_id": self.panel_id,
            "scene": self.scene,
            "shot_type": self.shot_type,
            "camera_angle": self.camera_angle,
            "camera_movement": self.camera_movement,
            "composition": self.composition,
            "description": self.description,
            "dialogue": self.dialogue,
            "duration": self.duration,
            "notes": self.notes
        }


@dataclass
class Storyboard:
    """分镜数据类"""
    title: str
    panels: List[Panel] = field(default_factory=list)
    aspect_ratio: str = "16:9"
    resolution: Tuple[int, int] = (1920, 1080)
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "aspect_ratio": self.aspect_ratio,
            "resolution": self.resolution,
            "panels": [p.to_dict() for p in self.panels]
        }
    
    def export(
        self,
        output: str,
        format: str = "json",
        **kwargs
    ):
        """导出分镜"""
        if format == "json":
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        # TODO: PDF/PNG导出实现


class ScriptParser:
    """剧本解析器"""
    
    SCENE_MARKERS = ['场景', 'Scene', 'S']
    SHOT_MARKERS = ['镜头', 'Shot', '画面']
    
    def __init__(self):
        self.characters = set()
        self.scenes = []
        
    def parse(self, script: str) -> Dict:
        """解析剧本文本
        
        Args:
            script: 剧本文本
            
        Returns:
            解析结果字典
        """
        lines = script.strip().split('\n')
        
        result = {
            "scenes": [],
            "shots": [],
            "characters": [],
            "dialogues": []
        }
        
        current_scene = None
        current_shot = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测场景
            if self._is_scene_marker(line):
                current_scene = self._parse_scene(line)
                result["scenes"].append(current_scene)
                
            # 检测镜头
            elif self._is_shot_marker(line):
                current_shot = self._parse_shot(line, current_scene)
                result["shots"].append(current_shot)
                
            # 检测对话
            elif ':' in line and current_shot:
                dialogue = self._parse_dialogue(line)
                result["dialogues"].append(dialogue)
                current_shot["description"] += f"\n{dialogue}"
                
        return result
    
    def _is_scene_marker(self, line: str) -> bool:
        """检查是否为场景标记"""
        return any(marker in line for marker in self.SCENE_MARKERS)
    
    def _is_shot_marker(self, line: str) -> bool:
        """检查是否为镜头标记"""
        return any(marker in line for marker in self.SHOT_MARKERS)
    
    def _parse_scene(self, line: str) -> Dict:
        """解析场景"""
        return {
            "name": line,
            "location": "",
            "time": "",
            "shots": []
        }
    
    def _parse_shot(self, line: str, scene: Optional[Dict]) -> Dict:
        """解析镜头"""
        return {
            "shot_id": line,
            "scene": scene["name"] if scene else "",
            "type": "medium",
            "description": line,
            "dialogue": ""
        }
    
    def _parse_dialogue(self, line: str) -> Dict:
        """解析对话"""
        if ':' in line:
            parts = line.split(':', 1)
            return {
                "character": parts[0].strip(),
                "text": parts[1].strip()
            }
        return {"character": "", "text": line}
    
    def parse_from_file(self, path: str) -> Dict:
        """从文件解析剧本"""
        with open(path, 'r', encoding='utf-8') as f:
            return self.parse(f.read())


class ShotDesigner:
    """镜头设计师"""
    
    SHOT_TYPES = {
        "establishing": {"size": "wide", "angle": "high_angle", "movement": "static"},
        "character": {"size": "medium", "angle": "eye_level", "movement": "static"},
        "dialogue": {"size": "close_up", "angle": "eye_level", "movement": "static"},
        "action": {"size": "medium", "angle": "low_angle", "movement": "pan"},
        "detail": {"size": "extreme_close_up", "angle": "eye_level", "movement": "static"}
    }
    
    def design_shot(
        self,
        scene_type: str = "",
        action: str = "",
        emotion: str = "",
        shot_size: str = "medium",
        camera_angle: str = "eye_level",
        camera_movement: str = "static"
    ) -> Dict:
        """设计镜头参数
        
        Args:
            scene_type: 场景类型
            action: 动作类型
            emotion: 情绪
            shot_size: 景别
            camera_angle: 拍摄角度
            camera_movement: 运镜方式
            
        Returns:
            镜头参数字典
        """
        # 基于场景类型调整
        preset = self.SHOT_TYPES.get(shot_size, {})
        
        return {
            "shot_size": shot_size,
            "camera_angle": camera_angle,
            "camera_movement": camera_movement,
            "scene_type": scene_type,
            "action": action,
            "emotion": emotion,
            **preset
        }
    
    def get_composition(
        self,
        shot_type: Dict,
        aspect_ratio: str = "16:9",
        rule_of_thirds: bool = True
    ) -> Dict:
        """获取构图建议
        
        Args:
            shot_type: 镜头参数
            aspect_ratio: 宽高比
            rule_of_thirds: 是否使用三分法
            
        Returns:
            构图建议字典
        """
        return {
            "rule_of_thirds": rule_of_thirds,
            "focal_point": self._get_focal_point(shot_type),
            "leading_lines": self._get_leading_lines(shot_type),
            "headroom": self._get_headroom(shot_type),
            "look_room": self._get_look_room(shot_type)
        }
    
    def _get_focal_point(self, shot_type: Dict) -> Tuple[int, int]:
        """获取焦点位置"""
        if shot_type.get("camera_angle") == "high_angle":
            return (50, 70)  # 下方
        elif shot_type.get("camera_angle") == "low_angle":
            return (50, 30)  # 上方
        return (50, 50)  # 中心
    
    def _get_leading_lines(self, shot_type: Dict) -> List:
        """获取引导线建议"""
        return []
    
    def _get_headroom(self, shot_type: Dict) -> int:
        """获取头部空间"""
        sizes = {
            "wide": 15,
            "medium": 20,
            "close_up": 10,
            "extreme_close_up": 5
        }
        return sizes.get(shot_type.get("shot_size", "medium"), 15)
    
    def _get_look_room(self, shot_type: Dict) -> str:
        """获取视线空间"""
        if shot_type.get("camera_movement") in ["pan", "dolly"]:
            return "movement_direction"
        return "dialogue_direction"


class SketchGenerator:
    """草图生成器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        
    def generate(
        self,
        prompt: str,
        style: str = "simple_sketch",
        size: Tuple[int, int] = (1920, 1080)
    ) -> Image.Image:
        """生成分镜草图
        
        Args:
            prompt: 场景描述
            style: 风格
            size: 图像尺寸
            
        Returns:
            PIL图像
        """
        # 创建空白画布
        image = Image.new('RGB', size, (255, 255, 255))
        # TODO: 实现实际草图生成逻辑
        return image
    
    def generate_thumbnail(
        self,
        prompt: str,
        size: Tuple[int, int] = (320, 180)
    ) -> Image.Image:
        """生成缩略图"""
        return self.generate(prompt, "simple_sketch", size)


class StoryboardGenerator:
    """分镜生成器主类"""
    
    def __init__(self, config_path: str = "configs/templates.yaml"):
        """初始化"""
        self.config = self._load_config(config_path)
        self.parser = ScriptParser()
        self.designer = ShotDesigner()
        self.sketcher = SketchGenerator()
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def generate(
        self,
        script: str,
        num_panels: Optional[int] = None,
        style: str = "anime",
        aspect_ratio: str = "16:9"
    ) -> Storyboard:
        """从剧本生成分镜
        
        Args:
            script: 剧本文本
            num_panels: 分镜格数量 (None=自动)
            style: 风格
            aspect_ratio: 宽高比
            
        Returns:
            Storyboard对象
        """
        # 解析剧本
        parsed = self.parser.parse(script)
        
        # 获取分辨率
        resolution = self._get_resolution(aspect_ratio)
        
        # 创建分镜
        storyboard = Storyboard(
            title="Generated Storyboard",
            aspect_ratio=aspect_ratio,
            resolution=resolution
        )
        
        # 生成面板
        scene_idx = 1
        panel_idx = 1
        
        for shot in parsed.get("shots", []):
            panel = self._create_panel(
                shot=shot,
                scene_idx=scene_idx,
                panel_idx=panel_idx,
                style=style
            )
            storyboard.panels.append(panel)
            
            panel_idx += 1
            if panel_idx > num_panels:
                break
                
        return storyboard
    
    def generate_from_file(
        self,
        script_path: str,
        style: str = "anime",
        format: str = "long"
    ) -> Storyboard:
        """从文件生成分镜"""
        with open(script_path, 'r', encoding='utf-8') as f:
            return self.generate(f.read(), style=style)
    
    def _create_panel(
        self,
        shot: Dict,
        scene_idx: int,
        panel_idx: int,
        style: str
    ) -> Panel:
        """创建分镜格"""
        shot_design = self.designer.design_shot(
            shot_type=shot.get("type", "medium")
        )
        
        return Panel(
            panel_id=f"{scene_idx}-{panel_idx}",
            scene=shot.get("scene", f"场景{scene_idx}"),
            shot_type=shot_design.get("shot_size", "medium"),
            camera_angle=shot_design.get("camera_angle", "eye_level"),
            camera_movement=shot_design.get("camera_movement", "static"),
            description=shot.get("description", ""),
            dialogue=shot.get("dialogue", ""),
            duration=3.0
        )
    
    def _get_resolution(self, aspect_ratio: str) -> Tuple[int, int]:
        """获取分辨率"""
        ratios = {
            "16:9": (1920, 1080),
            "4:3": (1440, 1080),
            "1:1": (1080, 1080),
            "9:16": (1080, 1920)
        }
        return ratios.get(aspect_ratio, (1920, 1080))
