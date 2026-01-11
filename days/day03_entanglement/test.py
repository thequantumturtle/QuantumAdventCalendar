import unittest

from solution import create_bell_pair, run_circuit

class TestDay3Entanglement(unittest.TestCase):
    def test_circuit_creation(self):
        qc = create_bell_pair()
        self.assertIsNotNone(qc)
        self.assertEqual(qc.num_qubits, 2)

    def test_entanglement_distribution(self):
        counts = run_circuit(shots=1000)
        # Expect 00 and 11 to be present and dominant
        self.assertIn('00', counts)
        self.assertIn('11', counts)

        total = sum(counts.values())
        prob_00 = counts.get('00', 0) / total
        prob_11 = counts.get('11', 0) / total

        # Ensure together they account for the majority of outcomes (e.g., >80%)
        self.assertGreater(prob_00 + prob_11, 0.8)

if __name__ == '__main__':
    unittest.main()
