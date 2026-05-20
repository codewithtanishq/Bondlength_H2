# Quantum Simulation of the H₂ Molecule Potential Energy Surface

This repository implements a complete H₂ potential energy surface (PES) simulation project using Qiskit. It now includes a higher-resolution dataset and a more accurate UCCSD VQE execution, plus a formal project report.

## Highlights
- Phase 0 and Phase 1 scans use a fine `0.02 Å` distance step for improved PES resolution.
- Phase 1 VQE uses `UCCSD` with the `SLSQP` optimizer for stable and accurate convergence.
- The new UCCSD dataset is available in `results/phase1_vqe_uccsd.csv` and the plot is in `results/phase1_vqe_uccsd.png`.
- A complete, project-grade report is available in `report.md`.

## Execution
### Setup
```bash
cd /workspaces/codespaces-blank
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Phase 0 — Classical Baseline
```bash
python src/phase0_baseline.py
```
Generates: `results/phase0_energies.csv`, `results/phase0_pes.png`

### Phase 1 — VQE UCCSD
```bash
python src/phase1_vqe.py --ansatz uccsd --max_iter 300
```
Generates: `results/phase1_vqe_uccsd.csv`, `results/phase1_vqe_uccsd.png`

## Results Summary
- Phase 0 equilibrium bond length: **0.7349 Å**
- Phase 0 equilibrium energy: **-1.137306 Ha**
- Phase 1 equilibrium bond length: **0.7349 Å**
- Phase 1 equilibrium energy: **-1.137306 Ha**
- VQE energy error at the VQE minimum: **0.000 mHa**
- Maximum absolute VQE error across the scan: **0.001 mHa**

## Output Files
- `results/phase0_energies.csv`
- `results/phase0_pes.png`
- `results/phase1_vqe_uccsd.csv`
- `results/phase1_vqe_uccsd.png`
- `report.md`

## Notes
- The project uses a fixed random seed (`SEED = 42`) for reproducibility.
- The full report includes raw datasets, figures, experiment descriptions, error analysis, and conclusions.
