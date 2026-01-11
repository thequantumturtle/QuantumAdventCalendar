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
        'day': 3,
        'title': 'Entanglement',
        'description': '''
        Create a maximally entangled Bell pair and observe correlated measurement outcomes.

        **Your task:**
        1. Prepare the Bell state |Φ+> using H and CNOT
        2. Measure both qubits and run on AerSimulator with 1000 shots
        3. Verify `00` and `11` dominate
        ''',
        'starter_code': '''from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_bell_pair():
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(q, c)

    # Prepare Bell state
    circuit.h(q[0])
    circuit.cx(q[0], q[1])

    circuit.measure(q[0], c[0])
    circuit.measure(q[1], c[1])

    return circuit

def run_circuit(shots=1000):
    qc = create_bell_pair()
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    return result.get_counts(qc)

if __name__ == "__main__":
    print(run_circuit())
''',
        'test_code': '''import unittest

from solution import create_bell_pair, run_circuit

class TestDay3Entanglement(unittest.TestCase):
    def test_circuit_creation(self):
        qc = create_bell_pair()
        self.assertIsNotNone(qc)
        self.assertEqual(qc.num_qubits, 2)

    def test_entanglement_distribution(self):
        counts = run_circuit(shots=1000)
        self.assertIn('00', counts)
        self.assertIn('11', counts)
        total = sum(counts.values())
        prob_00 = counts.get('00',0)/total
        prob_11 = counts.get('11',0)/total
        self.assertGreater(prob_00 + prob_11, 0.8)

if __name__ == '__main__':
    unittest.main()
''',
        'difficulty': 2
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
    """Create a 2-qubit superposition circuit."""
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(q, c)

    # Apply Hadamard to both qubits
    circuit.h(q[0])
    circuit.h(q[1])

    # Measure both qubits
    circuit.measure(q[0], c[0])
    circuit.measure(q[1], c[1])

    return circuit

def run_circuit(shots=1000):
    """Execute the circuit and return counts dictionary."""
    qc = create_superposition_circuit()
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)
    return counts

if __name__ == "__main__":
    counts = run_circuit()
    print(counts)
''',
        'test_code': '''import unittest

from solution import create_superposition_circuit, run_circuit

class TestDay2Superposition(unittest.TestCase):
    def test_circuit_creation(self):
        qc = create_superposition_circuit()
        self.assertIsNotNone(qc)
        # Expect 2 qubits and 2 classical bits
        self.assertEqual(qc.num_qubits, 2)
        self.assertEqual(len(qc.clbits), 2)

    def test_distribution(self):
        counts = run_circuit(shots=1000)
        # Ensure all four states are present
        for s in ['00', '01', '10', '11']:
            self.assertIn(s, counts)

        total = sum(counts.values())
        # Check approximate 25% per state with 10% absolute tolerance
        for s in ['00', '01', '10', '11']:
            prob = counts[s] / total
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
