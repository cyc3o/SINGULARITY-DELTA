"""
Configuration Management
Centralized configuration for the entire system
"""
from typing import Dict, Any


class Config:
    """
    Application configuration.
    Single source of truth for all settings.
    """
    
    # Engine Configuration
    ENGINE_VERSION = "1.0.0"
    ENGINE_NAME = "Singularity Delta"
    
    # Scoring Configuration
    BASE_SCORE = 100.0
    MIN_SCORE = 0.0
    MAX_SCORE = 100.0
    
    # Severity Weights
    SEVERITY_WEIGHTS = {
        "CRITICAL": 40,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5,
        "INFO": 1
    }
    
    # Output Configuration
    DEFAULT_OUTPUT_FORMAT = "cli"  # cli | json | compact
    USE_COLORS = True
    PRETTY_JSON = True
    
    # Validation Configuration
    MAX_NESTING_DEPTH = 5
    MAX_SYSTEM_NAME_LENGTH = 200
    
    # Logging Configuration
    LOG_LEVEL = "INFO"  # DEBUG | INFO | WARNING | ERROR | CRITICAL
    LOG_TO_FILE = False
    LOG_DIR = "logs"
    
    # Rule Configuration
    ENABLE_ALL_RULES = True
    STRICT_MODE = False
    
    # Export Configuration
    EXPORT_DIR = "output"
    AUTO_EXPORT = False
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "engine": {
                "version": cls.ENGINE_VERSION,
                "name": cls.ENGINE_NAME
            },
            "scoring": {
                "base_score": cls.BASE_SCORE,
                "severity_weights": cls.SEVERITY_WEIGHTS
            },
            "output": {
                "format": cls.DEFAULT_OUTPUT_FORMAT,
                "use_colors": cls.USE_COLORS,
                "pretty_json": cls.PRETTY_JSON
            },
            "validation": {
                "max_nesting_depth": cls.MAX_NESTING_DEPTH,
                "max_system_name_length": cls.MAX_SYSTEM_NAME_LENGTH
            },
            "rules": {
                "enable_all": cls.ENABLE_ALL_RULES,
                "strict_mode": cls.STRICT_MODE
            }
        }
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return getattr(cls, key.upper(), default)
