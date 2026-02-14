"""
Singularity Delta
Deterministic Policy Verification Engine

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Singularity Delta Contributors"
__license__ = "MIT"

from core.engine import Engine
from core.result import AnalysisResult
from rules import DEFAULT_RULES

__all__ = ['Engine', 'AnalysisResult', 'DEFAULT_RULES']
