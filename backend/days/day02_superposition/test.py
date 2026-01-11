import unittest

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
