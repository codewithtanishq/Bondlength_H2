"""
Project Configuration & Constants
==================================
Centralized settings for all phases of the quantum H₂ simulation.
"""

import numpy as np
from pathlib import Path

# ── Directories ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent
RESULTS_DIR = PROJECT_ROOT.parent / "results"
SRC_DIR = PROJECT_ROOT

# Create directories if they don't exist
RESULTS_DIR.mkdir(exist_ok=True)

# ── Random Seed & Reproducibility ──────────────────────────────────────────────

SEED = 42  # Fixed seed for reproducible results

# ── Simulation Parameters ────────────────────────────────────────────────────

# Distance scan range (Ångströms)
DISTANCE_MIN = 0.4
DISTANCE_MAX = 2.0
DISTANCE_STEP = 0.05  # Phase 0–2 (default scan density)
DISTANCE_STEP_COARSE = 0.1  # For expensive calculations

# Default basis set
BASIS_DEFAULT = "sto-3g"
BASIS_SETS = {
    "sto-3g": {"label": "STO-3G (minimal, lightweight)",
                "n_orbitals_h2": 2,
                "n_qubits_h2": 4},
    "6-31g": {"label": "6-31G (flexible)",
              "n_orbitals_h2": 4,
              "n_qubits_h2": 8},
    "cc-pvdz": {"label": "cc-pVDZ (high accuracy)",
                "n_orbitals_h2": 5,
                "n_qubits_h2": 10},
}

# ── Phase 0: Classical Baseline ─────────────────────────────────────────────

class Phase0Config:
    """Classical exact diagonalization (NumPyMinimumEigensolver)."""
    DISTANCES = None  # Computed from DISTANCE_MIN/MAX/STEP
    BASIS = BASIS_DEFAULT
    DESCRIPTION = "Exact classical diagonalization using NumPy"

# ── Phase 1: VQE ─────────────────────────────────────────────────────────────

class Phase1Config:
    """Variational Quantum Eigensolver with chemistry-inspired ansatze."""
    DISTANCES = None  # Computed from DISTANCE_MIN/MAX/STEP
    BASIS = BASIS_DEFAULT
    ANSATZ_OPTIONS = ["uccsd", "real_amplitudes"]
    DEFAULT_ANSATZ = "uccsd"
    MAX_ITERATIONS = 300
    OPTIMIZER = "COBYLA"
    DESCRIPTION = "VQE with UCCSD/RealAmplitudes ansatz"

# ── Phase 2: Noise & Mitigation ─────────────────────────────────────────────

class Phase2Config:
    """Quantum noise modeling and error mitigation techniques."""
    EQUILIBRIUM_DISTANCE = 0.735  # Å
    BASIS = BASIS_DEFAULT
    NOISE_MODEL = {
        "t1_us": 100.0,
        "t2_us": 80.0,
        "gate1_err": 1e-3,
        "gate2_err": 1e-2,
        "readout_err": 0.015,
    }
    ZNE_SCALE_FACTORS = (1, 2, 3)
    READOUT_ERROR_CORRECTION = True
    SHOTS = 4096
    MAX_ITERATIONS = 300
    DESCRIPTION = "Noise modeling with ZNE + readout mitigation"

# ── Phase 3: Chemistry & Accuracy ────────────────────────────────────────────

class Phase3Config:
    """Larger basis sets, active space reduction, multi-molecule systems."""
    TASKS = ["basis", "active_space", "molecules"]
    BASES_TO_SCAN = ["sto-3g", "6-31g", "cc-pvdz"]
    DISTANCES_H2 = None
    FREEZE_CORE = True
    MOLECULES = {
        "H2": {"geometry_template": "H 0 0 0; H 0 0 {:.2f}",
               "distances": np.arange(0.4, 2.0, 0.05)},
        "LiH": {"geometry_template": "Li 0 0 0; H 0 0 {:.2f}",
                "distances": np.arange(0.8, 4.0, 0.1)},
        "BeH2": {"geometry_template": "Be 0 0 0; H 0 0 {:.2f}; H 0 0 -{:.2f}",
                 "distances": np.arange(0.8, 3.5, 0.1)},
    }
    DESCRIPTION = "Basis sets, active space, larger molecules"

# ── Phase 4: Hardware Execution ──────────────────────────────────────────────

class Phase4Config:
    """IBM Quantum hardware execution and comparison."""
    EQUILIBRIUM_DISTANCE = 0.735
    BASIS = BASIS_DEFAULT
    SIMULATORS = ["simulator", "aer_simulator"]
    BACKENDS = [
        "ibm_brisbane",
        "ibm_kyoto",
        "ibm_osaka",
    ]
    SHOTS = 1024
    MAX_ITERATIONS = 300
    TIMEOUT_SECONDS = 3600
    DESCRIPTION = "Hardware execution on real quantum devices"

# ── Plotting & Visualization ──────────────────────────────────────────────

class PlottingConfig:
    """Matplotlib and visualization settings."""
    DPI = 150
    FIGURE_SIZE_SINGLE = (9, 5)
    FIGURE_SIZE_DOUBLE = (14, 5)
    COLORS = {
        "exact": "#607D8B",
        "vqe": "#4CAF50",
        "noisy": "#F44336",
        "mitigated": "#9C27B0",
        "hardware": "#FF5722",
    }
    FONT_SIZE = {
        "title": 13,
        "label": 12,
        "legend": 10,
        "tick": 9,
    }

CHEMICAL_ACCURACY_mHa = 1.6
EXPERIMENTAL_DATA = {
    "H2": {"bond_length_angstrom": 0.7414, "dissociation_energy_eV": 4.478},
    "LiH": {"bond_length_angstrom": 1.5949, "dissociation_energy_eV": 4.635},
    "BeH2": {"bond_length_angstrom": 1.3264, "dissociation_energy_eV": 2.35},
}

# ── Utility: Compute distance arrays ─────────────────────────────────────────────

def get_distance_array(step: float = DISTANCE_STEP) -> np.ndarray:
    """Return distance array from MIN to MAX with given step."""
    return np.arange(DISTANCE_MIN, DISTANCE_MAX + step / 2, step)

Phase0Config.DISTANCES = get_distance_array()
Phase1Config.DISTANCES = get_distance_array()
Phase3Config.DISTANCES_H2 = get_distance_array()
