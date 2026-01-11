from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
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

if __name__ == '__main__':
    counts = run_circuit()
    print(counts)
