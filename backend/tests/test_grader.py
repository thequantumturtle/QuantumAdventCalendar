"""
Test suite for the CodeGrader module.
Tests correct and incorrect submissions using Day 1 challenge.
"""
import pytest
from grader import CodeGrader

# Test code for Day 1 (from seed.py)
DAY1_TEST_CODE = '''
import unittest

class TestDay1(unittest.TestCase):
    def test_circuit_execution(self):
        qc = create_hadamard_circuit()
        self.assertIsNotNone(qc)
    
    def test_hadamard_superposition(self):
        counts = run_circuit()
        self.assertIn('0', counts)
        self.assertIn('1', counts)
        
        total = sum(counts.values())
        prob_0 = counts['0'] / total
        prob_1 = counts['1'] / total
        
        # Allow 20% tolerance
        self.assertGreater(prob_0, 0.3)
        self.assertLess(prob_0, 0.7)
        self.assertGreater(prob_1, 0.3)
        self.assertLess(prob_1, 0.7)
'''

# Correct submission
CORRECT_SOLUTION = '''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(q, c)
    circuit.h(q[0])
    circuit.measure(q[0], c[0])
    return circuit

def run_circuit():
    simulator = AerSimulator()
    circuit = create_hadamard_circuit()
    result = simulator.run(circuit, shots=1000).result()
    return result.get_counts(circuit)
'''

# Incorrect submission (missing Hadamard gate)
INCORRECT_NO_HADAMARD = '''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(q, c)
    # forgot Hadamard!
    circuit.measure(q[0], c[0])
    return circuit

def run_circuit():
    simulator = AerSimulator()
    circuit = create_hadamard_circuit()
    result = simulator.run(circuit, shots=1000).result()
    return result.get_counts(circuit)
'''

# Incorrect submission (syntax error)
INCORRECT_SYNTAX = '''
def create_hadamard_circuit():
    return this is invalid python!
'''


class TestCodeGrader:
    """Test suite for CodeGrader class"""
    
    def test_correct_submission_passes(self):
        """Correct submission should pass all tests"""
        passed, results = CodeGrader.validate_solution(CORRECT_SOLUTION, DAY1_TEST_CODE)
        
        assert passed is True, "Correct solution should pass"
        assert results['test_results']['testsRun'] == 2
        assert results['test_results']['failures'] == 0
        assert results['test_results']['errors'] == 0
    
    def test_incorrect_submission_fails(self):
        """Incorrect submission (missing Hadamard) should fail"""
        passed, results = CodeGrader.validate_solution(INCORRECT_NO_HADAMARD, DAY1_TEST_CODE)
        
        assert passed is False, "Incorrect solution should fail"
        assert results['test_results']['testsRun'] == 2
        assert results['test_results']['failures'] >= 1, "Should have at least 1 failure"
    
    def test_syntax_error_submission(self):
        """Submission with syntax error should fail gracefully"""
        passed, results = CodeGrader.validate_solution(INCORRECT_SYNTAX, DAY1_TEST_CODE)
        
        assert passed is False, "Syntax error should fail"
        assert results['error'], "Should have an error message"
        assert 'SyntaxError' in results['error']
    
    def test_results_structure(self):
        """Results should have expected structure"""
        passed, results = CodeGrader.validate_solution(CORRECT_SOLUTION, DAY1_TEST_CODE)
        
        assert 'passed' in results
        assert 'output' in results
        assert 'error' in results
        assert 'test_results' in results
        assert isinstance(results['test_results'], dict)
        assert 'testsRun' in results['test_results']
        assert 'failures' in results['test_results']
        assert 'errors' in results['test_results']
