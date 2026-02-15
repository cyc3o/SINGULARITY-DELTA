"""
SINGULARITY-Δ REALITY GRAPH
============================
The foundational data structure that models a software system
as a directed graph of decisions and their consequences.

This is NOT a dependency graph or call graph.
This is a CAUSAL REALITY MODEL.
"""

from enum import Enum
from typing import Optional, List, Set, Dict, Any
from dataclasses import dataclass, field
import uuid


class NodeType(Enum):
    """Types of nodes in the reality graph"""
    DECISION = "decision"              # Explicit engineering decision
    CONSEQUENCE = "consequence"        # Direct result of decisions
    CONSTRAINT = "constraint"          # Limit or boundary condition
    ASSUMPTION = "assumption"          # Implicit or explicit assumption
    RESOURCE = "resource"              # System resource (CPU, memory, human, etc)
    BEHAVIOR = "behavior"              # Observable system behavior
    FAILURE_MODE = "failure_mode"      # Identified failure scenario
    POLICY = "policy"                  # Operational or organizational policy


class EdgeType(Enum):
    """Types of edges in the reality graph"""
    CAUSES = "causes"                  # A causes B
    REQUIRES = "requires"              # A requires B to function
    CONTRADICTS = "contradicts"        # A contradicts B (mutual exclusion)
    DEPENDS_ON = "depends_on"          # A depends on B
    ENABLES = "enables"                # A enables B to exist
    WEAKENS = "weakens"                # A weakens B's guarantees
    ASSUMES = "assumes"                # A assumes B is true


@dataclass
class Node:
    """A node in the reality graph"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: NodeType = NodeType.DECISION
    name: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    criticality: float = 0.5  # 0.0 - 1.0
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id


@dataclass
class Edge:
    """An edge in the reality graph"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""  # Source node ID
    target: str = ""  # Target node ID
    type: EdgeType = EdgeType.CAUSES
    weight: float = 1.0  # Strength of relationship
    confidence: float = 1.0  # How certain are we of this relationship
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Edge) and self.id == other.id


@dataclass
class Contradiction:
    """Represents a detected contradiction between nodes"""
    node_a: Node
    node_b: Node
    explanation: str
    severity: float  # 0.0 - 1.0
    causal_chain: List[str]  # Path that leads to contradiction
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_a": self.node_a.name,
            "node_b": self.node_b.name,
            "explanation": self.explanation,
            "severity": self.severity,
            "causal_chain": self.causal_chain
        }


class RealityGraph:
    """
    The core reality graph that models a software system.
    
    This is a directed graph where:
    - Nodes = decisions, constraints, assumptions, behaviors
    - Edges = causal relationships between nodes
    
    The graph must satisfy causality closure: every behavior must
    trace back to at least one decision.
    """
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self._adjacency: Dict[str, Set[str]] = {}  # node_id -> set of edge_ids
        self._reverse_adjacency: Dict[str, Set[str]] = {}  # reverse edges
    
    def add_node(self, node: Node) -> Node:
        """Add a node to the graph"""
        self.nodes[node.id] = node
        if node.id not in self._adjacency:
            self._adjacency[node.id] = set()
        if node.id not in self._reverse_adjacency:
            self._reverse_adjacency[node.id] = set()
        return node
    
    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge to the graph"""
        # Validate source and target exist
        if edge.source not in self.nodes:
            raise ValueError(f"Source node {edge.source} not found")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node {edge.target} not found")
        
        self.edges[edge.id] = edge
        self._adjacency[edge.source].add(edge.id)
        self._reverse_adjacency[edge.target].add(edge.id)
        return edge
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get node by ID"""
        return self.nodes.get(node_id)
    
    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Get edge by ID"""
        return self.edges.get(edge_id)
    
    def get_outgoing_edges(self, node_id: str) -> List[Edge]:
        """Get all edges originating from a node"""
        edge_ids = self._adjacency.get(node_id, set())
        return [self.edges[eid] for eid in edge_ids]
    
    def get_incoming_edges(self, node_id: str) -> List[Edge]:
        """Get all edges pointing to a node"""
        edge_ids = self._reverse_adjacency.get(node_id, set())
        return [self.edges[eid] for eid in edge_ids]
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        """Get all nodes of a specific type"""
        return [n for n in self.nodes.values() if n.type == node_type]
    
    def get_behavior_nodes(self) -> List[Node]:
        """Get all behavior nodes"""
        return self.get_nodes_by_type(NodeType.BEHAVIOR)
    
    def get_decision_nodes(self) -> List[Node]:
        """Get all decision nodes"""
        return self.get_nodes_by_type(NodeType.DECISION)
    
    def has_decision_ancestry(self, node: Node) -> bool:
        """
        Check if a node can trace back to at least one DECISION node.
        This implements the Existence Axiom verification.
        """
        visited = set()
        stack = [node.id]
        
        while stack:
            current_id = stack.pop()
            if current_id in visited:
                continue
            visited.add(current_id)
            
            current = self.nodes[current_id]
            if current.type == NodeType.DECISION:
                return True
            
            # Traverse incoming edges
            for edge in self.get_incoming_edges(current_id):
                stack.append(edge.source)
        
        return False
    
    def find_contradictions(self) -> List[Contradiction]:
        """
        Detect logical contradictions in the graph.
        
        A contradiction exists when:
        1. Two nodes have explicit CONTRADICTS edges
        2. Two decisions require mutually exclusive resources
        3. Two constraints cannot be satisfied simultaneously
        """
        contradictions = []
        
        # Find explicit contradictions
        for edge in self.edges.values():
            if edge.type == EdgeType.CONTRADICTS:
                source = self.nodes[edge.source]
                target = self.nodes[edge.target]
                
                contradictions.append(Contradiction(
                    node_a=source,
                    node_b=target,
                    explanation=edge.metadata.get("reason", "Explicit contradiction"),
                    severity=edge.metadata.get("severity", 0.9),
                    causal_chain=[source.name, "contradicts", target.name]
                ))
        
        # Find resource contradictions
        resource_contradictions = self._find_resource_contradictions()
        contradictions.extend(resource_contradictions)
        
        # Find logical contradictions (e.g., HA + Single DB)
        logical_contradictions = self._find_logical_contradictions()
        contradictions.extend(logical_contradictions)
        
        return contradictions
    
    def _find_resource_contradictions(self) -> List[Contradiction]:
        """Find contradictions in resource allocation"""
        contradictions = []
        resource_nodes = self.get_nodes_by_type(NodeType.RESOURCE)
        
        for resource in resource_nodes:
            # Find all decisions that require this resource
            consumers = []
            for edge in self.get_incoming_edges(resource.id):
                if edge.type == EdgeType.REQUIRES:
                    consumers.append(self.nodes[edge.source])
            
            # Check if resource capacity is exceeded
            if len(consumers) > 1:
                capacity = resource.metadata.get("capacity", 1)
                total_demand = sum(c.metadata.get("resource_demand", 1) for c in consumers)
                
                if total_demand > capacity:
                    contradictions.append(Contradiction(
                        node_a=consumers[0],
                        node_b=consumers[1] if len(consumers) > 1 else consumers[0],
                        explanation=f"Resource '{resource.name}' oversubscribed: {total_demand} > {capacity}",
                        severity=0.85,
                        causal_chain=[
                            consumers[0].name,
                            f"requires {resource.name}",
                            consumers[1].name if len(consumers) > 1 else "self",
                            "resource_exhausted"
                        ]
                    ))
        
        return contradictions
    
    def _find_logical_contradictions(self) -> List[Contradiction]:
        """
        Find logical contradictions like:
        - High Availability + Single Point of Failure
        - Zero Downtime + Manual Deployment
        - Stateless + In-Memory Cache
        """
        contradictions = []
        decisions = self.get_decision_nodes()
        
        # Pattern: HA + Single DB
        ha_decisions = [d for d in decisions if "high" in d.name.lower() and "availab" in d.name.lower()]
        single_points = [d for d in decisions if "single" in d.name.lower()]
        
        for ha in ha_decisions:
            for sp in single_points:
                contradictions.append(Contradiction(
                    node_a=ha,
                    node_b=sp,
                    explanation=f"High availability cannot coexist with single point of failure",
                    severity=0.95,
                    causal_chain=[ha.name, "requires_redundancy", sp.name, "lacks_redundancy"]
                ))
        
        # Pattern: Stateless + Stateful resource
        stateless = [d for d in decisions if "stateless" in d.name.lower()]
        stateful = [d for d in decisions if "state" in d.name.lower() and "stateless" not in d.name.lower()]
        
        for sl in stateless:
            for sf in stateful:
                contradictions.append(Contradiction(
                    node_a=sl,
                    node_b=sf,
                    explanation=f"Stateless architecture contradicts stateful component",
                    severity=0.7,
                    causal_chain=[sl.name, "requires_no_state", sf.name, "maintains_state"]
                ))
        
        return contradictions
    
    def compute_causal_paths(self, from_node_id: str, to_node_id: str) -> List[List[str]]:
        """
        Compute all causal paths from one node to another.
        Returns list of paths, where each path is a list of node IDs.
        """
        paths = []
        visited = set()
        current_path = []
        
        def dfs(node_id: str):
            if node_id in visited:
                return
            
            visited.add(node_id)
            current_path.append(node_id)
            
            if node_id == to_node_id:
                paths.append(list(current_path))
            else:
                for edge in self.get_outgoing_edges(node_id):
                    if edge.type in [EdgeType.CAUSES, EdgeType.ENABLES, EdgeType.REQUIRES]:
                        dfs(edge.target)
            
            current_path.pop()
            visited.remove(node_id)
        
        dfs(from_node_id)
        return paths
    
    def get_critical_nodes(self, threshold: float = 0.7) -> List[Node]:
        """Get nodes with criticality above threshold"""
        return [n for n in self.nodes.values() if n.criticality >= threshold]
    
    def to_dict(self) -> Dict[str, Any]:
        """Export graph as dictionary for serialization"""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "type": n.type.value,
                    "name": n.name,
                    "description": n.description,
                    "criticality": n.criticality,
                    "metadata": n.metadata
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "id": e.id,
                    "source": e.source,
                    "target": e.target,
                    "type": e.type.value,
                    "weight": e.weight,
                    "confidence": e.confidence,
                    "metadata": e.metadata
                }
                for e in self.edges.values()
            ]
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "decisions": len(self.get_decision_nodes()),
            "behaviors": len(self.get_behavior_nodes()),
            "assumptions": len(self.get_nodes_by_type(NodeType.ASSUMPTION)),
            "constraints": len(self.get_nodes_by_type(NodeType.CONSTRAINT)),
            "critical_nodes": len(self.get_critical_nodes()),
        }
