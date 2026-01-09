"""
Unit tests for Day 1: Qubits 101
"""

import unittest
from solution import create_hadamard_circuit, run_circuit, verify_superposition


class TestDay01(unittest.TestCase):
    
    def test_circuit_creation(self):
        """Test that circuit can be created without errors."""
        circuit = create_hadamard_circuit()
        self.assertIsNotNone(circuit)
        self.assertEqual(len(circuit), 3)  # h, measure operations
    
    def test_circuit_execution(self):
        """Test that circuit can be executed."""
        counts = run_circuit()
        self.assertIsNotNone(counts)
        self.assertTrue('0' in counts or '1' in counts)
    
    def test_superposition_verification(self):
        """Test that Hadamard creates valid superposition."""
        counts = run_circuit()
        total = sum(counts.values())
        
        # Both 0 and 1 should appear
        self.assertTrue('0' in counts)
        self.assertTrue('1' in counts)
        
        # Check that probabilities are roughly 50/50 (within 20%)
        prob_0 = counts['0'] / total
        prob_1 = counts['1'] / total
        
        self.assertGreater(prob_0, 0.3)
        self.assertLess(prob_0, 0.7)
        self.assertGreater(prob_1, 0.3)
        self.assertLess(prob_1, 0.7)
    
    def test_verify_superposition_function(self):
        """Test the verification function."""
        counts = run_circuit()
        result = verify_superposition(counts)
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()
