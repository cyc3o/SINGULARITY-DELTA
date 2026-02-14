"""
Consistency Rules
Validates internal logical consistency of the system
"""
from typing import Dict, Any, Optional, Set
from .base_rule import BaseRule


class DecisionConsistencyRule(BaseRule):
    """Validates that decision IDs are unique"""
    
    id = "CX-001"
    severity = "CRITICAL"
    description = "Duplicate decision IDs detected"
    category = "CONSISTENCY"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        
        if not isinstance(decisions, list):
            return None  # Type checking is handled by completeness rules
        
        ids_seen = set()
        duplicates = []
        
        for i, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                continue
                
            decision_id = decision.get("id")
            if decision_id:
                if decision_id in ids_seen:
                    duplicates.append(decision_id)
                ids_seen.add(decision_id)
        
        if duplicates:
            return self._create_finding(
                f"Duplicate decision IDs found: {', '.join(duplicates)}",
                details={
                    "duplicate_ids": list(set(duplicates)),
                    "total_decisions": len(decisions)
                }
            )
        
        return None


class ConstraintReferenceRule(BaseRule):
    """Validates that constraint references point to valid decisions"""
    
    id = "CX-002"
    severity = "HIGH"
    description = "Constraint references invalid decision IDs"
    category = "CONSISTENCY"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        constraints = data.get("constraints", {})
        
        # Build set of valid decision IDs
        valid_ids = set()
        for decision in decisions:
            if isinstance(decision, dict) and "id" in decision:
                valid_ids.add(decision["id"])
        
        # Check constraint references
        invalid_refs = []
        for constraint_name, constraint_value in constraints.items():
            if isinstance(constraint_value, dict):
                applies_to = constraint_value.get("applies_to", [])
                if isinstance(applies_to, list):
                    for ref in applies_to:
                        if ref not in valid_ids:
                            invalid_refs.append(f"{constraint_name} → {ref}")
        
        if invalid_refs:
            return self._create_finding(
                f"Invalid constraint references: {', '.join(invalid_refs)}",
                details={
                    "invalid_references": invalid_refs,
                    "valid_ids": list(valid_ids)
                }
            )
        
        return None


class TypeConsistencyRule(BaseRule):
    """Validates consistent types across the system"""
    
    id = "CX-003"
    severity = "MEDIUM"
    description = "Type inconsistencies detected"
    category = "CONSISTENCY"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        
        type_errors = []
        
        for i, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                type_errors.append(f"Decision at index {i} is not a dict")
                continue
            
            # Check that priority is a number if present
            if "priority" in decision:
                if not isinstance(decision["priority"], (int, float)):
                    type_errors.append(
                        f"Decision '{decision.get('id', i)}' has non-numeric priority"
                    )
        
        if type_errors:
            return self._create_finding(
                "Type consistency violations found",
                details={"errors": type_errors}
            )
        
        return None


class ValueRangeConsistencyRule(BaseRule):
    """Validates that values are within expected ranges"""
    
    id = "CX-004"
    severity = "LOW"
    description = "Values outside expected ranges"
    category = "CONSISTENCY"
    
    def evaluate(self, data: Dict[str, Any], context) -> Optional[Dict]:
        decisions = data.get("decisions", [])
        
        range_violations = []
        
        for decision in decisions:
            if not isinstance(decision, dict):
                continue
            
            # Check priority range (should be 0-100)
            priority = decision.get("priority")
            if priority is not None and isinstance(priority, (int, float)):
                if priority < 0 or priority > 100:
                    range_violations.append(
                        f"Decision '{decision.get('id', 'unknown')}' priority {priority} outside range [0-100]"
                    )
            
            # Check confidence range (should be 0-1)
            confidence = decision.get("confidence")
            if confidence is not None and isinstance(confidence, (int, float)):
                if confidence < 0 or confidence > 1:
                    range_violations.append(
                        f"Decision '{decision.get('id', 'unknown')}' confidence {confidence} outside range [0-1]"
                    )
        
        if range_violations:
            return self._create_finding(
                "Value range violations detected",
                details={"violations": range_violations}
            )
        
        return None
