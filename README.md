# Quantum Advent Calendar

A daily quantum computing advent calendar featuring puzzles, challenges, and educational content for December 1-25.

## Overview

This project presents 25 days of quantum computing content, from foundational concepts to advanced algorithms and applications. Each day includes:

- **Challenge**: A quantum computing puzzle or problem
- **Tutorial**: Educational content and background
- **Solution**: Working code examples
- **Resources**: Additional reading and references

## Structure

```
QuantumAdventCalendar/
├── days/
│   ├── day01_qubits_101/
│   ├── day02_superposition/
│   ├── day03_entanglement/
│   └── ... (day04 through day25)
├── solutions/
├── resources/
├── README.md
└── requirements.txt
```

## Days Overview

### Week 1: Foundations
- **Day 1**: Qubits 101
- **Day 2**: Superposition
- **Day 3**: Entanglement
- **Day 4**: Quantum Gates
- **Day 5**: Quantum Circuits

### Week 2: Core Concepts
- **Day 6**: Measurement & Collapse
- **Day 7**: Bell States
- **Day 8**: Quantum Teleportation
- **Day 9**: Dense Coding
- **Day 10**: Quantum Key Distribution

### Week 3: Algorithms
- **Day 11**: Deutsch-Jozsa Algorithm
- **Day 12**: Grover's Search
- **Day 13**: Shor's Algorithm Intro
- **Day 14**: Variational Quantum Eigensolver (VQE)
- **Day 15**: Quantum Approximate Optimization Algorithm (QAOA)

### Week 4: Applications & Advanced Topics
- **Day 16**: Quantum Machine Learning
- **Day 17**: Quantum Neural Networks
- **Day 18**: Error Correction Intro
- **Day 19**: Topological Quantum Computing
- **Day 20**: Hybrid Classical-Quantum Algorithms

### Week 5: Practical & Cutting Edge
- **Day 21**: Quantum Simulation
- **Day 22**: Variational Quantum Algorithms
- **Day 23**: NISQ Era Algorithms
- **Day 24**: Quantum Cryptography Advanced
- **Day 25**: Future of Quantum Computing

## Getting Started

### Prerequisites
- Python 3.9+
- Qiskit (IBM's quantum framework)
- NumPy
- Jupyter Notebook (optional but recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/thequantumturtle/QuantumAdventCalendar.git
cd QuantumAdventCalendar

# Install dependencies
pip install -r requirements.txt
```

### Running Challenges

Each day's folder contains:
- `challenge.md` - Problem statement
- `tutorial.ipynb` - Educational content
- `solution.py` - Reference implementation
- `test.py` - Unit tests

```bash
# Run a specific day's solution
python solutions/day01_solution.py

# Or open the Jupyter notebook
jupyter notebook days/day01_qubits_101/tutorial.ipynb
```

## Project Goals

1. **Education**: Make quantum computing accessible to learners at all levels
2. **Hands-on Learning**: Provide working code for every concept
3. **Community**: Encourage contributions and discussions
4. **Practical Skills**: Bridge theory and implementation

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/day-xx-topic`)
3. Commit changes (`git commit -am 'Add Day XX: Topic'`)
4. Push to the branch (`git push origin feature/day-xx-topic`)
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Development & Contributor Guide

Please see `CONTRIBUTING.md` for full contributor guidelines, local Docker-based testing instructions, and pre-push hook behavior. We require Docker for local development to ensure parity with CI.

## Resources

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [IBM Quantum Network](https://quantum.ibm.com/)
- [Quantum Computing Report](https://quantumcomputingreport.com/)
- [Qiskit Textbook](https://qiskit.org/textbook/)

## Author

Created by [@thequantumturtle](https://github.com/thequantumturtle)

## Acknowledgments

- IBM Qiskit team
- Quantum computing community
- All contributors and learners
