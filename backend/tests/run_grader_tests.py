"""
Simple test runner for the CodeGrader implementation.
Runs two cases:
- correct submission should pass
- incorrect submission should fail
"""
from grader import CodeGrader

# Test code taken from seed.py for Day 1
TEST_CODE = '''
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

# Correct user code
CORRECT_CODE = '''
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

# Incorrect user code (missing Hadamard)
INCORRECT_CODE = '''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(q, c)
    # forgot to apply H
    circuit.measure(q[0], c[0])
    return circuit

def run_circuit():
    simulator = AerSimulator()
    circuit = create_hadamard_circuit()
    result = simulator.run(circuit, shots=1000).result()
    return result.get_counts(circuit)
'''


def run_case(code, label):
    print(f"\n=== Running case: {label} ===")
    passed, results = CodeGrader.validate_solution(code, TEST_CODE)
    print(f"Passed: {passed}")
    print("Summary:")
    print(results.get('test_results'))
    if results.get('output'):
        print("Output:\n", results.get('output'))
    if results.get('error'):
        print("Error:\n", results.get('error'))

if __name__ == '__main__':
    run_case(CORRECT_CODE, 'Correct submission (expect PASS)')
    run_case(INCORRECT_CODE, 'Incorrect submission (expect FAIL)')
