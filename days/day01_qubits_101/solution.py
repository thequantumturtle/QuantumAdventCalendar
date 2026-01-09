"""
Day 1: Qubits 101
================

Challenge: Create a quantum circuit with a single qubit, apply a Hadamard gate,
and measure the result. Verify that the measurement probabilities are 50/50.

Background:
A qubit (quantum bit) is the fundamental unit of quantum information.
Unlike classical bits (0 or 1), qubits can exist in a superposition of both
states simultaneously, following quantum mechanics principles.

Key Concepts:
- Qubit: |ψ⟩ = α|0⟩ + β|1⟩, where |α|² + |β|² = 1
- Hadamard Gate: Creates equal superposition from basis states
- Measurement: Collapses superposition to classical outcome (0 or 1)
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

def create_hadamard_circuit():
    """Create a quantum circuit with a Hadamard gate on a single qubit."""
    
    # Create quantum and classical registers
    q = QuantumRegister(1, 'q')  # 1 qubit
    c = ClassicalRegister(1, 'c')  # 1 classical bit for measurement
    
    # Create the circuit
    circuit = QuantumCircuit(q, c)
    
    # Apply Hadamard gate to put qubit in superposition
    circuit.h(q[0])
    
    # Measure the qubit
    circuit.measure(q[0], c[0])
    
    return circuit

def run_circuit():
    """Execute the circuit and get results."""
    
    # Create the circuit
    qc = create_hadamard_circuit()
    
    # Use the Aer simulator
    simulator = AerSimulator()
    
    # Run the circuit 1000 times (shots)
    result = simulator.run(qc, shots=1000).result()
    counts = result.get_counts(qc)
    
    return counts

def verify_superposition(counts):
    """Verify that measurement results are approximately 50/50."""
    
    total_shots = sum(counts.values())
    
    # Get counts for 0 and 1
    count_0 = counts.get('0', 0)
    count_1 = counts.get('1', 0)
    
    prob_0 = count_0 / total_shots
    prob_1 = count_1 / total_shots
    
    print("Day 1: Qubits 101")
    print("=" * 40)
    print(f"Measurement results (out of {total_shots} shots):")
    print(f"  State |0⟩: {count_0} times ({prob_0:.1%})")
    print(f"  State |1⟩: {count_1} times ({prob_1:.1%})")
    print()
    
    # Check if approximately 50/50 (within 10%)
    tolerance = 0.10
    is_balanced = abs(prob_0 - 0.5) < tolerance and abs(prob_1 - 0.5) < tolerance
    
    if is_balanced:
        print("✓ Success! Superposition verified - probabilities are ~50/50")
    else:
        print("✗ Warning: Probabilities deviate from expected 50/50")
    
    return is_balanced

if __name__ == "__main__":
    # Run the circuit
    counts = run_circuit()
    
    # Verify results
    verify_superposition(counts)
