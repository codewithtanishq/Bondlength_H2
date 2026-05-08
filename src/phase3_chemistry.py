"""
Phase 3 — Chemical Accuracy: Larger Basis Sets, Active Space & Bigger Molecules
================================================================================
Pushes beyond sto-3g to more realistic basis sets and demonstrates:
  • Basis set comparison  : sto-3g → 6-31G → cc-pVDZ for H₂
  • Active space reduction: FreezeCoreTransformer to tame qubit explosion
  • Multi-molecule PES    : LiH and BeH₂ (with active-space reduction)

Usage:
    python src/phase3_chemistry.py --task basis        # basis set comparison
    python src/phase3_chemistry.py --task active_space  # active space demo
    python src/phase3_chemistry.py --task molecules     # LiH / BeH2 PES
"""

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.transformers import FreezeCoreTransformer
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_algorithms import NumPyMinimumEigensolver

RESULTS_DIR = "results"


# ── Helpers ───────────────────────────────────────────────────────────────────

def solve_exact(geometry: str, basis: str, charge: int = 0, spin: int = 0,
                freeze_core: bool = False):
    driver = PySCFDriver(
        atom=geometry,
        basis=basis,
        charge=charge,
        spin=spin,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()

    if freeze_core:
        transformer = FreezeCoreTransformer()
        problem = transformer.transform(problem)

    mapper = JordanWignerMapper()
    solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
    result = solver.solve(problem)
    return result.total_energies[0].real, problem.num_spatial_orbitals, problem.num_particles


def qubit_count(n_spatial_orbs: int) -> int:
    return 2 * n_spatial_orbs


# ── Task 1: Basis set comparison ─────────────────────────────────────────────

def task_basis_comparison():
    basis_sets = ["sto-3g", "6-31g", "cc-pvdz"]
    distances = np.arange(0.4, 2.0, 0.05)

    print(f"\n{'─'*65}")
    print("  Task: Basis Set Comparison for H₂")
    print(f"{'─'*65}")

    results = {}
    for basis in basis_sets:
        energies = []
        for d in distances:
            geo = f"H 0 0 0; H 0 0 {d:.3f}"
            e, n_orbs, n_part = solve_exact(geo, basis)
            energies.append(e)
        results[basis] = energies

        sp = UnivariateSpline(distances, energies, k=4, s=0)
        roots = sp.derivative().roots()
        eq_d = roots[np.argmin([sp(r) for r in roots])]

        _, n_orbs, _ = solve_exact(f"H 0 0 0; H 0 0 0.74", basis)
        q_count = qubit_count(n_orbs)
        print(f"  {basis:<10} → eq. bond: {eq_d:.4f} Å  | "
              f"{n_orbs} spatial orbs → {q_count} qubits")

    _plot_basis_comparison(distances, results)


def _plot_basis_comparison(distances, results):
    colors = {"sto-3g": "#4CAF50", "6-31g": "#2196F3", "cc-pvdz": "#FF5722"}
    fig, ax = plt.subplots(figsize=(9, 5))

    for basis, energies in results.items():
        sp = UnivariateSpline(distances, energies, k=4, s=0)
        d_f = np.linspace(distances[0], distances[-1], 500)
        label = f"{basis} ({min(energies):.4f} Ha min)"
        ax.plot(d_f, sp(d_f), color=colors.get(basis, "gray"),
                linewidth=2, label=label)
        ax.scatter(distances, energies, color=colors.get(basis, "gray"), s=15)

    ax.set_xlabel("Interatomic Distance (Å)")
    ax.set_ylabel("Ground-State Energy (Ha)")
    ax.set_title("H₂ PES — Basis Set Comparison")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = f"{RESULTS_DIR}/phase3_basis_comparison.png"
    fig.savefig(path, dpi=150)
    print(f"\n  Plot saved → {path}")
    plt.close(fig)


# ── Task 2: Active space reduction ────────────────────────────────────────────

def task_active_space():
    print(f"\n{'─'*65}")
    print("  Task: Active Space Reduction")
    print(f"{'─'*65}")

    print("\n  H₂  (sto-3g, d=0.74 Å)")
    geo_h2 = "H 0 0 0; H 0 0 0.74"
    e_full, n_orbs_full, _ = solve_exact(geo_h2, "sto-3g", freeze_core=False)
    e_fc, n_orbs_fc, _ = solve_exact(geo_h2, "sto-3g", freeze_core=True)
    print(f"    Full space : {n_orbs_full} orbitals → {qubit_count(n_orbs_full)} qubits  "
          f" E = {e_full:.6f} Ha")
    print(f"    Frozen core: {n_orbs_fc} orbitals → {qubit_count(n_orbs_fc)} qubits  "
          f" E = {e_fc:.6f} Ha")

    print("\n  LiH  (sto-3g, d=1.60 Å)")
    geo_lih = "Li 0 0 0; H 0 0 1.6"
    e_full, n_orbs_full, _ = solve_exact(geo_lih, "sto-3g", freeze_core=False)
    e_fc, n_orbs_fc, _ = solve_exact(geo_lih, "sto-3g", freeze_core=True)
    print(f"    Full space : {n_orbs_full} orbitals → {qubit_count(n_orbs_full)} qubits  "
          f" E = {e_full:.6f} Ha")
    print(f"    Frozen core: {n_orbs_fc} orbitals → {qubit_count(n_orbs_fc)} qubits  "
          f" E = {e_fc:.6f} Ha")
    print(f"    Qubit saving: {qubit_count(n_orbs_full) - qubit_count(n_orbs_fc)} qubits")

    print("\n  BeH₂  (sto-3g, d=1.33 Å each H)")
    geo_beh2 = "Be 0 0 0; H 0 0 1.33; H 0 0 -1.33"
    e_full, n_orbs_full, _ = solve_exact(geo_beh2, "sto-3g", freeze_core=False)
    e_fc, n_orbs_fc, _ = solve_exact(geo_beh2, "sto-3g", freeze_core=True)
    print(f"    Full space : {n_orbs_full} orbitals → {qubit_count(n_orbs_full)} qubits  "
          f" E = {e_full:.6f} Ha")
    print(f"    Frozen core: {n_orbs_fc} orbitals → {qubit_count(n_orbs_fc)} qubits  "
          f" E = {e_fc:.6f} Ha")
    print(f"    Qubit saving: {qubit_count(n_orbs_full) - qubit_count(n_orbs_fc)} qubits")


# ── Task 3: Multi-molecule PES ────────────────────────────────────────────────

def task_molecules():
    print(f"\n{'─'*65}")
    print("  Task: Multi-Molecule PES (LiH & BeH₂)")
    print(f"{'─'*65}")

    lih_dists = np.arange(0.8, 4.0, 0.1)
    lih_energies = []
    print("\n  Computing LiH PES …")
    for d in lih_dists:
        geo = f"Li 0 0 0; H 0 0 {d:.2f}"
        e, _, _ = solve_exact(geo, "sto-3g", charge=0, spin=0, freeze_core=True)
        lih_energies.append(e)
        print(f"    d={d:.2f}  E={e:.6f} Ha")

    eq_lih = _find_eq(lih_dists, lih_energies)
    print(f"\n  LiH equilibrium: {eq_lih[0]:.4f} Å  (exp. ~1.595 Å)")

    beh2_dists = np.arange(0.8, 3.5, 0.1)
    beh2_energies = []
    print("\n  Computing BeH₂ PES (symmetric stretch) …")
    for d in beh2_dists:
        geo = f"Be 0 0 0; H 0 0 {d:.2f}; H 0 0 -{d:.2f}"
        e, _, _ = solve_exact(geo, "sto-3g", charge=0, spin=0, freeze_core=True)
        beh2_energies.append(e)
        print(f"    d={d:.2f}  E={e:.6f} Ha")

    eq_beh2 = _find_eq(beh2_dists, beh2_energies)
    print(f"\n  BeH₂ equilibrium: {eq_beh2[0]:.4f} Å  (exp. ~1.326 Å)")

    _plot_molecules(
        lih_dists, lih_energies, eq_lih,
        beh2_dists, beh2_energies, eq_beh2,
    )


def _find_eq(distances, energies):
    sp = UnivariateSpline(distances, energies, k=4, s=0)
    deriv = sp.derivative()
    roots = deriv.roots()
    if len(roots) == 0:
        idx = np.argmin(energies)
        return distances[idx], energies[idx]
    min_r = roots[np.argmin([sp(r) for r in roots])]
    return float(min_r), float(sp(min_r))


def _plot_molecules(lih_d, lih_e, eq_lih, beh2_d, beh2_e, eq_beh2):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    def plot_pes(ax, dists, energies, eq, title, color):
        sp = UnivariateSpline(dists, energies, k=4, s=0)
        df = np.linspace(dists[0], dists[-1], 500)
        ax.plot(df, sp(df), color=color, linewidth=2.2)
        ax.scatter(dists, energies, color=color, s=20, zorder=5)
        ax.axvline(eq[0], color="#F44336", linestyle="--", linewidth=1.5,
                   label=f"Eq. bond: {eq[0]:.4f} Å")
        ax.scatter([eq[0]], [eq[1]], color="#F44336", s=80, zorder=6)
        ax.set_xlabel("Interatomic Distance (Å)")
        ax.set_ylabel("Ground-State Energy (Ha)")
        ax.set_title(title)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    plot_pes(ax1, lih_d, lih_e, eq_lih, "LiH PES (sto-3g, frozen core)", "#9C27B0")
    plot_pes(ax2, beh2_d, beh2_e, eq_beh2, "BeH₂ PES — Symmetric Stretch (sto-3g, frozen core)", "#FF5722")

    fig.suptitle("Phase 3 — Multi-Molecule Potential Energy Surfaces", fontsize=13)
    fig.tight_layout()

    path = f"{RESULTS_DIR}/phase3_molecules.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"\n  Plot saved → {path}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 3 — Chemical Accuracy")
    parser.add_argument("--task",
                        choices=["basis", "active_space", "molecules", "all"],
                        default="all",
                        help="Which sub-task to run")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.task in ("basis", "all"):
        task_basis_comparison()

    if args.task in ("active_space", "all"):
        task_active_space()

    if args.task in ("molecules", "all"):
        task_molecules()


if __name__ == "__main__":
    main()
