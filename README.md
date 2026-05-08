# Quantum Simulation of the H₂ Molecule Potential Energy Surface
 
A production-grade quantum chemistry project demonstrating the simulation of hydrogen molecule (H₂) properties using IBM Qiskit. Progresses from a classical baseline through quantum algorithms, noise simulation, and hardware execution.
 
## 📋 Project Overview
 
This project implements all phases described in the original specification:
 
- **Phase 0**: Classical baseline using exact numpy diagonalization
- **Phase 1**: Variational Quantum Eigensolver (VQE) with UCCSD ansatz
- **Phase 2**: Quantum noise modeling and error mitigation (ZNE, readout correction)
- **Phase 3**: Chemical accuracy: basis sets, active space, multi-molecule systems
- **Phase 4**: Hardware execution on real IBM Quantum devices
- **Phase 5**: Demo script for sequential execution
## 🚀 Quick Start
 
### 1. Installation
 
```bash
# Clone or navigate to project directory
cd quantum_h2_project
 
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
 
# Install dependencies
pip install -r requirements.txt
```
 
### 2. Run Phase 0 (Baseline)
 
```bash
python src/phase0_baseline.py
```
 
Output:
- Energy scan across H-H distances (0.4–2.0 Å)
- Interpolated PES with spline fitting
- **Equilibrium bond length**: ~0.735 Å (matches experiment ≈ 0.74 Å)
- Plots saved to `results/phase0_pes.png`
### 3. Run Phase 1 (VQE)
 
```bash
# With UCCSD (chemistry-inspired, higher accuracy)
python src/phase1_vqe.py --ansatz uccsd --max_iter 300
 
# With RealAmplitudes (hardware-efficient)
python src/phase1_vqe.py --ansatz real_amplitudes --max_iter 300
```
 
Output:
- VQE energies at each distance (hybrid quantum-classical optimization)
- Comparison against exact baseline
- Energy error analysis
- Plots: `results/phase1_vqe_*.png`
### 4. Run Phase 2 (Noise & Mitigation)
 
```bash
# Noisy simulation at equilibrium distance (d = 0.735 Å)
python src/phase2_noise.py --distance 0.735 --shots 4096
 
# Skip ZNE (fast mode)
python src/phase2_noise.py --distance 0.735 --skip_zne
```
 
Output:
- Noiseless VQE baseline
- Noisy VQE (IBM Eagle-class hardware noise model)
- Readout error mitigation (linear correction)
- Zero Noise Extrapolation (Richardson method, scales 1–2–3)
- Comparison to chemical accuracy threshold (±1.6 mHa)
- Plots: `results/phase2_noise_mitigation.png`
### 5. Run Phase 3 (Chemistry & Accuracy)
 
```bash
# Basis set comparison: sto-3g, 6-31g, cc-pVDZ
python src/phase3_chemistry.py --task basis
 
# Active space reduction: show qubit savings
python src/phase3_chemistry.py --task active_space
 
# Multi-molecule PES: LiH and BeH₂
python src/phase3_chemistry.py --task molecules
 
# Run all tasks
python src/phase3_chemistry.py --task all
```
 
Output:
- Basis set convergence for H₂
- Qubit reduction via frozen-core transformer
  - H₂ (sto-3g): 2 orbs → 4 qubits
  - LiH (sto-3g): 5 orbs → 10 qubits (frozen-core: 2 → 4 qubits)
  - BeH₂ (sto-3g): 9 orbs → 18 qubits (frozen-core: 3 → 6 qubits)
- PES for LiH and BeH₂ (equilibrium distances)
- Plots: `results/phase3_*.png`
### 6. Run Phase 4 (Hardware Execution)
 
#### List Available Backends
 
```bash
python src/phase4_hardware.py --list_backends
```
 
#### Local Simulator (No Credentials Required)
 
```bash
python src/phase4_hardware.py --backend simulator --max_iter 300
```
 
#### Real Hardware (Requires IBM Quantum Account)
 
First, set up IBM Quantum credentials:
 
```python
# One-time setup in Python REPL
from qiskit_ibm_runtime import QiskitRuntimeService
 
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_API_TOKEN"  # Get from https://quantum.ibm.com
)
```
 
Then run on hardware:
 
```bash
python src/phase4_hardware.py --backend ibm_brisbane --shots 1024
```
 
Output:
- Baseline (local simulator)
- Hardware result (if available)
- Energy comparison and error analysis
- Plot: `results/phase4_hardware_comparison.png`
---
 
## 📊 Results & Output
 
All runs produce:
 
1. **Plots** (PNG): Potential energy surfaces, noise comparisons, basis set analysis
2. **CSV data**: Energy values for further analysis
3. **JSON metadata**: Timestamps, parameters, results (Phase 4)
Directory structure:
 
```
results/
├── phase0_pes.png
├── phase0_energies.csv
├── phase1_vqe_uccsd.png
├── phase1_vqe_uccsd.csv
├── phase2_noise_mitigation.png
├── phase3_basis_comparison.png
├── phase3_molecules.png
└── phase4_hardware_comparison.png
```
 
---
 
## 🧬 Scientific Background
 
### Potential Energy Surface (PES)
 
The PES describes the energy of the H₂ molecule as a function of the bond length (distance between nuclei). The minimum of this curve corresponds to the equilibrium bond length where the molecule is most stable.
 
### Jordan-Wigner Mapping
 
Electrons are fermions; quantum computers manipulate qubits. The Jordan-Wigner transformation maps fermionic creation/annihilation operators to Pauli (X, Y, Z) operators:
 
```
2 spatial orbitals  →  4 qubits (spin α, β per orbital)
```
 
### Variational Quantum Eigensolver (VQE)
 
A hybrid quantum-classical algorithm for near-term quantum computers (NISQ era):
 
1. **Ansatz**: Parameterized quantum circuit (UCCSD, RealAmplitudes)
2. **Loop**:
   - Quantum device evaluates ⟨ψ(θ) | H | ψ(θ) ⟩ (energy expectation)
   - Classical optimizer (COBYLA, SPSA) updates parameters θ
3. **Convergence**: Energy value converges to ground-state estimate
### Error Mitigation
 
Real quantum hardware is noisy. Two techniques demonstrated:
 
- **Zero Noise Extrapolation (ZNE)**: Measure at multiple noise levels; extrapolate to zero noise
- **Readout Error Mitigation**: Correct measurement bit-flip errors via probability distribution scaling
### Chemical Accuracy
 
Target: ±1.6 mHa (milli-Hartree) error relative to exact solution. Necessary for predicting reaction rates and molecular properties.
 
---
 
## 🔬 Technical Details
 
### Dependencies
 
- **qiskit** (1.0+): Quantum computing framework
- **qiskit-nature**: Molecular simulation module
- **qiskit-aer**: High-performance simulator with noise models
- **qiskit-algorithms**: VQE, QAOA, etc.
- **pyscf**: Electronic structure calculations (used via PySCFDriver)
- **scipy**: Spline interpolation, optimization
- **numpy, matplotlib**: Data handling and plotting
### Basis Sets
 
- **sto-3g**: Minimal, lightweight (good for learning)
- **6-31g**: More flexible, higher accuracy
- **cc-pVDZ**: Correlation-consistent, high accuracy (expensive in qubits)
### Hardware Notes
 
- **Qubit count**: 4 qubits for H₂ (sto-3g), 10+ for larger systems
- **Gate depth**: UCCSD ansatz can be deep; hardware-efficient ansätze trade accuracy for depth
- **Coherence time**: Must be long relative to circuit execution time
- **Typical backends**: IBM Falcon (27Q), Heron (133Q), Eagle (127Q)
---
 
## 📈 Expected Results
 
### Phase 0 (Exact)
- Bond length: **0.7349 Å**
- Experimental reference: **0.7414 Å**
- Error: **0.9 mÅ** ✓
### Phase 1 (VQE + UCCSD)
- Matches Phase 0 (same basis set)
- Error vs exact: **< 0.1 mHa** (for well-converged optimization)
### Phase 2 (Noise)
- Noiseless VQE: matches Phase 1
- Noisy VQE: **5–20 mHa** error (depends on circuit depth)
- + Readout mitigation: **2–8 mHa** improvement
- + ZNE: **1–3 mHa** (can achieve chemical accuracy)
### Phase 3 (Basis Sets)
- **sto-3g**: 0.735 Å (4 qubits)
- **6-31g**: 0.740 Å (8 qubits)
- **cc-pVDZ**: 0.741 Å (10 qubits)
- Convergence toward experiment ✓
### Phase 3 (Active Space)
- LiH: 10 qubits → **4 qubits** (60% reduction)
- BeH₂: 18 qubits → **6 qubits** (67% reduction)
---
 
## 🛠️ Customization
 
### Modify Simulation Parameters
 
Edit `DISTANCES`, `BASIS_SET`, or other constants in each script:
 
```python
DISTANCES = np.arange(0.3, 2.5, 0.02)   # Finer grid
BASIS_SET = "6-31g"                      # Better basis
```
 
### Change Optimizer
 
In Phase 1, swap COBYLA for SPSA (gradient-free, fewer evaluations):
 
```python
optimizer = SPSA(maxiter=100, learning_rate=0.05)
```
 
### Custom Noise Model
 
In Phase 2, build a custom model:
 
```python
nm = build_noise_model(
    t1_us=50.0,      # Faster relaxation
    t2_us=40.0,
    gate1_err=2e-3,  # Higher gate error
    gate2_err=2e-2,
)
```
 
---
 
## 🐛 Troubleshooting
 
### ImportError for qiskit modules
 
Ensure all packages are installed:
```bash
pip install --upgrade qiskit qiskit-nature qiskit-aer qiskit-algorithms qiskit-ibm-runtime
```
 
### Phase 2 is slow
 
Skip ZNE (runs 3× more VQE optimizations):
```bash
python src/phase2_noise.py --skip_zne --distance 0.735
```
 
### Phase 1 convergence issues
 
Increase max iterations or reduce tolerance:
```bash
python src/phase1_vqe.py --ansatz uccsd --max_iter 500
```
 
### Hardware execution fails
 
1. Check credentials: `python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService().backends())"`
2. Verify backend is operational: `python src/phase4_hardware.py --list_backends`
3. Check queue time (may wait hours during peak usage)
---
 
## 📚 Further Reading
 
- **Qiskit Textbook**: https://qiskit.org/learn
- **Nature Reviews** (VQE review): arXiv:2012.09265
- **Error Mitigation**: arXiv:2210.08763
- **Chemical Accuracy**: https://en.wikipedia.org/wiki/Chemical_accuracy
---
 
## 📝 Project Structure
 
```
quantum_h2_project/
├── README.md                 (this file)
├── requirements.txt          (dependencies)
├── src/
│   ├── phase0_baseline.py    (classical exact diagonalization)
│   ├── phase1_vqe.py         (VQE with UCCSD/RealAmplitudes)
│   ├── phase2_noise.py       (noise modeling & mitigation)
│   ├── phase3_chemistry.py   (basis sets, active space, molecules)
│   ├── phase4_hardware.py    (IBM Quantum hardware execution)
│   ├── __init__.py
│   └── config.py
├── results/                  (output plots, data, JSON)
└── demo.py
```
 
---
 
## ✨ Key Takeaways
 
This project demonstrates:
 
1. **Quantum simulation** of real chemistry problems
2. **Hybrid quantum-classical** algorithms (VQE)
3. **Error mitigation** for near-term quantum hardware
4. **Multi-scale modeling**: from toy to realistic systems
5. **Hardware integration** with IBM Quantum cloud
6. **Scientific communication**: clear results, reproducible code
 
---
 
## 📄 License & Citation
 
This project is provided as-is for educational and research purposes.
 
If you use this code in research, please cite:
- Qiskit: https://doi.org/10.1038/s41534-021-00430-1
- VQE: Cao et al., Chem. Rev. 2021, 121, 5, 3073–3126
---
 
## 🤝 Contributing
 
Ideas? Found a bug? Want to add:
- Adaptive VQE (adapt the ansatz dynamically)
- Parities error correction
- More molecules (H₂O, NH₃, etc.)
- Notebook tutorials
Feel free to extend this project!
 
---
 
**Last Updated**: 2025-05-08  
**Status**: Complete & Production-Ready ✓
