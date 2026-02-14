"""
SINGULARITY DELTA ENGINE
DETERMINISTIC POLICY VERIFICATION ENGINE
NO UI. NO INPUT. PURE LOGIC.
"""
import time
from typing import List, Dict, Any
from .result import AnalysisResult
from .context import ExecutionContext


class Engine:
    """
    CORE ANALYSIS ENGINE.
    EXECUTES RULES AND AGGREGATES RESULTS DETERMINISTICALLY.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, rules: List = None):
        """
        INITIALIZE ENGINE WITH RULE SET
        
        Args:
            rules: List of rule instances to execute
        """
        self.rules = rules or []
        self.context = ExecutionContext()
        print(f"\n🔧 ENGINE INITIALIZED", flush=True)
        print(f"📋 LOADED {len(self.rules)} RULES", flush=True)
        time.sleep(0.3)
    
    def run(self, data: Dict[str, Any], target: str = "unknown") -> AnalysisResult:
        """
        EXECUTE ALL RULES AGAINST DATA AND RETURN ANALYSIS RESULT.
        
        Args:
            data: System data to analyze
            target: Name/identifier of the target system
            
        Returns:
            AnalysisResult object with verdict, score, and findings
        """
        print(f"\n⚡ STARTING ANALYSIS ENGINE...", flush=True)
        print(f"🎯 TARGET: {target.upper()}", flush=True)
        time.sleep(0.4)
        
        result = AnalysisResult()
        result.target = target
        result.engine_version = self.VERSION
        
        # EXECUTE EACH RULE
        print(f"\n🔍 EXECUTING VALIDATION RULES...", flush=True)
        time.sleep(0.3)
        
        rule_categories = {}
        for rule in self.rules:
            category = getattr(rule, 'category', 'GENERAL')
            rule_categories[category] = rule_categories.get(category, 0) + 1
        
        for category, count in rule_categories.items():
            print(f"   ✓ {category}: {count} RULES", flush=True)
            time.sleep(0.15)
        
        print(f"\n⚙️  PROCESSING...", flush=True)
        time.sleep(0.5)
        
        for i, rule in enumerate(self.rules, 1):
            try:
                finding = rule.evaluate(data, self.context)
                if finding:
                    result.add_finding(finding)
                    severity = finding.get('severity', 'UNKNOWN')
                    emoji = self._get_severity_emoji(severity)
                    print(f"   {emoji} FINDING: {severity} [{finding.get('id', 'N/A')}]", flush=True)
                    time.sleep(0.1)
            except Exception as e:
                # LOG RULE EXECUTION FAILURE
                result.add_finding({
                    "id": "ENGINE-ERROR",
                    "severity": "CRITICAL",
                    "rule": rule.id if hasattr(rule, 'id') else str(rule),
                    "message": f"RULE EXECUTION FAILED: {str(e)}"
                })
                print(f"   ❌ ERROR IN RULE: {rule.id if hasattr(rule, 'id') else 'UNKNOWN'}", flush=True)
                time.sleep(0.1)
        
        # FINALIZE VERDICT AND SCORING
        print(f"\n🧮 CALCULATING FINAL VERDICT...", flush=True)
        time.sleep(0.4)
        
        self._finalize(result)
        
        print(f"✅ ANALYSIS COMPLETE!", flush=True)
        time.sleep(0.2)
        
        return result
    
    def _get_severity_emoji(self, severity: str) -> str:
        """GET EMOJI FOR SEVERITY LEVEL"""
        emoji_map = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': '💡',
            'INFO': 'ℹ️'
        }
        return emoji_map.get(severity, '•')
    
    def _finalize(self, result: AnalysisResult) -> None:
        """
        CALCULATE FINAL VERDICT, RISK LEVEL, AND SCORE BASED ON FINDINGS.
        
        Args:
            result: AnalysisResult to finalize
        """
        # COUNT SEVERITY LEVELS
        critical_count = sum(1 for f in result.findings if f.get("severity") == "CRITICAL")
        high_count = sum(1 for f in result.findings if f.get("severity") == "HIGH")
        medium_count = sum(1 for f in result.findings if f.get("severity") == "MEDIUM")
        low_count = sum(1 for f in result.findings if f.get("severity") == "LOW")
        
        # CALCULATE SCORE PENALTIES
        score_penalty = 0
        score_penalty += critical_count * 40  # -40 PER CRITICAL
        score_penalty += high_count * 20      # -20 PER HIGH
        score_penalty += medium_count * 10    # -10 PER MEDIUM
        score_penalty += low_count * 5        # -5 PER LOW
        
        result.score = max(0, 100 - score_penalty)
        
        # DETERMINE VERDICT AND RISK LEVEL
        if critical_count > 0:
            result.verdict = "FAILED"
            result.risk = "CRITICAL"
            result.confidence = 1.0
            print(f"   🚨 CRITICAL ISSUES DETECTED: {critical_count}", flush=True)
        elif high_count > 0:
            result.verdict = "FAILED"
            result.risk = "HIGH"
            result.confidence = 0.95
            print(f"   ⚠️  HIGH SEVERITY ISSUES: {high_count}", flush=True)
        elif medium_count > 0:
            result.verdict = "WARNING"
            result.risk = "MEDIUM"
            result.confidence = 0.85
            print(f"   ⚡ MEDIUM ISSUES DETECTED: {medium_count}", flush=True)
        elif low_count > 0:
            result.verdict = "PASSED"
            result.risk = "LOW"
            result.confidence = 0.90
            print(f"   💡 MINOR ISSUES FOUND: {low_count}", flush=True)
        else:
            result.verdict = "PASSED"
            result.risk = "NONE"
            result.confidence = 1.0
            print(f"   ✨ NO ISSUES DETECTED - PERFECT!", flush=True)
        
        time.sleep(0.2)
        
        # STORE METADATA
        result.metadata = {
            "total_findings": len(result.findings),
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "rules_executed": len(self.rules)
        }
    
    def add_rule(self, rule) -> None:
        """ADD A RULE TO THE ENGINE"""
        self.rules.append(rule)
    
    def __repr__(self) -> str:
        return f"<ENGINE v{self.VERSION} RULES={len(self.rules)}>"
