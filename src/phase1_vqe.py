"""
Phase 1 — VQE with Chemistry-Inspired Ansatz (UCCSD / RealAmplitudes)
=======================================================================
Replaces the exact classical solver with the Variational Quantum
Eigensolver (VQE) — a hybrid quantum-classical algorithm suited for
NISQ devices. Supports two ansatz choices:
  • UCCSD  : chemistry-inspired, more accurate, higher gate depth
  • RealAmplitudes : hardware-efficient, lower depth, less expressive

The VQE loop uses COBYLA (gradient-free) to optimize circuit parameters
until the expectation value of the Hamiltonian converges.

Usage:
    python src/phase1_vqe.py [--ansatz uccsd|real_amplitudes] [--max_iter 1024]
"""

import argparse
import os
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

from qiskit_algorithms import VQE, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_algorithms.utils import algorithm_globals

from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator


# ── Configuration ─────────────────────────────────────────────────────────────

DISTANCES = np.arange(0.4, 2.0, 0.05)
BASIS_SET = "sto-3g"
RESULTS_DIR = "results"
SEED = 42

algorithm_globals.random_seed = SEED


# ── Driver / problem builder ──────────────────────────────────────────────────

def build_problem(distance: float, basis: str = BASIS_SET):
    geometry = f"H 0 0 0; H 0 0 {distance:.3f}"
    driver = PySCFDriver(
        atom=geometry,
        basis=basis,
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    return driver.run()


# ── VQE solver factory ────────────────────────────────────────────────────────

def make_vqe_solver(problem, ansatz_name: str = "uccsd", max_iter: int = 500):
    """Return a configured VQE-based GroundStateEigensolver."""
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(problem.hamiltonian.second_q_op())
    n_qubits = qubit_op.num_qubits

    if ansatz_name == "uccsd":
        particle_number = problem.num_particles
        num_spatial_orbitals = problem.num_spatial_orbitals

        hf_state = HartreeFock(
            num_spatial_orbitals=num_spatial_orbitals,
            num_particles=particle_number,
            qubit_mapper=mapper,
        )
        ansatz = UCCSD(
            num_spatial_orbitals=num_spatial_orbitals,
            num_particles=particle_number,
            qubit_mapper=mapper,
            initial_state=hf_state,
        )
        optimizer = COBYLA(maxiter=max_iter)

    elif ansatz_name == "real_amplitudes":
        ansatz = RealAmplitudes(n_qubits, reps=2)
        optimizer = SPSA(maxiter=max_iter)

    else:
        raise ValueError(f"Unknown ansatz: {ansatz_name!r}")

    estimator = Estimator()
    vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)

    return GroundStateEigensolver(mapper, vqe)


# ── PES scan ─────────────────────────────────────────────────────────────────

def compute_pes_vqe(distances, ansatz_name="uccsd", max_iter=300):
    energies = []

    print(f"\n{'─'*62}")
    print(f"  Phase 1 — VQE PES Scan  |  ansatz: {ansatz_name}")
    print(f"{'─'*62}")
    print(f"  {'Distance (Å)':>14}  {'VQE Energy (Ha)':>17}  {'Time (s)':>9}")
    print(f"  {'─'*14}  {'─'*17}  {'─'*9}")

    for d in distances:
        t0 = time.time()
        problem = build_problem(d)
        solver = make_vqe_solver(problem, ansatz_name=ansatz_name, max_iter=max_iter)
        result = solver.solve(problem)
        energy = result.total_energies[0].real
        elapsed = time.time() - t0

        energies.append(energy)
        print(f"  {d:>14.3f}  {energy:>17.6f}  {elapsed:>9.2f}")

    return energies


# ── Reference (exact) for comparison ─────────────────────────────────────────

def compute_pes_exact(distances):
    mapper = JordanWignerMapper()
    solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
    energies = []
    for d in distances:
        problem = build_problem(d)
        result = solver.solve(problem)
        energies.append(result.total_energies[0].real)
    return energies


# ── Equilibrium extraction ───────────────────────────────────────────────────

def find_equilibrium(distances, energies):
    spline = UnivariateSpline(distances, energies, k=4, s=0)
    deriv = spline.derivative()
    roots = deriv.roots()
    min_r = roots[np.argmin([spline(r) for r in roots])]
    return float(min_r), float(spline(min_r))


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_comparison(distances, vqe_energies, exact_energies, eq_vqe, ansatz_name):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    def smooth(d, e):
        sp = UnivariateSpline(d, e, k=4, s=0)
        df = np.linspace(d[0], d[-1], 500)
        return df, sp(df)

    d_fine, e_exact_fine = smooth(distances, exact_energies)
    _, e_vqe_fine = smooth(distances, vqe_energies)

    ax1.plot(d_fine, e_exact_fine, color="#607D8B", linewidth=1.5,
             linestyle="--", label="Exact (NumPy)")
    ax1.plot(d_fine, e_vqe_fine, color="#4CAF50", linewidth=2.0,
             label=f"VQE ({ansatz_name})")
    ax1.scatter(distances, vqe_energies, color="#4CAF50", s=25, zorder=5)
    ax1.axvline(eq_vqe[0], color="#F44336", linestyle=":", linewidth=1.5,
                label=f"Bond length: {eq_vqe[0]:.4f} Å")
    ax1.set_xlabel("Interatomic Distance (Å)")
    ax1.set_ylabel("Ground-State Energy (Ha)")
    ax1.set_title("H₂ PES: VQE vs Exact")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    errors = np.array(vqe_energies) - np.array(exact_energies)
    ax2.plot(distances, errors * 1000, color="#FF5722", linewidth=2.0)
    ax2.axhline(0, color="gray", linewidth=0.8)
    ax2.set_xlabel("Interatomic Distance (Å)")
    ax2.set_ylabel("ΔE  (VQE − Exact)  [mHa]")
    ax2.set_title("VQE Energy Error vs Exact Baseline")
    ax2.grid(True, alpha=0.3)

    fig.suptitle(f"Phase 1 — VQE Results  |  ansatz: {ansatz_name}", fontsize=13, y=1.01)
    fig.tight_layout()

    path = f"{RESULTS_DIR}/phase1_vqe_{ansatz_name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"\n  Plot saved → {path}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 1 — VQE H₂ PES")
    parser.add_argument("--ansatz", choices=["uccsd", "real_amplitudes"],
                        default="uccsd", help="Ansatz circuit type")
    parser.add_argument("--max_iter", type=int, default=300,
                        help="Max optimizer iterations per distance point")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("  Computing VQE energies …")
    vqe_energies = compute_pes_vqe(DISTANCES, ansatz_name=args.ansatz,
                                   max_iter=args.max_iter)

    print("\n  Computing exact reference …")
    exact_energies = compute_pes_exact(DISTANCES)

    eq_vqe = find_equilibrium(DISTANCES, vqe_energies)
    eq_exact = find_equilibrium(DISTANCES, exact_energies)

    print(f"\n{'═'*62}")
    print(f"  VQE bond length    : {eq_vqe[0]:.4f} Å   "
          f"  energy: {eq_vqe[1]:.6f} Ha")
    print(f"  Exact bond length  : {eq_exact[0]:.4f} Å   "
          f"  energy: {eq_exact[1]:.6f} Ha")
    print(f"  Experimental ref.  : ~0.7400 Å")
    print(f"  VQE vs exact ΔE    : "
          f"{(eq_vqe[1]-eq_exact[1])*1000:.2f} mHa  "
          f"(chemical accuracy ≤ 1.6 mHa)")
    print(f"{'═'*62}\n")

    plot_comparison(DISTANCES, vqe_energies, exact_energies, eq_vqe, args.ansatz)

    csv_path = f"{RESULTS_DIR}/phase1_vqe_{args.ansatz}.csv"
    data = np.column_stack([DISTANCES, vqe_energies, exact_energies,
                            np.array(vqe_energies) - np.array(exact_energies)])
    np.savetxt(csv_path, data, delimiter=",",
               header="distance_angstrom,vqe_energy_ha,exact_energy_ha,delta_ha",
               comments="")
    print(f"  Data saved  → {csv_path}\n")


if __name__ == "__main__":
    main()
