"""
Rule Registry
All validation rules available in the system
"""
from .base_rule import BaseRule
from .completeness import (
    CompletenessRule,
    DecisionCompletenessRule,
    ConstraintCompletenessRule,
    MetadataCompletenessRule
)
from .consistency import (
    DecisionConsistencyRule,
    ConstraintReferenceRule,
    TypeConsistencyRule,
    ValueRangeConsistencyRule
)
from .structure import (
    DecisionStructureRule,
    NestedDepthRule,
    ConstraintStructureRule,
    SystemNameRule,
    EmptyValuesRule
)

# Default rule set - enterprise standard
DEFAULT_RULES = [
    # Completeness
    CompletenessRule(),
    DecisionCompletenessRule(),
    ConstraintCompletenessRule(),
    MetadataCompletenessRule(),
    
    # Consistency
    DecisionConsistencyRule(),
    ConstraintReferenceRule(),
    TypeConsistencyRule(),
    ValueRangeConsistencyRule(),
    
    # Structure
    DecisionStructureRule(),
    NestedDepthRule(),
    ConstraintStructureRule(),
    SystemNameRule(),
    EmptyValuesRule()
]

__all__ = [
    'BaseRule',
    'DEFAULT_RULES',
    # Completeness
    'CompletenessRule',
    'DecisionCompletenessRule',
    'ConstraintCompletenessRule',
    'MetadataCompletenessRule',
    # Consistency
    'DecisionConsistencyRule',
    'ConstraintReferenceRule',
    'TypeConsistencyRule',
    'ValueRangeConsistencyRule',
    # Structure
    'DecisionStructureRule',
    'NestedDepthRule',
    'ConstraintStructureRule',
    'SystemNameRule',
    'EmptyValuesRule'
]
