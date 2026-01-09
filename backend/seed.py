"""
Seed database with challenges
"""

from app import app, db, Challenge

CHALLENGES = [
    {
        'day': 1,
        'title': 'Qubits 101',
        'description': '''
        Your first quantum challenge! Create a quantum circuit with a single qubit.
        Apply a Hadamard gate to put it in superposition, then measure it.
        Verify that the measurement probabilities are 50/50.
        
        **Your task:**
        1. Create a QuantumCircuit with 1 qubit and 1 classical bit
        2. Apply a Hadamard gate to the qubit
        3. Measure the qubit into the classical bit
        4. Run on AerSimulator with 1000 shots
        5. Verify both |0⟩ and |1⟩ appear roughly equally
        ''',
        'starter_code': '''from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    """Create a quantum circuit with a Hadamard gate"""
    # TODO: Implement this function
    pass

def run_circuit():
    """Execute the circuit and return measurement counts"""
    # TODO: Implement this function
    pass

if __name__ == "__main__":
    qc = create_hadamard_circuit()
    counts = run_circuit()
    print(counts)
''',
        'test_code': '''
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

if __name__ == '__main__':
    unittest.main()
''',
        'difficulty': 1
    },
    {
        'day': 2,
        'title': 'Superposition',
        'description': '''
        Explore superposition with multiple qubits!
        Create a 2-qubit system in equal superposition and observe the outcomes.
        
        **Your task:**
        1. Create a QuantumCircuit with 2 qubits and 2 classical bits
        2. Apply Hadamard gates to both qubits
        3. Measure both qubits
        4. Run on AerSimulator with 1000 shots
        5. Verify all 4 states (00, 01, 10, 11) appear roughly equally (~250 each)
        ''',
        'starter_code': '''from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_superposition_circuit():
    """Create a 2-qubit superposition circuit"""
    # TODO: Implement this function
    pass

def run_circuit():
    """Execute the circuit and return measurement counts"""
    # TODO: Implement this function
    pass

if __name__ == "__main__":
    qc = create_superposition_circuit()
    counts = run_circuit()
    print(counts)
''',
        'test_code': '''
import unittest

class TestDay2(unittest.TestCase):
    def test_four_states(self):
        counts = run_circuit()
        
        # All 4 states should appear
        for state in ['00', '01', '10', '11']:
            self.assertIn(state, counts)
        
        total = sum(counts.values())
        
        # Each should be roughly 25%
        for state in ['00', '01', '10', '11']:
            prob = counts[state] / total
            self.assertGreater(prob, 0.15)
            self.assertLess(prob, 0.35)

if __name__ == '__main__':
    unittest.main()
''',
        'difficulty': 1
    }
]

def seed_database():
    """Seed database with initial challenges"""
    with app.app_context():
        db.create_all()
        
        # Clear existing challenges
        Challenge.query.delete()
        
        # Add challenges
        for challenge_data in CHALLENGES:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
        
        db.session.commit()
        print(f"Seeded {len(CHALLENGES)} challenges")

if __name__ == '__main__':
    seed_database()
