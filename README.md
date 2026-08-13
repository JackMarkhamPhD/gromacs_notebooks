# GROMACS MD Simulation Notebooks

A complete workflow for setting up, running, monitoring, and analyzing
molecular dynamics simulations with GROMACS 2026.3.

## Prerequisites

```bash
conda activate gromacs_env
```

- **GROMACS 2026.3** — GPU-accelerated (CUDA, compiled for sm_61+)
- **MDAnalysis** — Python trajectory analysis
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
(preparation notebook) and use CHARMM-GUI Membrane Builder outputs.

## Reference scripts

`data/templates/` contains standalone MDP files for:
- `minim.mdp` — energy minimization
- `nvt.mdp` — NVT equilibration
- `prod.mdp` — production MD (default 100 ns)