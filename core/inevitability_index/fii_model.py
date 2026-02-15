"""
SINGULARITY-Δ FAILURE INEVITABILITY INDEX (FII)
================================================
Quantifies the logical certainty that a system will collapse.

THIS IS NOT:
- A probability estimate
- An ML prediction
- A risk score

THIS IS:
- A logical certainty measure
- Based on graph structure and axiom violations
- Deterministic given the same reality graph

FII Scale:
0.00 - 0.30: Low inevitability (survivable)
0.30 - 0.70: Medium inevitability (fragile)
0.70 - 0.90: High inevitability (will fail)
0.90 - 1.00: Absolute inevitability (already failed)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Set
from enum import Enum


class CollapsePathType(Enum):
    """Types of paths that lead to system collapse"""
    CONTRADICTION = "contradiction"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    HUMAN_DEPENDENCY = "human_dependency"
    CASCADING_FAILURE = "cascading_failure"
    ASSUMPTION_VIOLATION = "assumption_violation"
    DEADLOCK = "deadlock"
    UNBOUNDED_GROWTH = "unbounded_growth"


@dataclass
class CollapsePath:
    """Represents a path that leads to system collapse"""
    path_type: CollapsePathType
    nodes: List[str]  # Node IDs in the path
    certainty: float  # 0.0 - 1.0
    explanation: str
    metadata: Dict[str, Any]


class FIICalculator:
    """
    Calculates Failure Inevitability Index.
    
    The FII is computed by:
    1. Identifying all collapse paths in the reality graph
    2. Computing certainty for each path
    3. Combining path certainties using logical OR
    4. Adjusting for graph structure and axiom violations
    """
    
    def __init__(self, reality_graph, axiom_violations: List):
        self.graph = reality_graph
        self.violations = axiom_violations
        self.collapse_paths: List[CollapsePath] = []
    
    def compute(self) -> float:
        """
        Compute the Failure Inevitability Index.
        Returns a value between 0.0 and 1.0.
        """
        # Step 1: Find all collapse paths
        self._identify_collapse_paths()
        
        # Step 2: Compute base FII from collapse paths
        base_fii = self._compute_base_fii()
        
        # Step 3: Adjust for axiom violations
        violation_adjustment = self._compute_violation_adjustment()
        
        # Step 4: Adjust for graph structure
        structure_adjustment = self._compute_structure_adjustment()
        
        # Step 5: Combine adjustments (using logical OR-like operation)
        fii = self._combine_factors(base_fii, violation_adjustment, structure_adjustment)
        
        return min(1.0, max(0.0, fii))
    
    def _identify_collapse_paths(self):
        """Identify all paths in the graph that lead to collapse"""
        self.collapse_paths = []
        
        # Find contradiction-based collapse paths
        contradictions = self.graph.find_contradictions()
        for c in contradictions:
            self.collapse_paths.append(CollapsePath(
                path_type=CollapsePathType.CONTRADICTION,
                nodes=c.causal_chain,
                certainty=c.severity,
                explanation=c.explanation,
                metadata={"source": c.node_a.name, "target": c.node_b.name}
            ))
        
        # Find resource exhaustion paths
        resource_paths = self._find_resource_exhaustion_paths()
        self.collapse_paths.extend(resource_paths)
        
        # Find cascading failure paths
        cascade_paths = self._find_cascading_failure_paths()
        self.collapse_paths.extend(cascade_paths)
        
        # Find single point of failure paths
        spof_paths = self._find_spof_paths()
        self.collapse_paths.extend(spof_paths)
        
        # Find deadlock paths
        deadlock_paths = self._find_deadlock_paths()
        self.collapse_paths.extend(deadlock_paths)
    
    def _find_resource_exhaustion_paths(self) -> List[CollapsePath]:
        """Find paths where resources are exhausted"""
        paths = []
        resource_nodes = self.graph.get_nodes_by_type(
            __import__('core.reality_graph.graph_builder', fromlist=['NodeType']).NodeType.RESOURCE
        )
        
        for resource in resource_nodes:
            capacity = resource.metadata.get("capacity", float('inf'))
            
            # Find all consumers of this resource
            incoming = self.graph.get_incoming_edges(resource.id)
            requires_edges = [e for e in incoming if e.type.value == "requires"]
            
            if len(requires_edges) > 0:
                total_demand = sum(
                    self.graph.get_node(e.source).metadata.get("resource_demand", 1)
                    for e in requires_edges
                )
                
                if total_demand > capacity:
                    if capacity > 0:
                        certainty = min(1.0, total_demand / capacity - 1.0)
                    else:
                        certainty = 1.0  # Resource completely unavailable
                    paths.append(CollapsePath(
                        path_type=CollapsePathType.RESOURCE_EXHAUSTION,
                        nodes=[e.source for e in requires_edges] + [resource.id],
                        certainty=certainty,
                        explanation=f"Resource '{resource.name}' exhausted: demand {total_demand} > capacity {capacity}",
                        metadata={
                            "resource": resource.name,
                            "capacity": capacity,
                            "demand": total_demand,
                            "oversubscription": total_demand / capacity if capacity > 0 else float('inf')
                        }
                    ))
        
        return paths
    
    def _find_cascading_failure_paths(self) -> List[CollapsePath]:
        """Find paths where one failure cascades to system collapse"""
        paths = []
        critical_nodes = self.graph.get_critical_nodes(threshold=0.8)
        
        for node in critical_nodes:
            # Find all nodes that depend on this critical node
            dependents = self._find_all_dependents(node.id)
            
            if len(dependents) > 3:  # Significant cascade potential
                certainty = min(0.9, len(dependents) / 10.0)
                paths.append(CollapsePath(
                    path_type=CollapsePathType.CASCADING_FAILURE,
                    nodes=[node.id] + list(dependents),
                    certainty=certainty,
                    explanation=f"Failure of '{node.name}' cascades to {len(dependents)} components",
                    metadata={
                        "trigger": node.name,
                        "cascade_size": len(dependents),
                        "criticality": node.criticality
                    }
                ))
        
        return paths
    
    def _find_spof_paths(self) -> List[CollapsePath]:
        """Find single points of failure"""
        paths = []
        nodes = self.graph.nodes.values()
        
        for node in nodes:
            # A node is a SPOF if:
            # 1. It has no redundancy
            # 2. Multiple critical components depend on it
            dependents = self._find_all_dependents(node.id)
            critical_dependents = [
                d for d in dependents
                if self.graph.get_node(d).criticality > 0.7
            ]
            
            has_redundancy = node.metadata.get("has_redundancy", False)
            
            if not has_redundancy and len(critical_dependents) > 1:
                certainty = min(0.95, 0.7 + len(critical_dependents) * 0.05)
                paths.append(CollapsePath(
                    path_type=CollapsePathType.HUMAN_DEPENDENCY if node.type.value == "resource" else CollapsePathType.CASCADING_FAILURE,
                    nodes=[node.id] + list(critical_dependents),
                    certainty=certainty,
                    explanation=f"'{node.name}' is a single point of failure for {len(critical_dependents)} critical components",
                    metadata={
                        "spof": node.name,
                        "critical_dependents": len(critical_dependents)
                    }
                ))
        
        return paths
    
    def _find_deadlock_paths(self) -> List[CollapsePath]:
        """Find potential deadlock cycles"""
        paths = []
        visited = set()
        rec_stack = set()
        current_path = []
        
        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            current_path.append(node_id)
            
            for edge in self.graph.get_outgoing_edges(node_id):
                if edge.type.value in ["requires", "depends_on"]:
                    target = edge.target
                    if target not in visited:
                        if has_cycle(target):
                            return True
                    elif target in rec_stack:
                        # Found a cycle
                        cycle_start = current_path.index(target)
                        cycle = current_path[cycle_start:]
                        paths.append(CollapsePath(
                            path_type=CollapsePathType.DEADLOCK,
                            nodes=cycle,
                            certainty=0.8,
                            explanation=f"Circular dependency detected: {' → '.join(self.graph.get_node(n).name for n in cycle)}",
                            metadata={"cycle": cycle}
                        ))
                        return True
            
            current_path.pop()
            rec_stack.remove(node_id)
            return False
        
        for node_id in self.graph.nodes:
            if node_id not in visited:
                has_cycle(node_id)
        
        return paths
    
    def _find_all_dependents(self, node_id: str) -> Set[str]:
        """Find all nodes that depend on the given node"""
        dependents = set()
        visited = set()
        stack = [node_id]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            
            for edge in self.graph.get_outgoing_edges(current):
                if edge.type.value in ["causes", "enables"]:
                    dependents.add(edge.target)
                    stack.append(edge.target)
        
        return dependents
    
    def _compute_base_fii(self) -> float:
        """Compute base FII from collapse paths"""
        if not self.collapse_paths:
            return 0.0
        
        # Use logical OR combination: P(A or B) = P(A) + P(B) - P(A)*P(B)
        combined_certainty = 0.0
        for path in self.collapse_paths:
            combined_certainty = combined_certainty + path.certainty - (combined_certainty * path.certainty)
        
        return combined_certainty
    
    def _compute_violation_adjustment(self) -> float:
        """Compute adjustment based on axiom violations"""
        if not self.violations:
            return 0.0
        
        max_severity = max(v.severity for v in self.violations)
        violation_count = len(self.violations)
        
        # More violations = higher FII
        adjustment = max_severity * (1.0 + 0.05 * (violation_count - 1))
        return min(1.0, adjustment)
    
    def _compute_structure_adjustment(self) -> float:
        """Compute adjustment based on graph structure"""
        stats = self.graph.get_stats()
        
        # Factors that increase FII:
        # - High ratio of critical nodes
        # - Low decision-to-behavior ratio (underspecified)
        # - High assumption-to-decision ratio (risky)
        
        total_nodes = stats["total_nodes"]
        if total_nodes == 0:
            return 0.0
        
        critical_ratio = stats["critical_nodes"] / total_nodes
        
        decisions = stats["decisions"]
        assumptions = stats["assumptions"]
        assumption_ratio = assumptions / max(decisions, 1)
        
        # Structure score: higher = worse
        structure_score = (critical_ratio * 0.3) + (min(1.0, assumption_ratio) * 0.2)
        
        return structure_score
    
    def _combine_factors(self, base: float, violations: float, structure: float) -> float:
        """Combine FII factors using logical OR"""
        # Use probabilistic OR: P(A or B or C)
        combined = base
        combined = combined + violations - (combined * violations)
        combined = combined + structure - (combined * structure)
        return combined
    
    def get_collapse_paths(self) -> List[CollapsePath]:
        """Return all identified collapse paths"""
        return self.collapse_paths
    
    def get_most_certain_path(self) -> CollapsePath:
        """Return the collapse path with highest certainty"""
        if not self.collapse_paths:
            return None
        return max(self.collapse_paths, key=lambda p: p.certainty)
    
    def explain(self) -> str:
        """Generate detailed explanation of FII calculation"""
        lines = [
            "FAILURE INEVITABILITY INDEX CALCULATION",
            "=" * 50,
            ""
        ]
        
        fii = self.compute()
        lines.append(f"FINAL FII: {fii:.4f} ({self._interpret_fii(fii)})")
        lines.append("")
        
        lines.append(f"Identified {len(self.collapse_paths)} collapse paths:")
        for i, path in enumerate(self.collapse_paths[:5], 1):  # Top 5
            lines.append(f"\n{i}. {path.path_type.value.upper()} (certainty: {path.certainty:.2f})")
            lines.append(f"   {path.explanation}")
        
        return "\n".join(lines)
    
    def _interpret_fii(self, fii: float) -> str:
        """Interpret FII value"""
        if fii < 0.3:
            return "LOW - System may survive"
        elif fii < 0.7:
            return "MEDIUM - System is fragile"
        elif fii < 0.9:
            return "HIGH - Failure is likely inevitable"
        else:
            return "ABSOLUTE - System is logically failed"
