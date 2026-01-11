# Day 2: Superposition

## Challenge

Create a quantum circuit with two qubits, apply Hadamard gates to both qubits, and measure the results. Verify that the measurement outcomes (00, 01, 10, 11) appear roughly equally when run with many shots.

## Learning Objectives

- Build multi-qubit circuits
- Create equal superposition across multiple qubits
- Measure and interpret multi-qubit outcomes
- Understand how probabilities distribute over basis states

## Background

Applying a Hadamard gate to each qubit in a 2-qubit system produces an equal superposition over all four computational basis states:

```
H ⊗ H |00⟩ = (1/2)(|00⟩ + |01⟩ + |10⟩ + |11⟩)
```

When executed with many shots, each of the four outcomes should appear approximately 25% of the time (allowing for sampling noise).

## Task

1. Create a `QuantumCircuit` with 2 qubits and 2 classical bits.
2. Apply Hadamard gates to both qubits.
3. Measure both qubits into classical bits.
4. Run the circuit with 1000 shots on `AerSimulator`.
5. Verify that each of the states `00`, `01`, `10`, and `11` appears with roughly equal probability (±10% tolerance).

## Starter Code

See `solution.py` for starter functions to implement.

## Tests

See `test.py` for unit tests that validate the circuit and the distribution of counts.


See Also

- `solution.py` — Starter implementation
- `test.py` — Unit tests
