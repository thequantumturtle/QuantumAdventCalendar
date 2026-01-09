# Day 1: Qubits 101

## Challenge

Create a quantum circuit with a single qubit, apply a Hadamard gate, and measure the result. Verify that the measurement probabilities are 50/50.

## Learning Objectives

- Understand what a qubit is
- Learn about quantum superposition
- Create your first quantum circuit
- Apply the Hadamard gate
- Interpret measurement results

## Background

### What is a Qubit?

A **qubit** (quantum bit) is the fundamental unit of quantum information. Unlike a classical bit that is either 0 or 1, a qubit can exist in a **superposition** of both states simultaneously.

The state of a qubit is mathematically represented as:
```
|ψ⟩ = α|0⟩ + β|1⟩
```

Where:
- |0⟩ and |1⟩ are the basis states (like classical 0 and 1)
- α and β are complex amplitudes
- |α|² + |β|² = 1 (normalization condition)

The values |α|² and |β|² represent the probabilities of measuring 0 and 1, respectively.

### The Hadamard Gate

The **Hadamard gate** is one of the most important single-qubit gates. It transforms a basis state into an equal superposition:

```
H|0⟩ = (1/√2)(|0⟩ + |1⟩)
H|1⟩ = (1/√2)(|0⟩ - |1⟩)
```

When you apply a Hadamard gate to |0⟩, you get a state with 50% probability of measuring 0 and 50% probability of measuring 1.

### Measurement

When you **measure** a qubit, it collapses from its superposition state to a definite classical value (0 or 1). Each measurement result occurs with a probability determined by the amplitude squares.

## Solution Walkthrough

### Step 1: Import necessary modules

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
```

### Step 2: Create quantum and classical registers

```python
q = QuantumRegister(1, 'q')      # 1 qubit
c = ClassicalRegister(1, 'c')    # 1 classical bit
circuit = QuantumCircuit(q, c)   # Combine into circuit
```

### Step 3: Apply Hadamard gate

```python
circuit.h(q[0])  # Apply Hadamard to first qubit
```

### Step 4: Measure

```python
circuit.measure(q[0], c[0])  # Measure qubit, store in classical bit
```

### Step 5: Run and analyze

```python
simulator = AerSimulator()
result = simulator.run(circuit, shots=1000).result()
counts = result.get_counts(circuit)
```

## Expected Output

After running 1000 shots:
- State |0⟩: ~500 times (50%)
- State |1⟩: ~500 times (50%)

The slight variations are due to statistical randomness.

## Questions to Explore

1. What happens if you apply the Hadamard gate twice? Try it!
2. What would happen without the Hadamard gate?
3. Can you modify the circuit to measure in a different basis?

## Further Reading

- [Qiskit Textbook: Qubits](https://qiskit.org/textbook/what-is-quantum.html)
- [IBM Quantum: Single Qubit Gates](https://quantum.ibm.com/docs/faq)
- Nielsen & Chuang: "Quantum Computation and Quantum Information" Chapter 1

## See Also

- `solution.py` - Full working implementation
- `test.py` - Unit tests
