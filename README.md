# GROMACS MD Simulation Notebooks

A complete workflow for setting up, running, monitoring, and analyzing
molecular dynamics simulations with GROMACS 2026.3.

## Prerequisites

```bash
conda activate gromacs_env
```

- **GROMACS 2026.3** — GPU-accelerated (CUDA, compiled for sm_61+)
- **MDAnalysis 2.10** — Python trajectory analysis
- **MDTraj** — Additional trajectory I/O
- **Jupyter** — Notebook interface

## GPU Hardware

NVIDIA TITAN Xp (Pascal, CC 6.1, 12 GB VRAM)

## Notebooks

| # | Notebook | Purpose |
|---|----------|---------|
| 1 | `01_preparation.ipynb` | System preparation from PDB — solvation, force field, energy minimization |
| 2 | `02_running.ipynb` | NVT equilibration → NPT equilibration → production MD |
| 3 | `03_monitoring.ipynb` | Real-time monitoring via EDR extraction, RMSD, Rg |
| 4 | `04_analysis.ipynb` | RMSD/RMSF, DSSP, contact maps, H-bonds, PCA, free energy landscape |

## Workflow

```
PDB structure
    ↓ 01_preparation.ipynb
Minimized system (em.gro + topol.top)
    ↓ 02_running.ipynb
Equilibration (NVT → NPT)
    ↓
Production trajectory (prod.xtc)
    ↓                        ↕
03_monitoring.ipynb       04_analysis.ipynb
```

## Usage

Each notebook has a configuration cell at the top — edit paths and parameters,
then run cells sequentially. For membrane proteins, set `MEMBRANE_SIMULATION = True`
(01_preparation.ipynb) and use CHARMM-GUI Membrane Builder outputs.

## Force fields

GROMACS 2026.3 conda-forge includes: amber14sb (default), amber99sb-ildn, charmm27.
CHARMM36m requires manual installation. Set `FORCE_FIELD = "amber14sb"` for soluble proteins.

## Reference scripts

`data/templates/` contains standalone MDP files for:
- `minim.mdp` — energy minimization (steepest descent)
- `nvt.mdp` — NVT equilibration (V-rescale, 310 K)
- `prod.mdp` — production MD (Parrinello-Rahman, default 100 ns)

## Test data and benchmark

`data/` contains a test system (CB1 receptor, PDB 6N4B chain R, 276 residues).
See `data/benchmark_results.md` for performance numbers on TITAN Xp.

Input PDB: `data/input.pdb` — cleaned with PDBFixer, ready for pdb2gmx.
Example run output: `data/my_protein_prep/` (minimized) and `data/my_protein_md/` (100 ps production).
Analysis output: `data/my_protein_analysis/plots/`.