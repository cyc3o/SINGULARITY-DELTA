"""
Scoring Service
Advanced scoring and risk calculation utilities
"""
from typing import Dict, List


class Scorer:
    """
    Provides advanced scoring algorithms and risk assessment.
    Can be extended for custom scoring strategies.
    """
    
    # Severity weights for scoring
    SEVERITY_WEIGHTS = {
        "CRITICAL": 40,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5,
        "INFO": 1
    }
    
    @staticmethod
    def calculate_weighted_score(findings: List[Dict], base_score: float = 100.0) -> float:
        """
        Calculate score with weighted penalties.
        
        Args:
            findings: List of finding dictionaries
            base_score: Starting score (default 100)
            
        Returns:
            Final weighted score
        """
        penalty = 0
        
        for finding in findings:
            severity = finding.get("severity", "INFO")
            weight = Scorer.SEVERITY_WEIGHTS.get(severity, 1)
            penalty += weight
        
        return max(0.0, base_score - penalty)
    
    @staticmethod
    def calculate_risk_level(findings: List[Dict]) -> str:
        """
        Determine risk level based on findings.
        
        Args:
            findings: List of finding dictionaries
            
        Returns:
            Risk level: CRITICAL | HIGH | MEDIUM | LOW | NONE
        """
        if not findings:
            return "NONE"
        
        severities = [f.get("severity", "INFO") for f in findings]
        
        if "CRITICAL" in severities:
            return "CRITICAL"
        elif "HIGH" in severities:
            return "HIGH"
        elif "MEDIUM" in severities:
            return "MEDIUM"
        elif "LOW" in severities:
            return "LOW"
        else:
            return "NONE"
    
    @staticmethod
    def calculate_confidence(findings: List[Dict], total_rules: int) -> float:
        """
        Calculate confidence in the analysis.
        
        Args:
            findings: List of finding dictionaries
            total_rules: Total number of rules executed
            
        Returns:
            Confidence score between 0 and 1
        """
        if total_rules == 0:
            return 0.0
        
        # Base confidence
        base_confidence = 1.0
        
        # Reduce confidence based on severity distribution
        critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL")
        
        if critical_count > 0:
            # High confidence in failure
            return 1.0
        
        # Lower confidence if many different severity levels
        unique_severities = len(set(f.get("severity") for f in findings))
        confidence_penalty = unique_severities * 0.05
        
        return max(0.5, base_confidence - confidence_penalty)
    
    @staticmethod
    def get_severity_distribution(findings: List[Dict]) -> Dict[str, int]:
        """
        Get count of findings by severity.
        
        Args:
            findings: List of finding dictionaries
            
        Returns:
            Dictionary mapping severity to count
        """
        distribution = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0
        }
        
        for finding in findings:
            severity = finding.get("severity", "INFO")
            if severity in distribution:
                distribution[severity] += 1
        
        return distribution
    
    @staticmethod
    def calculate_health_score(score: float) -> str:
        """
        Convert numeric score to health rating.
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Health rating: EXCELLENT | GOOD | FAIR | POOR | CRITICAL
        """
        if score >= 90:
            return "EXCELLENT"
        elif score >= 75:
            return "GOOD"
        elif score >= 60:
            return "FAIR"
        elif score >= 40:
            return "POOR"
        else:
            return "CRITICAL"
