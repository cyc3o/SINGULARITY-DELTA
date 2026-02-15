"""
SINGULARITY-Δ AXIOM BASE
========================
Foundational laws that govern system existence verification.
These are NOT configurable - they are mathematical truths.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class AxiomViolationType(Enum):
    """Types of axiom violations"""
    CONTRADICTION = "contradiction"
    CAUSALITY_BREAK = "causality_break"
    INEVITABILITY = "inevitability"
    HUMAN_DEPENDENCY = "human_dependency"
    SILENT_ASSUMPTION = "silent_assumption"
    UNEXPLAINED_BEHAVIOR = "unexplained_behavior"
    COUNTERFACTUAL_FAILURE = "counterfactual_failure"


@dataclass
class AxiomViolation:
    """Represents a violation of a foundational axiom"""
    axiom_name: str
    violation_type: AxiomViolationType
    severity: float  # 0.0 - 1.0, where 1.0 = system cannot exist
    evidence: Dict[str, Any]
    causal_chain: list[str]
    explanation: str
    
    def is_fatal(self) -> bool:
        """Fatal violations prevent system existence"""
        return self.severity >= 0.95


class AxiomBase:
    """Base class for all axioms in SINGULARITY-Δ"""
    
    def __init__(self):
        self.name: str = "BASE_AXIOM"
        self.description: str = ""
        self.is_fundamental: bool = True  # Cannot be disabled
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """
        Verify this axiom holds for the given reality graph.
        Returns None if axiom holds, AxiomViolation if violated.
        """
        raise NotImplementedError("Axiom must implement verify()")
    
    def explain(self) -> str:
        """Explain this axiom in formal terms"""
        raise NotImplementedError("Axiom must implement explain()")


class ExistenceAxiom(AxiomBase):
    """
    AXIOM 1: SOFTWARE = FROZEN DECISIONS
    
    A software system is a set of engineering decisions frozen in time.
    All system behavior derives from these decisions.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "EXISTENCE_AXIOM"
        self.description = "Software exists as frozen engineering decisions"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Verify all behaviors trace to explicit decisions"""
        orphaned_behaviors = []
        
        for node in reality_graph.get_behavior_nodes():
            if not reality_graph.has_decision_ancestry(node):
                orphaned_behaviors.append(node.id)
        
        if orphaned_behaviors:
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.UNEXPLAINED_BEHAVIOR,
                severity=0.8,
                evidence={"orphaned_behaviors": orphaned_behaviors},
                causal_chain=["undefined_origin", "behavior_without_decision"],
                explanation=f"Found {len(orphaned_behaviors)} behaviors with no decision origin"
            )
        
        return None
    
    def explain(self) -> str:
        return """
        EXISTENCE AXIOM:
        ∀ behavior B, ∃ decision D such that B derives from D
        
        If any observable system behavior cannot be traced to an explicit
        engineering decision, the system model is incomplete and cannot
        be verified.
        """


class ContradictionLaw(AxiomBase):
    """
    AXIOM 4: MUTUAL UNSATISFIABILITY = INVALID SYSTEM
    
    Two decisions that cannot both be satisfied invalidate the entire system.
    There is no "partial validity" - contradictions are fatal.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "CONTRADICTION_LAW"
        self.description = "Mutually unsatisfiable decisions invalidate system"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Detect logical contradictions in decision graph"""
        contradictions = reality_graph.find_contradictions()
        
        if contradictions:
            # Find the most severe contradiction
            max_severity = max(c.severity for c in contradictions)
            primary_contradiction = next(c for c in contradictions if c.severity == max_severity)
            
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.CONTRADICTION,
                severity=max_severity,
                evidence={
                    "contradictions": [c.to_dict() for c in contradictions],
                    "primary": primary_contradiction.to_dict()
                },
                causal_chain=primary_contradiction.causal_chain,
                explanation=primary_contradiction.explanation
            )
        
        return None
    
    def explain(self) -> str:
        return """
        CONTRADICTION LAW:
        ∀ decisions D1, D2: if ¬(D1 ∧ D2), then System is INVALID
        
        If any two decisions in the system cannot both be true simultaneously,
        the system cannot logically exist. Time does not resolve contradictions.
        """


class InevitabilityAxiom(AxiomBase):
    """
    AXIOM 5: ALL PATHS TO FAILURE = ALREADY FAILED
    
    If every possible execution path leads to system failure,
    the system is considered already failed regardless of time.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "INEVITABILITY_AXIOM"
        self.description = "Inevitable failure = present failure"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Check if failure is inevitable"""
        fii = context.get("failure_inevitability_index", 0.0)
        
        if fii >= 0.95:  # 95%+ certainty of collapse
            failure_paths = context.get("failure_paths", [])
            
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.INEVITABILITY,
                severity=fii,
                evidence={
                    "fii": fii,
                    "failure_paths": failure_paths,
                    "escape_paths": 0
                },
                causal_chain=["all_paths_analyzed", "no_escape_route", "collapse_certain"],
                explanation=f"Failure Inevitability Index: {fii:.2%}. No viable execution path exists."
            )
        
        return None
    
    def explain(self) -> str:
        return """
        INEVITABILITY AXIOM:
        if P(failure) = 1.0 across all execution paths,
        then System is FAILED at t=0
        
        Time is not a factor in logical existence. If collapse is certain,
        the system has already collapsed from a logical perspective.
        """


class CounterfactualValidityAxiom(AxiomBase):
    """
    AXIOM 6: MUST SURVIVE ALTERNATE REALITIES
    
    A valid system must remain coherent under reasonable counterfactual scenarios.
    Fragility to minor changes indicates structural invalidity.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "COUNTERFACTUAL_VALIDITY"
        self.description = "System must survive alternate realities"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Test system against counterfactual scenarios"""
        counterfactual_results = context.get("counterfactual_results", [])
        
        failed_scenarios = [r for r in counterfactual_results if not r["survived"]]
        critical_failures = [r for r in failed_scenarios if r["scenario_criticality"] >= 0.7]
        
        if critical_failures:
            failure_rate = len(failed_scenarios) / len(counterfactual_results) if counterfactual_results else 0
            
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.COUNTERFACTUAL_FAILURE,
                severity=min(0.9, failure_rate),
                evidence={
                    "failed_scenarios": len(failed_scenarios),
                    "critical_failures": len(critical_failures),
                    "total_tested": len(counterfactual_results),
                    "details": critical_failures[:3]  # Top 3
                },
                causal_chain=["counterfactual_test", "critical_scenario_failure"],
                explanation=f"System collapsed in {len(critical_failures)} critical alternate scenarios"
            )
        
        return None
    
    def explain(self) -> str:
        return """
        COUNTERFACTUAL VALIDITY:
        System S is valid ⟹ S remains coherent in alternate reality R
        where R represents reasonable perturbations to assumptions
        
        A system that collapses when assumptions are slightly violated
        is fundamentally invalid, not just fragile.
        """


class HumanDependencyParadox(AxiomBase):
    """
    AXIOM 7: HUMAN DEPENDENCY = INVALID DESIGN
    
    A system that depends on a specific human for stability
    has a single point of failure and cannot be considered valid.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "HUMAN_DEPENDENCY_PARADOX"
        self.description = "Specific human dependency invalidates design"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Detect critical human dependencies"""
        human_dependencies = context.get("human_dependencies", [])
        
        critical_dependencies = [
            h for h in human_dependencies 
            if h.get("is_single_point_of_failure", False)
        ]
        
        if critical_dependencies:
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.HUMAN_DEPENDENCY,
                severity=0.85,
                evidence={
                    "critical_humans": [h["identifier"] for h in critical_dependencies],
                    "failure_scenarios": [h["failure_scenario"] for h in critical_dependencies]
                },
                causal_chain=["human_identified", "no_redundancy", "single_point_of_failure"],
                explanation=f"System stability depends on {len(critical_dependencies)} irreplaceable human(s)"
            )
        
        return None
    
    def explain(self) -> str:
        return """
        HUMAN DEPENDENCY PARADOX:
        if ∃ human H such that (H unavailable ⟹ System fails),
        then System is INVALID
        
        Humans are inherently unreliable (leave, sleep, err, die).
        A system that requires a specific human is logically unstable.
        """


class SilentAssumptionLaw(AxiomBase):
    """
    AXIOM 8: UNSTATED ASSUMPTIONS ARE HOSTILE
    
    Any assumption not explicitly stated and verified is treated as hostile
    and must be stress-tested until it breaks.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "SILENT_ASSUMPTION_LAW"
        self.description = "Unstated assumptions are hostile entities"
    
    def verify(self, reality_graph, context: Dict[str, Any]) -> Optional[AxiomViolation]:
        """Identify and stress-test silent assumptions"""
        assumptions = context.get("extracted_assumptions", [])
        hostile_assumptions = context.get("hostile_assumptions", [])
        
        violated_assumptions = [
            a for a in hostile_assumptions
            if a.get("stress_test_failed", False)
        ]
        
        if violated_assumptions:
            return AxiomViolation(
                axiom_name=self.name,
                violation_type=AxiomViolationType.SILENT_ASSUMPTION,
                severity=0.75,
                evidence={
                    "total_assumptions": len(assumptions),
                    "violated": len(violated_assumptions),
                    "details": violated_assumptions[:5]
                },
                causal_chain=["assumption_extracted", "stress_test", "assumption_violated"],
                explanation=f"{len(violated_assumptions)} critical assumptions failed stress testing"
            )
        
        return None
    
    def explain(self) -> str:
        return """
        SILENT ASSUMPTION LAW:
        ∀ assumption A: if A is unstated, treat A as hostile
        
        Assumptions are where systems fail. Every implicit assumption
        must be made explicit and stress-tested until it breaks.
        If it breaks, the system is invalid.
        """


class AxiomRegistry:
    """Registry of all axioms that govern SINGULARITY-Δ"""
    
    def __init__(self):
        self.axioms: list[AxiomBase] = [
            ExistenceAxiom(),
            ContradictionLaw(),
            InevitabilityAxiom(),
            CounterfactualValidityAxiom(),
            HumanDependencyParadox(),
            SilentAssumptionLaw(),
        ]
    
    def verify_all(self, reality_graph, context: Dict[str, Any]) -> list[AxiomViolation]:
        """
        Verify all axioms and return violations.
        Fatal violations prevent system existence.
        """
        violations = []
        
        for axiom in self.axioms:
            violation = axiom.verify(reality_graph, context)
            if violation:
                violations.append(violation)
        
        return violations
    
    def get_fatal_violations(self, violations: list[AxiomViolation]) -> list[AxiomViolation]:
        """Return only fatal violations"""
        return [v for v in violations if v.is_fatal()]
    
    def explain_all(self) -> str:
        """Generate formal explanation of all axioms"""
        explanations = [axiom.explain() for axiom in self.axioms]
        return "\n\n".join(explanations)
