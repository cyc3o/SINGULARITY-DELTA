"""
Structure Rules
Validates the structural integrity and format of the system
"""
from typing import Dict, Any, Optional
from .base_rule import BaseRule


class DecisionStructureRule(BaseRule):
    """Validates that each decision has required structure"""
    
    id = "SX-001"
    severity = "HIGH"
    description = "Decision missing required fields"
    category = "STRUCTURE"
    
    REQUIRED_FIELDS = ["id", "description"]
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        
        invalid_decisions = []
        
        for i, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                invalid_decisions.append(f"Decision at index {i} is not a dictionary")
                continue
            
            missing = [f for f in self.REQUIRED_FIELDS if f not in decision]
            if missing:
                decision_id = decision.get("id", f"index_{i}")
                invalid_decisions.append(
                    f"Decision '{decision_id}' missing: {', '.join(missing)}"
                )
        
        if invalid_decisions:
            return self._create_finding(
                "Decisions with structural violations found",
                details={"violations": invalid_decisions}
            )
        
        return None


class NestedDepthRule(BaseRule):
    """Validates that nesting depth is reasonable"""
    
    id = "SX-002"
    severity = "MEDIUM"
    description = "Excessive nesting depth detected"
    category = "STRUCTURE"
    
    MAX_DEPTH = 5
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        max_depth = self._calculate_depth(data)
        
        if max_depth > self.MAX_DEPTH:
            return self._create_finding(
                f"Nesting depth {max_depth} exceeds maximum {self.MAX_DEPTH}",
                details={"max_depth": max_depth, "limit": self.MAX_DEPTH}
            )
        
        return None
    
    def _calculate_depth(self, obj, current_depth=1):
        """Recursively calculate maximum nesting depth"""
        if not isinstance(obj, (dict, list)):
            return current_depth
        
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(
                self._calculate_depth(v, current_depth + 1)
                for v in obj.values()
            )
        else:  # list
            if not obj:
                return current_depth
            return max(
                self._calculate_depth(item, current_depth + 1)
                for item in obj
            )


class ConstraintStructureRule(BaseRule):
    """Validates constraint structure"""
    
    id = "SX-003"
    severity = "MEDIUM"
    description = "Malformed constraint structure"
    category = "STRUCTURE"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        constraints = data.get("constraints", {})
        
        if not isinstance(constraints, dict):
            return None  # Type checking handled elsewhere
        
        malformed = []
        
        for name, constraint in constraints.items():
            if isinstance(constraint, dict):
                # Check for common constraint fields
                if "type" not in constraint and "applies_to" not in constraint:
                    malformed.append(
                        f"Constraint '{name}' has no 'type' or 'applies_to' field"
                    )
        
        if malformed:
            return self._create_finding(
                "Malformed constraints detected",
                details={"malformed": malformed}
            )
        
        return None


class SystemNameRule(BaseRule):
    """Validates system_name is properly formatted"""
    
    id = "SX-004"
    severity = "LOW"
    description = "System name formatting issue"
    category = "STRUCTURE"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        system_name = data.get("system_name")
        
        if not system_name:
            return None  # Handled by completeness rules
        
        if not isinstance(system_name, str):
            return self._create_finding(
                "System name must be a string",
                details={"actual_type": type(system_name).__name__}
            )
        
        if len(system_name.strip()) == 0:
            return self._create_finding(
                "System name is empty or whitespace only",
                details={"value": system_name}
            )
        
        if len(system_name) > 200:
            return self._create_finding(
                f"System name is too long ({len(system_name)} characters, max 200)",
                details={"length": len(system_name), "max": 200}
            )
        
        return None


class EmptyValuesRule(BaseRule):
    """Detects empty or null critical values"""
    
    id = "SX-005"
    severity = "LOW"
    description = "Empty or null critical values detected"
    category = "STRUCTURE"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        
        empty_values = []
        
        for decision in decisions:
            if not isinstance(decision, dict):
                continue
            
            decision_id = decision.get("id", "unknown")
            
            # Check for empty description
            description = decision.get("description")
            if description is not None and isinstance(description, str):
                if len(description.strip()) == 0:
                    empty_values.append(f"Decision '{decision_id}' has empty description")
        
        if empty_values:
            return self._create_finding(
                "Empty critical values detected",
                details={"empty_values": empty_values}
            )
        
        return None
