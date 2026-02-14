"""
Validation Service
Pre-validation and schema checking utilities
"""
from typing import Dict, Any, List, Tuple


class Validator:
    """
    Provides pre-validation checks before engine execution.
    Quick sanity checks that don't require full rule evaluation.
    """
    
    @staticmethod
    def is_valid_json_structure(data: Any) -> bool:
        """
        Check if data is a valid JSON-like structure.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        return isinstance(data, (dict, list, str, int, float, bool, type(None)))
    
    @staticmethod
    def has_required_top_level_keys(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Quick check for absolute minimum required keys.
        
        Args:
            data: System data
            
        Returns:
            (is_valid, missing_keys)
        """
        if not isinstance(data, dict):
            return False, ["Data must be a dictionary"]
        
        critical_keys = ["system_name"]
        missing = [k for k in critical_keys if k not in data]
        
        return len(missing) == 0, missing
    
    @staticmethod
    def estimate_complexity(data: Dict[str, Any]) -> Dict[str, int]:
        """
        Calculate complexity metrics for the system.
        
        Args:
            data: System data
            
        Returns:
            Dictionary with complexity metrics
        """
        metrics = {
            "total_keys": len(data.keys()) if isinstance(data, dict) else 0,
            "decision_count": 0,
            "constraint_count": 0,
            "max_depth": Validator._calculate_depth(data)
        }
        
        if isinstance(data, dict):
            decisions = data.get("decisions", [])
            if isinstance(decisions, list):
                metrics["decision_count"] = len(decisions)
            
            constraints = data.get("constraints", {})
            if isinstance(constraints, dict):
                metrics["constraint_count"] = len(constraints)
        
        return metrics
    
    @staticmethod
    def _calculate_depth(obj, current=0):
        """Recursively calculate nesting depth"""
        if not isinstance(obj, (dict, list)):
            return current
        
        if isinstance(obj, dict):
            if not obj:
                return current
            return max(Validator._calculate_depth(v, current + 1) for v in obj.values())
        else:
            if not obj:
                return current
            return max(Validator._calculate_depth(item, current + 1) for item in obj)
    
    @staticmethod
    def quick_validate(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Perform quick validation before running full engine.
        
        Args:
            data: System data to validate
            
        Returns:
            (is_valid, message)
        """
        # Check if dictionary
        if not isinstance(data, dict):
            return False, "Data must be a dictionary"
        
        # Check if empty
        if len(data) == 0:
            return False, "Data cannot be empty"
        
        # Check top-level keys
        is_valid, missing = Validator.has_required_top_level_keys(data)
        if not is_valid:
            return False, f"Missing critical keys: {', '.join(missing)}"
        
        return True, "Quick validation passed"
