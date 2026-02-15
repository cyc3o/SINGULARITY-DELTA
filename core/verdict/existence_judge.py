"""
SINGULARITY-Δ EXISTENCE JUDGE
==============================
The final arbiter that determines whether a software system
is logically permissible to exist in production.

OUTPUT:
✅ LOGICALLY PERMISSIBLE
❌ NOT LOGICALLY PERMISSIBLE

There is no "maybe", no confidence score, no advisory tone.
Only binary existence.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class VerdictType(Enum):
    """Binary existence verdict"""
    PERMISSIBLE = "✅ LOGICALLY PERMISSIBLE"
    NOT_PERMISSIBLE = "❌ NOT LOGICALLY PERMISSIBLE"
    UNVERIFIED = "⚠️ UNVERIFIED (Insufficient Data)"


@dataclass
class ExistenceVerdict:
    """Final verdict on system existence"""
    verdict: VerdictType
    certainty: float  # How certain are we (for UNVERIFIED cases)
    primary_reason: str
    supporting_evidence: List[str]
    failure_inevitability_index: float
    axiom_violations: List[Any]
    counterfactual_failures: int
    proof_chain: List[str]
    
    def is_permissible(self) -> bool:
        return self.verdict == VerdictType.PERMISSIBLE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "certainty": self.certainty,
            "primary_reason": self.primary_reason,
            "supporting_evidence": self.supporting_evidence,
            "fii": self.failure_inevitability_index,
            "axiom_violations": len(self.axiom_violations),
            "counterfactual_failures": self.counterfactual_failures,
            "proof_chain": self.proof_chain
        }


class ExistenceJudge:
    """
    The final judge that determines system existence.
    
    Decision logic:
    1. If any FATAL axiom violation exists → NOT PERMISSIBLE
    2. If FII ≥ 0.90 → NOT PERMISSIBLE (inevitable failure)
    3. If critical counterfactuals fail → NOT PERMISSIBLE (not robust)
    4. If insufficient data for verdict → UNVERIFIED
    5. Otherwise → PERMISSIBLE
    
    The judge must EXPLAIN its verdict with a proof chain.
    """
    
    def __init__(self, 
                 reality_graph,
                 axiom_violations: List,
                 fii: float,
                 counterfactual_results: List):
        self.graph = reality_graph
        self.violations = axiom_violations
        self.fii = fii
        self.cf_results = counterfactual_results
    
    def render_verdict(self) -> ExistenceVerdict:
        """
        Render the final existence verdict.
        This is a deterministic decision based on logical analysis.
        """
        
        # Check for fatal axiom violations
        fatal_violations = [v for v in self.violations if v.is_fatal()]
        
        if fatal_violations:
            return self._verdict_fatal_axiom(fatal_violations[0])
        
        # Check FII threshold
        if self.fii >= 0.90:
            return self._verdict_inevitable_failure()
        
        # Check critical counterfactual failures
        critical_cf_failures = [
            r for r in self.cf_results
            if not r.survived and r.scenario.criticality >= 0.7
        ]
        
        if len(critical_cf_failures) >= 2:  # Multiple critical failures
            return self._verdict_counterfactual_failure(critical_cf_failures)
        
        # Check if we have sufficient data
        if not self._has_sufficient_data():
            return self._verdict_unverified()
        
        # Check for non-fatal but concerning issues
        if self.fii >= 0.70 or len(self.violations) > 3:
            # System is permissible but fragile
            return self._verdict_permissible_fragile()
        
        # System is permissible
        return self._verdict_permissible_robust()
    
    def _verdict_fatal_axiom(self, violation) -> ExistenceVerdict:
        """Verdict: Fatal axiom violation"""
        return ExistenceVerdict(
            verdict=VerdictType.NOT_PERMISSIBLE,
            certainty=1.0,
            primary_reason=f"Fatal violation of {violation.axiom_name}",
            supporting_evidence=[
                violation.explanation,
                f"Severity: {violation.severity:.2%}",
                f"Violation type: {violation.violation_type.value}"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=self._count_cf_failures(),
            proof_chain=[
                "AXIOM_VERIFICATION",
                violation.axiom_name,
                violation.violation_type.value,
                f"severity={violation.severity:.2f}",
                "FATAL_VIOLATION",
                "SYSTEM_INVALID"
            ]
        )
    
    def _verdict_inevitable_failure(self) -> ExistenceVerdict:
        """Verdict: Failure is inevitable"""
        return ExistenceVerdict(
            verdict=VerdictType.NOT_PERMISSIBLE,
            certainty=1.0,
            primary_reason=f"Failure Inevitability Index: {self.fii:.2%}",
            supporting_evidence=[
                "All execution paths lead to system collapse",
                f"FII threshold exceeded: {self.fii:.2%} ≥ 90%",
                "Per Inevitability Axiom: system is logically failed"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=self._count_cf_failures(),
            proof_chain=[
                "FII_CALCULATION",
                f"fii={self.fii:.4f}",
                "fii >= 0.90",
                "INEVITABILITY_AXIOM_TRIGGERED",
                "COLLAPSE_CERTAIN",
                "SYSTEM_INVALID"
            ]
        )
    
    def _verdict_counterfactual_failure(self, failures: List) -> ExistenceVerdict:
        """Verdict: Failed critical counterfactuals"""
        return ExistenceVerdict(
            verdict=VerdictType.NOT_PERMISSIBLE,
            certainty=0.95,
            primary_reason=f"System collapsed in {len(failures)} critical scenarios",
            supporting_evidence=[
                f"Failed scenario: {f.scenario.name}" for f in failures[:3]
            ] + [
                "Per Counterfactual Validity Axiom: system is fundamentally fragile"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=len(failures),
            proof_chain=[
                "COUNTERFACTUAL_SIMULATION",
                f"critical_failures={len(failures)}",
                failures[0].scenario.name,
                failures[0].collapse_reason,
                "COUNTERFACTUAL_VALIDITY_VIOLATED",
                "SYSTEM_INVALID"
            ]
        )
    
    def _verdict_unverified(self) -> ExistenceVerdict:
        """Verdict: Insufficient data"""
        missing = self._identify_missing_data()
        
        return ExistenceVerdict(
            verdict=VerdictType.UNVERIFIED,
            certainty=0.5,
            primary_reason="Insufficient data to render verdict",
            supporting_evidence=[
                f"Missing: {', '.join(missing)}",
                "Cannot verify system without complete model",
                "Recommendation: Provide additional system specifications"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=self._count_cf_failures(),
            proof_chain=[
                "DATA_COMPLETENESS_CHECK",
                "INCOMPLETE_MODEL",
                f"missing={missing}",
                "CANNOT_VERIFY",
                "VERDICT_UNVERIFIED"
            ]
        )
    
    def _verdict_permissible_fragile(self) -> ExistenceVerdict:
        """Verdict: Permissible but fragile"""
        return ExistenceVerdict(
            verdict=VerdictType.PERMISSIBLE,
            certainty=0.75,
            primary_reason="System is logically permissible but exhibits fragility",
            supporting_evidence=[
                f"FII: {self.fii:.2%} (elevated but below threshold)",
                f"Axiom violations: {len(self.violations)} (non-fatal)",
                "System may survive but requires careful operation"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=self._count_cf_failures(),
            proof_chain=[
                "AXIOM_VERIFICATION",
                "no_fatal_violations",
                "FII_CALCULATION",
                f"fii={self.fii:.4f}",
                "fii < 0.90",
                "COUNTERFACTUAL_VALIDATION",
                "acceptable_failure_rate",
                "VERDICT_PERMISSIBLE_FRAGILE"
            ]
        )
    
    def _verdict_permissible_robust(self) -> ExistenceVerdict:
        """Verdict: Permissible and robust"""
        return ExistenceVerdict(
            verdict=VerdictType.PERMISSIBLE,
            certainty=1.0,
            primary_reason="System is logically permissible and robust",
            supporting_evidence=[
                f"FII: {self.fii:.2%} (low)",
                f"No fatal axiom violations ({len(self.violations)} minor issues)",
                "Survived critical counterfactual scenarios",
                "System demonstrates structural soundness"
            ],
            failure_inevitability_index=self.fii,
            axiom_violations=self.violations,
            counterfactual_failures=self._count_cf_failures(),
            proof_chain=[
                "AXIOM_VERIFICATION",
                "no_fatal_violations",
                "FII_CALCULATION",
                f"fii={self.fii:.4f}",
                "fii < 0.70",
                "COUNTERFACTUAL_VALIDATION",
                "critical_scenarios_survived",
                "VERDICT_PERMISSIBLE_ROBUST"
            ]
        )
    
    def _has_sufficient_data(self) -> bool:
        """Check if we have sufficient data to render verdict"""
        stats = self.graph.get_stats()
        
        # Must have at least:
        # - Some decisions
        # - Some behaviors or consequences
        # - Some edges connecting them
        
        if stats["decisions"] == 0:
            return False
        
        if stats["total_edges"] == 0:
            return False
        
        # Check for orphaned behaviors (no decision ancestry)
        behaviors = self.graph.get_behavior_nodes()
        for behavior in behaviors:
            if not self.graph.has_decision_ancestry(behavior):
                return False  # Incomplete model
        
        return True
    
    def _identify_missing_data(self) -> List[str]:
        """Identify what data is missing"""
        missing = []
        stats = self.graph.get_stats()
        
        if stats["decisions"] == 0:
            missing.append("engineering decisions")
        
        if stats["behaviors"] == 0:
            missing.append("system behaviors")
        
        if stats["total_edges"] == 0:
            missing.append("causal relationships")
        
        if stats["assumptions"] == 0:
            missing.append("system assumptions")
        
        return missing
    
    def _count_cf_failures(self) -> int:
        """Count counterfactual failures"""
        return sum(1 for r in self.cf_results if not r.survived)


class VerdictFormatter:
    """Formats the verdict for terminal output"""
    
    @staticmethod
    def format(verdict: ExistenceVerdict) -> str:
        """Format verdict as dark, authoritative terminal output"""
        lines = []
        
        # Header
        lines.append("")
        lines.append("═" * 70)
        lines.append("SINGULARITY-Δ EXISTENCE VERIFICATION")
        lines.append("═" * 70)
        lines.append("")
        
        # Verdict
        lines.append("SYSTEM EXISTENCE VERDICT:")
        lines.append(f"  {verdict.verdict.value}")
        lines.append("")
        
        # Primary reason
        lines.append("PRIMARY REASON:")
        lines.append(f"  {verdict.primary_reason}")
        lines.append("")
        
        # Supporting evidence
        if verdict.supporting_evidence:
            lines.append("SUPPORTING EVIDENCE:")
            for evidence in verdict.supporting_evidence:
                lines.append(f"  • {evidence}")
            lines.append("")
        
        # Metrics
        lines.append("METRICS:")
        lines.append(f"  Failure Inevitability Index: {verdict.failure_inevitability_index:.2%}")
        lines.append(f"  Axiom Violations: {len(verdict.axiom_violations)}")
        lines.append(f"  Counterfactual Failures: {verdict.counterfactual_failures}")
        lines.append(f"  Verdict Certainty: {verdict.certainty:.1%}")
        lines.append("")
        
        # Proof chain
        lines.append("PROOF CHAIN:")
        for i, step in enumerate(verdict.proof_chain, 1):
            lines.append(f"  {i}. {step}")
        lines.append("")
        
        lines.append("═" * 70)
        lines.append("")
        
        return "\n".join(lines)
