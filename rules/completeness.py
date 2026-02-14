"""
Completeness Rules
Validates presence of required fields and data
"""
from typing import Dict, Any, Optional, List
from .base_rule import BaseRule


class CompletenessRule(BaseRule):
    """Validates that all required keys are present"""
    
    id = "AX-001"
    severity = "HIGH"
    description = "Missing required keys in system data"
    category = "COMPLETENESS"
    
    REQUIRED_KEYS = ["system_name", "decisions", "constraints"]
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        missing = [k for k in self.REQUIRED_KEYS if k not in data]
        
        if missing:
            return self._create_finding(
                f"Missing required keys: {', '.join(missing)}",
                details={"missing_keys": missing, "required_keys": self.REQUIRED_KEYS}
            )
        
        return None


class DecisionCompletenessRule(BaseRule):
    """Validates that decisions list is not empty"""
    
    id = "AX-002"
    severity = "HIGH"
    description = "Decisions list is empty or missing"
    category = "COMPLETENESS"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        if "decisions" not in data:
            return self._create_finding(
                "Decisions field is missing",
                details={"field": "decisions"}
            )
        
        decisions = data.get("decisions", [])
        
        if not isinstance(decisions, list):
            return self._create_finding(
                "Decisions must be a list",
                details={"actual_type": type(decisions).__name__}
            )
        
        if len(decisions) == 0:
            return self._create_finding(
                "Decisions list is empty - system has no decisions defined",
                details={"count": 0}
            )
        
        return None


class ConstraintCompletenessRule(BaseRule):
    """Validates that constraints are properly defined"""
    
    id = "AX-003"
    severity = "MEDIUM"
    description = "Constraints are missing or improperly defined"
    category = "COMPLETENESS"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        constraints = data.get("constraints", {})
        
        if not isinstance(constraints, dict):
            return self._create_finding(
                "Constraints must be a dictionary",
                details={"actual_type": type(constraints).__name__}
            )
        
        if len(constraints) == 0:
            return self._create_finding(
                "No constraints defined - system is unconstrained",
                details={"constraint_count": 0}
            )
        
        return None


class MetadataCompletenessRule(BaseRule):
    """Validates essential metadata presence"""
    
    id = "AX-004"
    severity = "LOW"
    description = "Missing recommended metadata fields"
    category = "COMPLETENESS"
    
    RECOMMENDED_METADATA = ["version", "created", "author"]
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        metadata = data.get("metadata", {})
        
        if not metadata:
            return self._create_finding(
                "No metadata section found",
                details={"recommended_fields": self.RECOMMENDED_METADATA}
            )
        
        missing = [k for k in self.RECOMMENDED_METADATA if k not in metadata]
        
        if missing:
            return self._create_finding(
                f"Missing recommended metadata: {', '.join(missing)}",
                details={"missing_fields": missing}
            )
        
        return None
