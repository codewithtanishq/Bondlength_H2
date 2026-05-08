#!/usr/bin/env python3
"""
Quick-Start Demo: Run all phases sequentially (with shorter iterations for speed)

This script demonstrates the complete quantum H₂ simulation pipeline:
  1. Phase 0 (Baseline) — exact diagonalization (fast)
  2. Phase 1 (VQE) — variational quantum solver
  3. Phase 2 (Noise) — error simulation & mitigation
  4. Phase 3 (Chemistry) — basis sets & larger molecules
  5. Phase 4 (Hardware) — local simulator execution

Usage:
    python demo.py                    # Run all phases
    python demo.py --phase 0          # Run only Phase 0
    python demo.py --skip_phase 2     # Run all except Phase 2 (slow)
"""

import argparse
import subprocess
import sys
import os


def run_phase(phase_num: int, phase_script: str, args: list = None):
    if args is None:
        args = []

    print(f"\n{'='*70}")
    print(f"  PHASE {phase_num}: {phase_script}")
    print(f"{'='*70}")

    cmd = [sys.executable, f"src/{phase_script}"] + args
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✓ Phase {phase_num} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Phase {phase_num} failed with error code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Quick-start demo: run quantum H₂ simulation phases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo.py                  # Run all phases (full pipeline)
  python demo.py --phase 1        # Run only Phase 1 (VQE)
  python demo.py --skip_phase 2   # Skip Phase 2 (slow)
  python demo.py --short          # Fast mode (fewer iterations)
        """,
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[0, 1, 2, 3, 4],
        default=None,
        help="Run only a specific phase",
    )
    parser.add_argument(
        "--skip_phase",
        type=int,
        choices=[0, 1, 2, 3, 4],
        default=None,
        help="Skip a specific phase",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help="Fast mode: fewer iterations, coarser grids",
    )
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)

    phases = {
        0: ("phase0_baseline.py", []),
        1: ("phase1_vqe.py", ["--ansatz", "uccsd", "--max_iter",
                              "200" if args.short else "300"]),
        2: ("phase2_noise.py", ["--distance", "0.735",
                                "--skip_zne"] if args.short else ["--distance", "0.735"]),
        3: ("phase3_chemistry.py", ["--task", "all"]),
        4: ("phase4_hardware.py", ["--backend", "simulator"]),
    }

    if args.phase is not None:
        phases_to_run = [args.phase]
    else:
        phases_to_run = [i for i in range(5) if i != args.skip_phase]

    print(f"\n{'='*70}")
    print(f"  Quantum H₂ Simulation — Quick-Start Demo")
    print(f"{'='*70}")
    print(f"  Phases to run: {phases_to_run}")
    print(f"  Mode: {'FAST (fewer iterations)' if args.short else 'FULL'}")
    print(f"{'='*70}")

    success_count = 0
    for phase_idx in phases_to_run:
        script, script_args = phases[phase_idx]
        if run_phase(phase_idx, script, script_args):
            success_count += 1

    print(f"\n{'='*70}")
    print(f"  Demo Summary")
    print(f"{'='*70}")
    print(f"  Completed: {success_count}/{len(phases_to_run)} phases ✓")
    print(f"  Output: Results saved to results/ directory")
    print(f"{'='*70}\n")

    if success_count == len(phases_to_run):
        print("✓ All phases completed successfully!")
        print("\nNext steps:")
        print("  1. Check results/ directory for plots and data")
        print("  2. Review Phase 1 VQE energy convergence")
        print("  3. Examine Phase 2 noise mitigation effectiveness")
        print("  4. Explore basis set convergence in Phase 3")
        return 0
    else:
        print("✗ Some phases failed. Check error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
