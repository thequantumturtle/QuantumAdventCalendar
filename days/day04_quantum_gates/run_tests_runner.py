"""Simple test runner for Day 4 that doesn't require pytest.

Run with: python run_tests_runner.py
"""
import numpy as np
from solution import apply_gate, H, X, Z, zero, one


def main():
    tests = []

    def t1():
        out = apply_gate(zero, X)
        assert np.allclose(out, one)

    def t2():
        out = apply_gate(zero, H)
        expected = (1 / np.sqrt(2)) * np.array([1.0, 1.0])
        assert np.allclose(out, expected)

    def t3():
        out = apply_gate(one, Z)
        expected = -1 * one
        assert np.allclose(out, expected)

    tests = [t1, t2, t3]

    passed = 0
    for i, t in enumerate(tests, start=1):
        try:
            t()
            print(f"test_{i}: PASS")
            passed += 1
        except AssertionError:
            print(f"test_{i}: FAIL")
    print(f"{passed}/{len(tests)} tests passed")


if __name__ == "__main__":
    main()
