# Day 4 — Quantum Gates

Today you'll implement and explore basic single-qubit quantum gates and how they act on qubit state vectors.

Goals
- Implement the Pauli-X (NOT) gate, the Hadamard gate, and the Pauli-Z gate (matrices are provided in the reference).
- Write a small simulator function that applies a 2x2 gate to a 2-element state vector.
- Verify behavior by running the provided tests.

Tasks
1. Implement `apply_gate(state, gate)` in `solution.py`.
2. Use the provided matrices to observe how the gates transform the computational basis states `|0>` and `|1>`.
3. Run `pytest` in this day's folder to confirm tests pass.

Reference matrices

- Pauli-X (X):

```
[[0, 1],
 [1, 0]]
```

- Hadamard (H):

```
1/sqrt(2) * [[1,  1],
             [1, -1]]
```

- Pauli-Z (Z):

```
[[1,  0],
 [0, -1]]
```

Hints
- Use NumPy for vector/matrix operations.
- Normalize state vectors if you build them manually.

Good luck! Share any improvements or an extended challenge if you'd like to add multi-qubit gates next.
