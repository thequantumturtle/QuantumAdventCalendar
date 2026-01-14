import numpy as np

# Single-qubit computational basis
zero = np.array([1.0, 0.0])
one = np.array([0.0, 1.0])

# Gate matrices
H = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]])
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.array([[1.0, 0.0], [0.0, -1.0]])

def apply_gate(state, gate):
    """Apply a 2x2 gate matrix to a 2-element state vector.

    Args:
        state: array-like of length 2 (complex/float)
        gate: 2x2 array-like

    Returns:
        numpy.ndarray: resulting state vector (not automatically normalized)
    """
    state_arr = np.asarray(state, dtype=float)
    gate_arr = np.asarray(gate, dtype=float)
    return gate_arr.dot(state_arr)


if __name__ == "__main__":
    print("H |0> =", apply_gate(zero, H))
    print("X |0> =", apply_gate(zero, X))
    print("Z |1> =", apply_gate(one, Z))
