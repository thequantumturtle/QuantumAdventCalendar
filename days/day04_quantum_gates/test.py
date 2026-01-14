import numpy as np
from solution import apply_gate, H, X, Z, zero, one


def test_x_flips_zero_to_one():
    out = apply_gate(zero, X)
    assert np.allclose(out, one)


def test_h_on_zero_creates_equal_superposition():
    out = apply_gate(zero, H)
    expected = (1 / np.sqrt(2)) * np.array([1.0, 1.0])
    assert np.allclose(out, expected)


def test_z_on_one_introduces_minus_sign():
    out = apply_gate(one, Z)
    expected = -1 * one
    assert np.allclose(out, expected)
