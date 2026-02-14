"""
Base Rule - Abstract Foundation
All rules inherit from this
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseRule(ABC):
    """
    Abstract base class for all validation rules.
    Every rule MUST implement evaluate().
    """
    
    # Rule metadata (override in subclasses)
    id: str = "BASE"
    severity: str = "INFO"  # INFO | LOW | MEDIUM | HIGH | CRITICAL
    description: str = "Base rule"
    category: str = "GENERAL"
    
    @abstractmethod
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        """
        Evaluate data against this rule.
        
        Args:
            data: System data to validate
            context: Execution context with runtime state
            
        Returns:
            Finding dict if rule fails, None if passes
            Finding format: {
                "id": rule_id,
                "severity": severity_level,
                "message": description,
                "category": category,
                "details": {...}  # optional
            }
        """
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def _create_finding(self, message: str, details: Dict = None) -> Dict:
        """
        Helper to create a standardized finding
        
        Args:
            message: Description of the finding
            details: Optional additional details
            
        Returns:
            Finding dictionary
        """
        finding = {
            "id": self.id,
            "severity": self.severity,
            "message": message,
            "category": self.category,
            "rule": self.__class__.__name__
        }
        
        if details:
            finding["details"] = details
        
        return finding
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} severity={self.severity}>"
