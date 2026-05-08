"""
Phase 4 — Hardware Execution & IBM Quantum Integration
========================================================
Runs the H₂ VQE pipeline on a local simulator or an IBM Quantum backend.
Supports backend enumeration and local/hardware comparison.

Usage:
    python src/phase4_hardware.py --backend simulator --max_iter 300
    python src/phase4_hardware.py --list_backends
"""

import argparse
import os
import sys
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
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals

from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator as IBMEstimator

RESULTS_DIR = "results"
SEED = 42
algorithm_globals.random_seed = SEED


def build_problem(distance: float, basis: str = "sto-3g"):
    geometry = f"H 0 0 0; H 0 0 {distance:.3f}"
    driver = PySCFDriver(
        atom=geometry,
        basis=basis,
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    return driver.run()


def build_vqe(problem, ansatz_name="uccsd", max_iter=300):
    mapper = JordanWignerMapper()
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
    estimator = Estimator()
    vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=COBYLA(maxiter=max_iter))
    return GroundStateEigensolver(mapper, vqe)


def list_ibm_backends():
    try:
        service = QiskitRuntimeService()  # uses saved IBM Quantum credentials
    except Exception as exc:
        print("IBM Quantum credentials not configured:", exc)
        sys.exit(1)

    backends = [b.name for b in service.backends()]
    print("Available IBM Quantum backends:")
    for name in backends:
        print(f"  - {name}")
    return backends


def run_local_simulator(distance, ansatz, max_iter):
    problem = build_problem(distance)
    solver = build_vqe(problem, ansatz_name=ansatz, max_iter=max_iter)
    result = solver.solve(problem)
    return result.total_energies[0].real


def run_ibm_backend(distance, backend_name, ansatz, max_iter, shots=1024):
    try:
        service = QiskitRuntimeService()
    except Exception as exc:
        raise RuntimeError("IBM Quantum credentials are not configured") from exc

    problem = build_problem(distance)
    mapper = JordanWignerMapper()
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

    with Session(service=service, backend=backend_name) as session:
        estimator = IBMEstimator(session=session, options={"shots": shots})
        vqe = VQE(estimator=estimator, ansatz=ansatz,
                  optimizer=COBYLA(maxiter=max_iter))
        solver = GroundStateEigensolver(mapper, vqe)
        result = solver.solve(problem)
    return result.total_energies[0].real


def find_equilibrium(distances, energies):
    spline = UnivariateSpline(distances, energies, k=4, s=0)
    roots = spline.derivative().roots()
    min_r = roots[np.argmin([spline(r) for r in roots])]
    return float(min_r), float(spline(min_r))


def plot_comparison(distance, local_energy, hardware_energy, exact_energy):
    labels = ["Exact", "Local Simulator", "IBM Hardware"]
    values = [exact_energy, local_energy, hardware_energy]
    errors = [(v - exact_energy) * 1000 for v in values]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.bar(labels, values, color=["#607D8B", "#4CAF50", "#FF5722"])
    ax1.set_ylabel("Energy (Ha)")
    ax1.set_title(f"H₂ Energy Comparison at {distance:.3f} Å")

    ax2.bar(labels, errors, color=["#607D8B", "#4CAF50", "#FF5722"])
    ax2.axhline(0, color="gray", linewidth=0.8)
    ax2.set_ylabel("ΔE vs Exact (mHa)")
    ax2.set_title("Hardware vs Local Simulation Error")

    fig.tight_layout()
    path = f"{RESULTS_DIR}/phase4_hardware_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"\n  Plot saved → {path}")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Phase 4 — Hardware Execution")
    parser.add_argument("--list_backends", action="store_true",
                        help="List available IBM Quantum backends")
    parser.add_argument("--backend", type=str, default="simulator",
                        help="Backend to run: simulator or IBM backend name")
    parser.add_argument("--distance", type=float, default=0.735,
                        help="Interatomic distance (Å)")
    parser.add_argument("--ansatz", choices=["uccsd", "real_amplitudes"],
                        default="uccsd", help="VQE ansatz type")
    parser.add_argument("--shots", type=int, default=1024,
                        help="Number of shots for hardware execution")
    parser.add_argument("--max_iter", type=int, default=300,
                        help="Max optimizer iterations")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.list_backends:
        list_ibm_backends()
        return

    print(f"\n{'─'*60}")
    print(f"  Phase 4 — Hardware Execution  |  backend: {args.backend}")
    print(f"{'─'*60}")

    problem = build_problem(args.distance)
    mapper = JordanWignerMapper()
    exact_solver = GroundStateEigensolver(mapper, NumPyMinimumEigensolver())
    exact_energy = exact_solver.solve(problem).total_energies[0].real

    local_energy = run_local_simulator(args.distance, args.ansatz, args.max_iter)
    print(f"  Local simulator energy: {local_energy:.6f} Ha")

    hardware_energy = None
    if args.backend != "simulator":
        try:
            hardware_energy = run_ibm_backend(args.distance, args.backend,
                                             args.ansatz, args.max_iter, shots=args.shots)
            print(f"  IBM backend energy:   {hardware_energy:.6f} Ha")
        except Exception as exc:
            print(f"Failed to run on IBM backend: {exc}")
            hardware_energy = float('nan')

    if hardware_energy is None:
        hardware_energy = local_energy

    plot_comparison(args.distance, local_energy, hardware_energy, exact_energy)


if __name__ == "__main__":
    main()
