# 🔬 Quantum Simulation of the H₂ Molecule Potential Energy Surface

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0.2-4B8BBE.svg)](https://qiskit.org)

A comprehensive educational project exploring quantum computing's potential for molecular simulation. This repository implements a multi-phase pipeline to simulate the hydrogen molecule (H₂) using classical and quantum computational methods.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Phases](#project-phases)
- [Results & Benchmarks](#results--benchmarks)
- [Project Structure](#project-structure)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## 🎯 Project Overview

This project investigates the potential energy surface (PES) of the hydrogen molecule (H₂) using both classical computational chemistry and quantum computing approaches. By comparing classical and quantum methods, it demonstrates how quantum computers can simulate molecular behavior and provides insight into the advantages and current limitations of quantum algorithms in chemistry.

### Why H₂?
The hydrogen molecule is ideal for quantum computing research because:
- It's the simplest multi-electron molecule
- Its solution has been well-studied experimentally and theoretically
- It requires only 4 qubits for minimal basis sets
- It serves as a benchmark for quantum algorithm development

## ⭐ Key Features

- **5-Phase Simulation Pipeline**: From classical baseline to hardware-optimized quantum circuits
- **Multiple Quantum Ansätze**: Support for VQE, UCCSD, and custom ansatz implementations
- **High-Resolution PES**: Fine 0.02 Å distance steps for accurate potential energy curves
- **Noise Simulation**: Error mitigation strategies and noise model integration
- **Multiple Basis Sets**: STO-3G, 6-31G, and cc-pVDZ support
- **Reproducible Results**: Fixed random seed (SEED = 42) for consistent outputs
- **Comprehensive Documentation**: Educational explanations and inline code comments

## 💻 System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2 recommended for Windows)
- **Python**: 3.10 or higher
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Disk Space**: ~500 MB (including dependencies)

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/quantum-h2-pes.git
cd quantum-h2-pes
```

### 2. Create Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import qiskit; print('Qiskit version:', qiskit.__version__)"
```

## 🚀 Quick Start

### Run All Phases (Demo Mode - Shortened for Speed)
```bash
python demo.py
```

### Run Individual Phases

**Phase 0: Classical Baseline (Fast)**
```bash
python src/phase0_baseline.py
```

**Phase 1: Variational Quantum Eigensolver (VQE)**
```bash
python src/phase1_vqe.py --ansatz uccsd --max_iter 300
```

**Phase 2: Noise Simulation & Mitigation**
```bash
python src/phase2_noise.py --noise_level 0.01
```

**Phase 3: Chemistry & Larger Molecules**
```bash
python src/phase3_chemistry.py --basis sto-3g
```

**Phase 4: Hardware-Optimized Circuits**
```bash
python src/phase4_hardware.py --backend qasm_simulator
```

## 📊 Project Phases

### Phase 0: Classical Baseline ⚙️
**Purpose**: Establish reference values using exact classical diagonalization
- **Method**: NumPyMinimumEigensolver (exact eigenvalue solver)
- **Output**: `phase0_energies.csv`, `phase0_pes.png`
- **Runtime**: ~10-30 seconds

### Phase 1: Variational Quantum Eigensolver (VQE) ⚛️
**Purpose**: Find ground state energy using quantum variational methods
- **Ansatz**: UCCSD (Unitary Coupled Cluster with Single and Double excitations)
- **Optimizer**: SLSQP (Sequential Least Squares Programming)
- **Output**: `phase1_vqe_uccsd.csv`, `phase1_vqe_uccsd.png`
- **Runtime**: ~2-5 minutes (depending on iterations)

### Phase 2: Noise & Error Mitigation 🔊
**Purpose**: Simulate realistic quantum hardware noise and test mitigation strategies
- **Noise Models**: Depolarizing, amplitude damping, phase damping
- **Mitigation**: Zero-noise extrapolation techniques
- **Output**: `phase2_noise_mitigation.png`
- **Runtime**: ~1-3 minutes

### Phase 3: Quantum Chemistry & Basis Sets 🧪
**Purpose**: Explore different basis sets and larger molecular systems
- **Basis Sets**: STO-3G, 6-31G, cc-pVDZ
- **Molecules**: H₂, Li₂ (extensible framework)
- **Output**: CSV and PNG files per basis set
- **Runtime**: ~3-10 minutes

### Phase 4: Hardware-Optimized Circuits ⚙️🔧
**Purpose**: Generate hardware-ready quantum circuits
- **Optimization**: Circuit transpilation for different backends
- **Backends**: QASM simulator, FakeMelbourne, FakeNairobi (preview)
- **Output**: Optimized circuits and execution data
- **Runtime**: ~1-2 minutes

## 📈 Results & Benchmarks

### Reference Results (STO-3G Basis)

| Metric | Value | Unit |
|--------|-------|------|
| **Phase 0 - Equilibrium Bond Length** | 0.7349 | Å |
| **Phase 0 - Equilibrium Energy** | -1.137306 | Ha |
| **Phase 1 - Equilibrium Bond Length** | 0.7349 | Å |
| **Phase 1 - Equilibrium Energy** | -1.137306 | Ha |
| **VQE Error at Minimum** | 0.000 | mHa |
| **Maximum Absolute VQE Error** | 0.001 | mHa |
| **Convergence Rate (Phase 1)** | 93.5% | % (at 300 iterations) |

### Performance Metrics
- **Phase 0 Runtime**: ~15 seconds
- **Phase 1 Runtime**: ~180 seconds
- **Total Runtime (All Phases)**: ~8-10 minutes
- **Memory Usage**: ~800 MB peak

## 📁 Project Structure

```
quantum-h2-pes/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── requirements.txt                   # Python dependencies
├── demo.py                            # Quick-start demo script
├── explanation.md                     # Educational overview
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── config.py                      # Centralized configuration
│   ├── phase0_baseline.py             # Classical diagonalization
│   ├── phase1_vqe.py                  # Quantum VQE solver
│   ├── phase2_noise.py                # Noise simulation
│   ├── phase3_chemistry.py            # Multiple basis sets
│   └── phase4_hardware.py             # Hardware optimization
│
├── results/                           # Output directory
│   ├── phase0_energies.csv            # Classical results
│   ├── phase0_pes.png                 # Potential energy surface plot
│   ├── phase1_vqe_uccsd.csv           # VQE results
│   ├── phase1_vqe_uccsd.png           # VQE PES plot
│   └── phase2_noise_mitigation.png    # Noise analysis plot
│
└── assets/                            # Documentation assets
    ├── README.md
    └── figures/
```

## 🔧 Advanced Usage

### Custom Configuration
Edit `src/config.py` to modify:
- Distance scan range: `DISTANCE_MIN`, `DISTANCE_MAX`, `DISTANCE_STEP_*`
- Random seed: `SEED`
- Basis sets and their parameters
- Optimizer settings and iteration counts

### Run Only Specific Phases
```bash
# Run only Phase 0 and Phase 1
python demo.py --phase 0 --phase 1

# Skip expensive Phase 2
python demo.py --skip_phase 2

# Combine options
python demo.py --phase 3 --phase 4
```

### Enable Debug Logging
```bash
export QISKIT_SETTINGS_DEBUG=1
python src/phase1_vqe.py
```

### Parallel Execution
Run phases in separate terminals for parallel computation:
```bash
# Terminal 1
python src/phase0_baseline.py

# Terminal 2
python src/phase1_vqe.py --ansatz uccsd --max_iter 300
```

## 🤝 Contributing

Contributions are welcome! This is an educational project, and we appreciate:
- Bug reports and fixes
- Documentation improvements
- New phase implementations
- Performance optimizations
- Educational content

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup
```bash
git clone <your-fork>
cd quantum-h2-pes
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Make your changes
git commit -m "feat: description of changes"
git push origin feature/your-feature
# Create Pull Request on GitHub
```

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## 📚 References

### Key Papers & Resources
- Cao, Y., Aspuru-Guzik, A. (2018). Quantum Chemistry in the Age of Quantum Computing. *Journal of Chemical Theory and Computation*, 15(8), 4332-4338.
- Cerezo, M., et al. (2021). Variational quantum algorithms. *Nature Reviews Physics*, 3, 625-644.
- O'Malley, P. J. J., et al. (2016). Scalable Quantum Simulation of Molecular Energies. *Physical Review X*, 6, 031007.

### Learning Resources
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)
- [Variational Quantum Eigensolver (VQE) Tutorial](https://qiskit.org/textbook/ch-applications/vqe-molecules.html)
- [PySCF Documentation](https://pyscf.org/)

## ❓ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'qiskit'"
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Connection error to IBM Quantum" (in Phase 1)
**Solution**: This is normal if not configured. The code uses local simulator by default.

### Issue: Out of memory errors
**Solution**: Try running phases individually rather than the full demo:
```bash
python src/phase0_baseline.py    # Low memory
python src/phase1_vqe.py         # Moderate memory (try first)
```

### Issue: Plots not saving correctly
**Solution**: Ensure `results/` directory exists and is writable:
```bash
mkdir -p results
chmod 755 results
```

## 📞 Support & Questions

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact project maintainers

## 🎓 Educational Use

This project is designed for educational purposes in quantum computing and computational chemistry. It's suitable for:
- University quantum computing courses
- Self-study and learning quantum algorithms
- Quantum computing research prototyping
- Physics and chemistry education

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
