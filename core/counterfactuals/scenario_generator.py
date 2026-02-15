"""
SINGULARITY-Δ COUNTERFACTUAL SIMULATOR
=======================================
Tests whether a system survives under alternate reality scenarios.

A valid system must not collapse when reasonable assumptions are violated
or when conditions change slightly.

This is NOT scenario planning or what-if analysis.
This is LOGICAL ROBUSTNESS VERIFICATION.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Callable
from enum import Enum
import copy


class ScenarioType(Enum):
    """Types of counterfactual scenarios"""
    TRAFFIC_SPIKE = "traffic_spike"
    NODE_FAILURE = "node_failure"
    HUMAN_UNAVAILABLE = "human_unavailable"
    ASSUMPTION_VIOLATED = "assumption_violated"
    RESOURCE_DEGRADED = "resource_degraded"
    NETWORK_PARTITION = "network_partition"
    DATA_CORRUPTION = "data_corruption"
    DEPLOYMENT_FAILURE = "deployment_failure"


@dataclass
class CounterfactualScenario:
    """Represents an alternate reality scenario"""
    name: str
    scenario_type: ScenarioType
    description: str
    criticality: float  # 0.0 - 1.0, how critical is this scenario
    modifications: List[Callable]  # Functions that modify the reality graph
    metadata: Dict[str, Any]


@dataclass
class CounterfactualResult:
    """Result of testing a counterfactual scenario"""
    scenario: CounterfactualScenario
    survived: bool
    collapse_reason: str
    fii_after: float
    new_violations: List[Any]
    explanation: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_name": self.scenario.name,
            "scenario_type": self.scenario.scenario_type.value,
            "scenario_criticality": self.scenario.criticality,
            "survived": self.survived,
            "collapse_reason": self.collapse_reason if not self.survived else None,
            "fii_after": self.fii_after,
            "new_violations": len(self.new_violations),
            "explanation": self.explanation
        }


class CounterfactualSimulator:
    """
    Simulates alternate realities to test system robustness.
    
    The simulator:
    1. Generates realistic counterfactual scenarios
    2. Applies modifications to a copy of the reality graph
    3. Re-runs axiom verification and FII calculation
    4. Determines if the system survives
    """
    
    def __init__(self, reality_graph, axiom_registry):
        self.base_graph = reality_graph
        self.axiom_registry = axiom_registry
        self.scenarios: List[CounterfactualScenario] = []
    
    def generate_standard_scenarios(self):
        """Generate standard counterfactual scenarios"""
        self.scenarios = []
        
        # Scenario: 1.5x traffic spike
        self.scenarios.append(CounterfactualScenario(
            name="Traffic Spike 1.5x",
            scenario_type=ScenarioType.TRAFFIC_SPIKE,
            description="System receives 1.5x expected traffic",
            criticality=0.7,
            modifications=[self._modify_traffic_spike(1.5)],
            metadata={"multiplier": 1.5}
        ))
        
        # Scenario: 3x traffic spike
        self.scenarios.append(CounterfactualScenario(
            name="Traffic Spike 3x",
            scenario_type=ScenarioType.TRAFFIC_SPIKE,
            description="System receives 3x expected traffic",
            criticality=0.8,
            modifications=[self._modify_traffic_spike(3.0)],
            metadata={"multiplier": 3.0}
        ))
        
        # Scenario: Critical node failure
        critical_nodes = self.base_graph.get_critical_nodes(threshold=0.8)
        for node in critical_nodes[:3]:  # Test top 3 critical nodes
            self.scenarios.append(CounterfactualScenario(
                name=f"Node Failure: {node.name}",
                scenario_type=ScenarioType.NODE_FAILURE,
                description=f"Critical node '{node.name}' fails",
                criticality=0.9,
                modifications=[self._modify_node_failure(node.id)],
                metadata={"failed_node": node.name}
            ))
        
        # Scenario: Human dependency removed
        from core.reality_graph.graph_builder import NodeType
        resource_nodes = self.base_graph.get_nodes_by_type(NodeType.RESOURCE)
        human_resources = [r for r in resource_nodes if "human" in r.name.lower() or "engineer" in r.name.lower()]
        
        for human in human_resources[:2]:  # Test key human dependencies
            self.scenarios.append(CounterfactualScenario(
                name=f"Human Unavailable: {human.name}",
                scenario_type=ScenarioType.HUMAN_UNAVAILABLE,
                description=f"Key person '{human.name}' becomes unavailable",
                criticality=0.85,
                modifications=[self._modify_remove_resource(human.id)],
                metadata={"missing_human": human.name}
            ))
        
        # Scenario: Key assumption violated
        from core.reality_graph.graph_builder import NodeType
        assumptions = self.base_graph.get_nodes_by_type(NodeType.ASSUMPTION)
        for assumption in assumptions[:3]:  # Test top assumptions
            self.scenarios.append(CounterfactualScenario(
                name=f"Assumption Violated: {assumption.name}",
                scenario_type=ScenarioType.ASSUMPTION_VIOLATED,
                description=f"Assumption '{assumption.name}' proves false",
                criticality=0.75,
                modifications=[self._modify_violate_assumption(assumption.id)],
                metadata={"violated_assumption": assumption.name}
            ))
    
    def run_simulation(self) -> List[CounterfactualResult]:
        """
        Run all counterfactual scenarios.
        Returns list of results.
        """
        results = []
        
        for scenario in self.scenarios:
            result = self._test_scenario(scenario)
            results.append(result)
        
        return results
    
    def _test_scenario(self, scenario: CounterfactualScenario) -> CounterfactualResult:
        """Test a single counterfactual scenario"""
        # Create a deep copy of the graph
        test_graph = self._clone_graph(self.base_graph)
        
        # Apply modifications
        for modification in scenario.modifications:
            modification(test_graph)
        
        # Re-run axiom verification
        from core.inevitability_index.fii_model import FIICalculator
        
        context = {
            "counterfactual_mode": True,
            "scenario": scenario.name
        }
        
        violations = self.axiom_registry.verify_all(test_graph, context)
        
        # Calculate FII in this alternate reality
        fii_calc = FIICalculator(test_graph, violations)
        fii_after = fii_calc.compute()
        
        # Determine if system survived
        fatal_violations = self.axiom_registry.get_fatal_violations(violations)
        survived = len(fatal_violations) == 0 and fii_after < 0.9
        
        # Generate explanation
        if not survived:
            if fatal_violations:
                collapse_reason = f"Fatal axiom violation: {fatal_violations[0].explanation}"
            else:
                collapse_reason = f"FII reached {fii_after:.2%} - inevitable failure"
            
            explanation = f"System collapsed under '{scenario.name}': {collapse_reason}"
        else:
            explanation = f"System survived '{scenario.name}' (FII: {fii_after:.2%})"
        
        return CounterfactualResult(
            scenario=scenario,
            survived=survived,
            collapse_reason=collapse_reason if not survived else "",
            fii_after=fii_after,
            new_violations=violations,
            explanation=explanation
        )
    
    def _clone_graph(self, graph):
        """Create a deep copy of the reality graph"""
        # Create new graph
        new_graph = type(graph)()
        
        # Deep copy nodes
        for node_id, node in graph.nodes.items():
            new_node = copy.deepcopy(node)
            new_graph.nodes[new_node.id] = new_node
            new_graph._adjacency[new_node.id] = set()
            new_graph._reverse_adjacency[new_node.id] = set()
        
        # Deep copy edges and rebuild adjacency
        for edge_id, edge in graph.edges.items():
            new_edge = copy.deepcopy(edge)
            new_graph.edges[new_edge.id] = new_edge
            new_graph._adjacency[new_edge.source].add(new_edge.id)
            new_graph._reverse_adjacency[new_edge.target].add(new_edge.id)
        
        return new_graph
    
    # Modification functions
    
    def _modify_traffic_spike(self, multiplier: float) -> Callable:
        """Generate a traffic spike modification"""
        def modify(graph):
            # Find load-bearing resources
            from core.reality_graph.graph_builder import NodeType
            resources = graph.get_nodes_by_type(NodeType.RESOURCE)
            
            for resource in resources:
                if "cpu" in resource.name.lower() or "memory" in resource.name.lower():
                    # Increase demand on this resource
                    incoming = graph.get_incoming_edges(resource.id)
                    for edge in incoming:
                        source_node = graph.get_node(edge.source)
                        if "resource_demand" in source_node.metadata:
                            source_node.metadata["resource_demand"] *= multiplier
        
        return modify
    
    def _modify_node_failure(self, node_id: str) -> Callable:
        """Generate a node failure modification"""
        def modify(graph):
            # Remove the node and all its connected edges
            if node_id in graph.nodes:
                # Find all edges connected to this node
                edges_to_remove = []
                for edge_id, edge in list(graph.edges.items()):
                    if edge.source == node_id or edge.target == node_id:
                        edges_to_remove.append(edge_id)
                
                # Remove edges and clean up adjacency
                for edge_id in edges_to_remove:
                    edge = graph.edges[edge_id]
                    # Clean up adjacency maps
                    if edge.source in graph._adjacency:
                        graph._adjacency[edge.source].discard(edge_id)
                    if edge.target in graph._reverse_adjacency:
                        graph._reverse_adjacency[edge.target].discard(edge_id)
                    # Remove edge
                    del graph.edges[edge_id]
                
                # Remove node and its adjacency entries
                del graph.nodes[node_id]
                if node_id in graph._adjacency:
                    del graph._adjacency[node_id]
                if node_id in graph._reverse_adjacency:
                    del graph._reverse_adjacency[node_id]
        
        return modify
    
    def _modify_remove_resource(self, resource_id: str) -> Callable:
        """Generate a resource removal modification"""
        def modify(graph):
            # Similar to node failure
            if resource_id in graph.nodes:
                # Mark resource as unavailable instead of removing
                # (so we can trace dependencies)
                resource = graph.get_node(resource_id)
                resource.metadata["available"] = False
                resource.metadata["capacity"] = 0
        
        return modify
    
    def _modify_violate_assumption(self, assumption_id: str) -> Callable:
        """Generate an assumption violation modification"""
        def modify(graph):
            if assumption_id in graph.nodes:
                assumption = graph.get_node(assumption_id)
                
                # Find all nodes that depend on this assumption
                from core.reality_graph.graph_builder import EdgeType
                outgoing = graph.get_outgoing_edges(assumption_id)
                
                for edge in outgoing:
                    if edge.type == EdgeType.ASSUMES:
                        # This node assumed something that's now false
                        # Add a contradiction edge
                        from core.reality_graph.graph_builder import Edge, EdgeType
                        
                        contra_edge = Edge(
                            source=edge.target,
                            target=assumption_id,
                            type=EdgeType.CONTRADICTS,
                            metadata={
                                "reason": f"Assumption '{assumption.name}' violated",
                                "severity": 0.85
                            }
                        )
                        graph.add_edge(contra_edge)
        
        return modify
    
    def get_failure_rate(self, results: List[CounterfactualResult]) -> float:
        """Calculate the failure rate across all scenarios"""
        if not results:
            return 0.0
        
        failed = sum(1 for r in results if not r.survived)
        return failed / len(results)
    
    def get_critical_failures(self, results: List[CounterfactualResult]) -> List[CounterfactualResult]:
        """Get scenarios that were critical and failed"""
        return [r for r in results if not r.survived and r.scenario.criticality >= 0.7]
    
    def explain(self, results: List[CounterfactualResult]) -> str:
        """Generate explanation of counterfactual testing"""
        lines = [
            "COUNTERFACTUAL SIMULATION RESULTS",
            "=" * 50,
            ""
        ]
        
        total = len(results)
        survived = sum(1 for r in results if r.survived)
        failed = total - survived
        
        lines.append(f"Total scenarios tested: {total}")
        lines.append(f"Survived: {survived}")
        lines.append(f"Failed: {failed}")
        lines.append(f"Failure rate: {self.get_failure_rate(results):.1%}")
        lines.append("")
        
        critical_failures = self.get_critical_failures(results)
        if critical_failures:
            lines.append(f"CRITICAL FAILURES ({len(critical_failures)}):")
            for result in critical_failures[:5]:
                lines.append(f"\n- {result.scenario.name}")
                lines.append(f"  {result.collapse_reason}")
                lines.append(f"  FII after: {result.fii_after:.2%}")
        else:
            lines.append("No critical scenario failures detected.")
        
        return "\n".join(lines)
