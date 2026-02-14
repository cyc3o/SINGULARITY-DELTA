"""
Analysis Result - Single Source of Truth
Data contract for all analysis outputs
"""
from typing import List, Dict, Optional
from datetime import datetime


class AnalysisResult:
    """
    Immutable result object returned by the engine.
    Contains all findings, scores, and metadata.
    """
    
    def __init__(self):
        self.target: Optional[str] = None
        self.verdict: Optional[str] = None  # PASSED | FAILED
        self.risk: Optional[str] = None     # LOW | MEDIUM | HIGH | CRITICAL
        self.score: float = 100.0
        self.confidence: float = 1.0
        self.findings: List[Dict] = []
        self.engine_version: str = "1.0.0"
        self.timestamp: str = datetime.utcnow().isoformat()
        self.metadata: Dict = {}
    
    def add_finding(self, finding: Dict) -> None:
        """Add a finding to the results"""
        self.findings.append(finding)
    
    def to_dict(self) -> Dict:
        """Export result as dictionary for JSON serialization"""
        return {
            "target": self.target,
            "verdict": self.verdict,
            "risk": self.risk,
            "score": self.score,
            "confidence": self.confidence,
            "findings": self.findings,
            "engine_version": self.engine_version,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    def __repr__(self) -> str:
        return f"<AnalysisResult {self.verdict} score={self.score} findings={len(self.findings)}>"
