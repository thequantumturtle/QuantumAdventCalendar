# Day 3: Entanglement

Explore entanglement by creating a Bell pair (maximally entangled two-qubit state) and observing correlated outcomes.

Your task:

1. Create a 2-qubit circuit that prepares the Bell state |Φ+> = (|00> + |11>)/√2
2. Measure both qubits and run the circuit on AerSimulator for 1000 shots
3. Verify that outcomes `00` and `11` dominate and are roughly equal, while `01` and `10` are near-zero

Hints:
- Apply a Hadamard to qubit 0, then a CNOT with control qubit 0 and target qubit 1
- Measure both qubits into two classical bits

Good luck!
