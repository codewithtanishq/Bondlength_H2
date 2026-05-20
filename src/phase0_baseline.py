"""
Phase 0 — Baseline: Classical Exact Diagonalizer (NumPyMinimumEigensolver)
============================================================================
Calculates the H₂ ground-state energy across interatomic distances using
the Jordan-Wigner mapping + exact numpy diagonalization as a noise-free
theoretical reference. Interpolates the PES with a spline to find the
precise equilibrium bond length.

Usage:
    python src/phase0_baseline.py
"""

import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import NumPyMinimumEigensolver

from config import Phase0Config, RESULTS_DIR


# ── Configuration ───────────────────────────────────────────────────────────

DISTANCES = Phase0Config.DISTANCES
BASIS_SET = Phase0Config.BASIS
RESULTS_DIR = str(RESULTS_DIR)


# ── Core simulation ──────────────────────────────────────────────────────────

def compute_pes_classical(distances: np.ndarray, basis: str = BASIS_SET) -> list[float]:
    """Return ground-state energies (Hartree) at each interatomic distance."""
    mapper = JordanWignerMapper()
    solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
    energies = []

    print(f"\n{'─'*55}")
    print(f"  Phase 0 — Classical Baseline  |  basis: {basis}")
    print(f"{'─'*55}")
    print(f"  {'Distance (Å)':>14}  {'Energy (Ha)':>14}")
    print(f"  {'─'*14}  {'─'*14}")

    for d in distances:
        geometry = f"H 0 0 0; H 0 0 {d:.3f}"
        driver = PySCFDriver(
            atom=geometry,
            basis=basis,
            charge=0,
            spin=0,
            unit=DistanceUnit.ANGSTROM,
        )
        problem = driver.run()
        result = solver.solve(problem)
        energy = result.total_energies[0].real
        energies.append(energy)
        print(f"  {d:>14.3f}  {energy:>14.6f}")

    return energies


# ── Spline interpolation ──────────────────────────────────────────────────────

def find_equilibrium(distances: np.ndarray, energies: list[float]) -> tuple[float, float]:
    """Fit a spline and return (bond_length_Å, min_energy_Ha)."""
    spline = UnivariateSpline(distances, energies, k=4, s=0)
    deriv = spline.derivative()
    roots = deriv.roots()
    if len(roots) == 0:
        index = int(np.argmin(energies))
        return float(distances[index]), float(energies[index])
    min_root = roots[np.argmin([spline(r) for r in roots])]
    return float(min_root), float(spline(min_root))


def save_metadata(path: str, metadata: dict) -> None:
    """Save a JSON metadata file next to generated results."""
    import json
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_pes(distances, energies, eq_dist, eq_energy, label="sto-3g (exact)"):
    spline = UnivariateSpline(distances, energies, k=4, s=0)
    d_fine = np.linspace(distances[0], distances[-1], 500)
    e_fine = spline(d_fine)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(d_fine, e_fine, color="#2196F3", linewidth=2.0, label=f"PES — {label}")
    ax.scatter(distances, energies, color="#2196F3", s=30, zorder=5, label="Simulation points")
    ax.axvline(eq_dist, color="#F44336", linestyle="--", linewidth=1.5,
               label=f"Bond length: {eq_dist:.4f} Å")
    ax.scatter([eq_dist], [eq_energy], color="#F44336", s=80, zorder=6)

    ax.set_xlabel("Interatomic Distance (Å)", fontsize=12)
    ax.set_ylabel("Ground-State Energy (Hartree)", fontsize=12)
    ax.set_title("H₂ Potential Energy Surface — Phase 0 Baseline", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = f"{RESULTS_DIR}/phase0_pes.png"
    fig.savefig(path, dpi=150)
    print(f"\n  Plot saved → {path}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    energies = compute_pes_classical(DISTANCES)
    eq_dist, eq_e = find_equilibrium(DISTANCES, energies)

    print(f"\n{'═'*55}")
    print(f"  Equilibrium bond length : {eq_dist:.4f} Å")
    print(f"  Ground-state energy     : {eq_e:.6f} Ha")
    print(f"  Experimental reference  : ~0.7400 Å")
    print(f"  Error vs experiment     : {abs(eq_dist - 0.74)*1000:.1f} mÅ")
    print(f"{'═'*55}\n")

    plot_pes(DISTANCES, energies, eq_dist, eq_e)

    csv_path = f"{RESULTS_DIR}/phase0_energies.csv"
    data = np.column_stack([DISTANCES, energies])
    np.savetxt(csv_path, data, delimiter=",", header="distance_angstrom,energy_hartree",
               comments="")
    print(f"  Data saved  → {csv_path}\n")


if __name__ == "__main__":
    main()
