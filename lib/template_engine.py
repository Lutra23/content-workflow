#!/usr/bin/env python3
"""
Template Engine for Content Factory

Features:
- YAML template loading
- Variable substitution
- Template validation
- Quality checks
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Template:
    """Content template"""
    name: str
    description: str
    model: str
    temperature: float
    max_tokens: int
    system_prompt: str
    prompt_template: str
    quality_checks: Dict = None


class TemplateEngine:
    """Template management and rendering engine"""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all YAML templates"""
        yaml_file = self.template_dir / "content.yaml"
        if not yaml_file.exists():
            print(f"⚠️ Template file not found: {yaml_file}")
            return
        
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        for name, tpl_data in data.get("templates", {}).items():
            template = Template(
                name=tpl_data["name"],
                description=tpl_data.get("description", ""),
                model=tpl_data.get("model", "llama-3.3-70b-versatile"),
                temperature=tpl_data.get("temperature", 0.7),
                max_tokens=tpl_data.get("max_tokens", 2000),
                system_prompt=tpl_data.get("system_prompt", ""),
                prompt_template=tpl_data.get("prompt_template", ""),
                quality_checks=tpl_data.get("quality_checks", {}),
            )
            self.templates[name] = template
        
        print(f"✅ Loaded {len(self.templates)} templates")
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def get_template(self, name: str) -> Optional[Template]:
        """Get a template by name"""
        return self.templates.get(name)
    
    def render(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render a template with variables"""
        template = self.get_template(template_name)
        if not template:
            return f"[Template not found: {template_name}]"
        
        prompt = template.prompt_template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            prompt = prompt.replace(placeholder, str(value))
        
        return prompt
    
    def render_system_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render system prompt with variables"""
        template = self.get_template(template_name)
        if not template:
            return ""
        
        prompt = template.system_prompt
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            prompt = prompt.replace(placeholder, str(value))
        
        return prompt
    
    def get_template_config(self, template_name: str) -> Dict:
        """Get template configuration for AI client"""
        template = self.get_template(template_name)
        if not template:
            return {}
        
        return {
            "model": template.model,
            "temperature": template.temperature,
            "max_tokens": template.max_tokens,
        }
    
    def validate_output(self, template_name: str, content: str) -> Dict:
        """Validate generated content against quality checks"""
        template = self.get_template(template_name)
        if not template or not template.quality_checks:
            return {"valid": True, "reason": "No quality checks defined"}
        
        checks = template.quality_checks
        issues = []
        
        # Word count check
        word_count = len(content.split())
        if "min_word_count" in checks and word_count < checks["min_word_count"]:
            issues.append(f"Word count ({word_count}) below minimum ({checks['min_word_count']})")
        if "max_word_count" in checks and word_count > checks["max_word_count"]:
            issues.append(f"Word count ({word_count}) above maximum ({checks['max_word_count']})")
        
        # Section check
        required = checks.get("required_sections", [])
        for section in required:
            if section.lower() not in content.lower():
                issues.append(f"Missing section: {section}")
        
        # Forbidden phrases
        forbidden = checks.get("forbidden", [])
        for phrase in forbidden:
            if phrase.lower() in content.lower():
                issues.append(f"Contains forbidden phrase: {phrase}")
        
        return {
            "valid": len(issues) == 0,
            "reason": "; ".join(issues) if issues else "Passed all checks",
            "word_count": word_count,
        }
    
    def suggest_template(self, content_type: str, audience: str = "general") -> str:
        """Suggest best template based on content type and audience"""
        type_mapping = {
            "article": ["article_professional", "article_viral"],
            "video": ["video_script_3min"],
            "social": ["thread_x"],
        }
        
        candidates = type_mapping.get(content_type, list(self.templates.keys()))
        
        # Prefer professional for technical audiences
        if "technical" in audience.lower() or "developer" in audience.lower():
            for c in candidates:
                if "professional" in c:
                    return c
        
        return candidates[0] if candidates else "article_professional"


if __name__ == "__main__":
    engine = TemplateEngine()
    
    print("\n📋 Available Templates:")
    for name in engine.list_templates():
        tpl = engine.get_template(name)
        print(f"  - {name}: {tpl.description}")
    
    # Test rendering
    print("\n🧪 Test render:")
    prompt = engine.render("article_professional", {
        "topic": "AI Agent 开发",
        "keywords": "AI, Agent, 自动化",
        "audience": "技术开发者",
        "references": "官方文档",
    })
    print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
