"""
Unit Tests for Singularity Delta Engine
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import Engine
from core.result import AnalysisResult
from core.context import ExecutionContext
from rules.completeness import CompletenessRule, DecisionCompletenessRule
from rules.consistency import DecisionConsistencyRule
from rules.structure import DecisionStructureRule


class TestAnalysisResult(unittest.TestCase):
    """Test AnalysisResult class"""
    
    def test_initialization(self):
        """Test result initialization"""
        result = AnalysisResult()
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(len(result.findings), 0)
    
    def test_add_finding(self):
        """Test adding findings"""
        result = AnalysisResult()
        finding = {"id": "TEST", "severity": "HIGH", "message": "Test finding"}
        result.add_finding(finding)
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0]["id"], "TEST")
    
    def test_to_dict(self):
        """Test dictionary export"""
        result = AnalysisResult()
        result.target = "test-system"
        result.verdict = "PASSED"
        data = result.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["target"], "test-system")


class TestExecutionContext(unittest.TestCase):
    """Test ExecutionContext class"""
    
    def test_initialization(self):
        """Test context initialization"""
        context = ExecutionContext()
        self.assertIsInstance(context.config, dict)
        self.assertIsInstance(context.cache, dict)
        self.assertFalse(context.strict_mode)
    
    def test_set_get(self):
        """Test storing and retrieving values"""
        context = ExecutionContext()
        context.set("test_key", "test_value")
        self.assertEqual(context.get("test_key"), "test_value")
    
    def test_has(self):
        """Test key existence check"""
        context = ExecutionContext()
        context.set("existing_key", "value")
        self.assertTrue(context.has("existing_key"))
        self.assertFalse(context.has("nonexistent_key"))


class TestEngine(unittest.TestCase):
    """Test Engine class"""
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        rules = [CompletenessRule()]
        engine = Engine(rules=rules)
        self.assertEqual(len(engine.rules), 1)
    
    def test_engine_run_valid_data(self):
        """Test engine with valid data"""
        data = {
            "system_name": "test-system",
            "decisions": [
                {"id": "D1", "description": "Decision 1"}
            ],
            "constraints": {}
        }
        rules = [CompletenessRule()]
        engine = Engine(rules=rules)
        result = engine.run(data, "test-system")
        
        self.assertIsInstance(result, AnalysisResult)
        self.assertEqual(result.target, "test-system")
        self.assertIn(result.verdict, ["PASSED", "WARNING", "FAILED"])
    
    def test_engine_run_invalid_data(self):
        """Test engine with invalid data"""
        data = {
            "system_name": "test-system"
            # Missing decisions and constraints
        }
        rules = [CompletenessRule()]
        engine = Engine(rules=rules)
        result = engine.run(data, "test-system")
        
        self.assertTrue(len(result.findings) > 0)
        self.assertEqual(result.verdict, "FAILED")
    
    def test_finalize_critical(self):
        """Test finalization with critical findings"""
        data = {"system_name": "test"}
        engine = Engine(rules=[])
        result = AnalysisResult()
        result.add_finding({"severity": "CRITICAL", "message": "Critical issue"})
        engine._finalize(result)
        
        self.assertEqual(result.verdict, "FAILED")
        self.assertEqual(result.risk, "CRITICAL")
        self.assertLess(result.score, 100)


class TestCompletenessRule(unittest.TestCase):
    """Test Completeness Rules"""
    
    def test_completeness_rule_pass(self):
        """Test completeness rule with valid data"""
        data = {
            "system_name": "test",
            "decisions": [],
            "constraints": {}
        }
        rule = CompletenessRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNone(result)
    
    def test_completeness_rule_fail(self):
        """Test completeness rule with missing keys"""
        data = {"system_name": "test"}
        rule = CompletenessRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNotNone(result)
        self.assertEqual(result["severity"], "HIGH")
    
    def test_decision_completeness_empty(self):
        """Test decision completeness with empty list"""
        data = {
            "system_name": "test",
            "decisions": []
        }
        rule = DecisionCompletenessRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNotNone(result)


class TestConsistencyRule(unittest.TestCase):
    """Test Consistency Rules"""
    
    def test_decision_consistency_duplicates(self):
        """Test decision consistency with duplicates"""
        data = {
            "decisions": [
                {"id": "D1", "description": "First"},
                {"id": "D1", "description": "Duplicate"}
            ]
        }
        rule = DecisionConsistencyRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNotNone(result)
        self.assertEqual(result["severity"], "CRITICAL")
    
    def test_decision_consistency_unique(self):
        """Test decision consistency with unique IDs"""
        data = {
            "decisions": [
                {"id": "D1", "description": "First"},
                {"id": "D2", "description": "Second"}
            ]
        }
        rule = DecisionConsistencyRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNone(result)


class TestStructureRule(unittest.TestCase):
    """Test Structure Rules"""
    
    def test_decision_structure_valid(self):
        """Test decision structure with valid decisions"""
        data = {
            "decisions": [
                {"id": "D1", "description": "Valid decision"}
            ]
        }
        rule = DecisionStructureRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNone(result)
    
    def test_decision_structure_missing_fields(self):
        """Test decision structure with missing fields"""
        data = {
            "decisions": [
                {"id": "D1"}  # Missing description
            ]
        }
        rule = DecisionStructureRule()
        result = rule.evaluate(data, ExecutionContext())
        self.assertIsNotNone(result)
        self.assertEqual(result["severity"], "HIGH")


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline"""
        from rules import DEFAULT_RULES
        
        data = {
            "system_name": "integration-test",
            "decisions": [
                {
                    "id": "D1",
                    "description": "Test decision",
                    "priority": 50,
                    "confidence": 0.8
                }
            ],
            "constraints": {
                "C1": {
                    "type": "timing",
                    "applies_to": ["D1"]
                }
            },
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01",
                "author": "test"
            }
        }
        
        engine = Engine(rules=DEFAULT_RULES)
        result = engine.run(data, "integration-test")
        
        self.assertIsInstance(result, AnalysisResult)
        self.assertEqual(result.target, "integration-test")
        self.assertIsNotNone(result.verdict)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
