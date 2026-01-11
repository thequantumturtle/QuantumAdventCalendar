from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_bell_pair():
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(q, c)

    # Prepare Bell state |Φ+> = (|00> + |11>)/√2
    circuit.h(q[0])
    circuit.cx(q[0], q[1])

    # Measure both qubits
    circuit.measure(q[0], c[0])
    circuit.measure(q[1], c[1])

    return circuit

def run_circuit(shots=1000):
    qc = create_bell_pair()
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)
    return counts

if __name__ == "__main__":
    counts = run_circuit()
    print(counts)
