#!/usr/bin/env python3
"""
Quality Assessment Module

Features:
- Content scoring
- A/B test support
- Engagement prediction
- Continuous improvement tracking
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class QualityScore:
    """Content quality score"""
    overall: float  # 0-100
    readability: float  # 0-100
    engagement: float  # 0-100
    seo: float  # 0-100
    structure: float  # 0-100
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class QualityAssessor:
    """Assess content quality"""
    
    def __init__(self):
        self.scores_history: List[Dict] = []
    
    def assess(self, title: str, content: str, expected_keywords: List[str] = None) -> QualityScore:
        """Comprehensive quality assessment"""
        issues = []
        suggestions = []
        
        # Readability score (Flesch-Kincaid simplified)
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        avg_sentence_length = words / max(sentences, 1)
        
        readability = 100 - (avg_sentence_length * 3)
        readability = max(0, min(100, readability))
        
        if avg_sentence_length > 25:
            issues.append("Sentences too long (avg > 25 words)")
            suggestions.append("Split long sentences into shorter ones")
        
        # Engagement score
        engagement = 100
        
        # Hook check (first 100 chars)
        hook = content[:100].lower()
        if any(word in hook for word in ["今天", "大家好", "嗨", "hello", "hi"]):
            engagement += 10
        else:
            issues.append("Weak opening hook")
            suggestions.append("Start with a hook in first 100 characters")
        
        # Emotion words
        emotion_words = ["竟然", "太棒了", "震惊", "后悔", "惊喜", "amazing", "wow", "shocking"]
        emotion_count = sum(1 for w in emotion_words if w in content.lower())
        engagement += min(emotion_count * 5, 20)
        
        # SEO score
        seo = 80
        
        if title:
            if len(title) < 20:
                issues.append("Title too short")
                suggestions.append("Title should be 30-60 characters")
            elif len(title) > 80:
                issues.append("Title too long")
                suggestions.append("Shorten title to under 80 characters")
            else:
                seo += 10
        
        if expected_keywords:
            content_lower = content.lower()
            found = sum(1 for kw in expected_keywords if kw.lower() in content_lower)
            keyword_coverage = found / len(expected_keywords)
            seo += keyword_coverage * 20
            if keyword_coverage < 0.5:
                issues.append(f"Low keyword coverage ({keyword_coverage*100:.0f}%)")
                suggestions.append(f"Include more keywords: {expected_keywords}")
        
        # Structure score
        structure = 70
        
        h2_count = content.count("## ")
        if h2_count < 2:
            issues.append("Too few subheadings")
            suggestions.append("Add at least 2-3 h2 subheadings")
        elif h2_count >= 3:
            structure += 20
        else:
            structure += 10
        
        # Check for conclusion
        conclusion_words = ["总结", "总之", "最后", "conclusion", "finally", "in summary"]
        if any(word in content.lower() for word in conclusion_words):
            structure += 10
        else:
            issues.append("Missing conclusion section")
            suggestions.append("Add a summary/conclusion section")
        
        # Calculate overall
        overall = (readability * 0.25 + 
                  engagement * 0.25 + 
                  seo * 0.25 + 
                  structure * 0.25)
        
        return QualityScore(
            overall=overall,
            readability=readability,
            engagement=engagement,
            seo=seo,
            structure=structure,
            issues=issues,
            suggestions=suggestions,
        )
    
    def compare_versions(self, version_a: Dict, version_b: Dict) -> Dict:
        """Compare two content versions"""
        score_a = self.assess(version_a.get("title", ""), version_a.get("body", ""))
        score_b = self.assess(version_b.get("title", ""), version_b.get("body", ""))
        
        improvement = {
            "version_a_score": score_a.overall,
            "version_b_score": score_b.overall,
            "winner": "B" if score_b.overall > score_a.overall else "A",
            "improvement": abs(score_b.overall - score_a.overall),
            "version_a_issues": score_a.issues,
            "version_b_issues": score_b.issues,
        }
        
        return improvement
    
    def get_improvement_suggestions(self, score: QualityScore) -> List[str]:
        """Get prioritized improvement suggestions"""
        suggestions = []
        
        # Priority 1: Structure
        if score.structure < 70:
            suggestions.append("🔴 Priority: Fix structure (add subheadings, conclusion)")
        
        # Priority 2: Readability
        if score.readability < 60:
            suggestions.append("🟠 Priority: Improve readability (shorten sentences)")
        
        # Priority 3: Engagement
        if score.engagement < 70:
            suggestions.append("🟡 Medium: Add emotional hooks and calls-to-action")
        
        # Priority 4: SEO
        if score.seo < 70:
            suggestions.append("🟢 Low: Optimize keywords and title length")
        
        return suggestions


class ABTestTracker:
    """Track A/B test results"""
    
    def __init__(self):
        self.experiments: Dict[str, List[Dict]] = defaultdict(list)
    
    def start_experiment(self, experiment_name: str, content_a: Dict, content_b: Dict):
        """Start an A/B test"""
        assessor = QualityAssessor()
        comparison = assessor.compare_versions(content_a, content_b)
        
        experiment = {
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "comparison": comparison,
            "versions": {
                "A": {"content": content_a, "score": comparison["version_a_score"]},
                "B": {"content": content_b, "score": comparison["version_b_score"]},
            },
        }
        
        self.experiments[experiment_name].append(experiment)
        return experiment
    
    def record_result(self, experiment_name: str, winner: str, metrics: Dict = None):
        """Record actual engagement metrics"""
        if experiment_name in self.experiments and self.experiments[experiment_name]:
            exp = self.experiments[experiment_name][-1]
            exp["status"] = "completed"
            exp["winner"] = winner
            exp["metrics"] = metrics or {}
            exp["completed_at"] = datetime.now().isoformat()
    
    def get_best_practices(self, experiment_name: str) -> List[str]:
        """Extract best practices from completed experiments"""
        practices = []
        
        if experiment_name in self.experiments:
            for exp in self.experiments[experiment_name]:
                if exp["status"] == "completed":
                    winner = exp.get("winner")
                    if winner and winner in exp["versions"]:
                        winner_issues = exp["versions"][winner].get("issues", [])
                        practices.extend(winner_issues)
        
        return list(set(practices)) if practices else []


if __name__ == "__main__":
    assessor = QualityAssessor()
    tracker = ABTestTracker()
    
    # Test assessment
    test_content = """
    # AI Agent 开发实战

    大家好！今天我们来聊聊 AI Agent。

    ## 什么是 AI Agent

    AI Agent 是一个能够自主决策和执行任务的系统。

    ## 如何构建

    构建 AI Agent 需要以下步骤：
    1. 定义目标
    2. 选择模型
    3. 实现工具调用
    4. 添加记忆

    ## 总结

    AI Agent 开发需要不断迭代和优化。
    """
    
    score = assessor.assess(
        "AI Agent 开发实战",
        test_content,
        expected_keywords=["AI", "Agent", "开发"]
    )
    
    print(f"\n📊 Quality Assessment:")
    print(f"   Overall: {score.overall:.1f}/100")
    print(f"   Readability: {score.readability:.1f}/100")
    print(f"   Engagement: {score.engagement:.1f}/100")
    print(f"   SEO: {score.seo:.1f}/100")
    print(f"   Structure: {score.structure:.1f}/100")
    
    if score.issues:
        print(f"\n⚠️ Issues:")
        for issue in score.issues:
            print(f"   - {issue}")
    
    if score.suggestions:
        print(f"\n💡 Suggestions:")
        for suggestion in score.suggestions:
            print(f"   - {suggestion}")
