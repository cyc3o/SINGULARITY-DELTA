"""
Execution Context
Provides runtime information to rules during evaluation
"""
from typing import Dict, Any, Optional


class ExecutionContext:
    """
    Carries runtime state and configuration during rule execution.
    Allows rules to access shared resources without tight coupling.
    """
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.cache: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.strict_mode: bool = False
        self.debug: bool = False
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in context"""
        self.cache[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from context"""
        return self.cache.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if key exists in context"""
        return key in self.cache
    
    def enable_strict_mode(self) -> None:
        """Enable strict validation mode"""
        self.strict_mode = True
    
    def enable_debug(self) -> None:
        """Enable debug output"""
        self.debug = True
    
    def __repr__(self) -> str:
        return f"<ExecutionContext strict={self.strict_mode} debug={self.debug}>"
