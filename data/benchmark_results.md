# CB1 Receptor (6N4B Chain R) — Test Run Results

## System

| Property | Value |
|----------|-------|
| PDB | 6N4B chain R (CB1 receptor, residues MET109-MET411) |
| Force field | Amber14sb |
| Water | TIP3P |
| Box | Dodecahedron, 9.0 nm, 1.2 nm padding |
| System size | ~73,243 atoms |
| Ions | 67 Na+, 82 Cl- (0.15 M, neutralized) |
| Non-protein residues | ~23,000 water molecules |

## Performance (NVIDIA TITAN Xp, 12 GB)

| Phase | Steps | Wall time | Notes |
|-------|-------|-----------|-------|
| pdb2gmx | — | < 1 s | Amber14sb |
| editconf | — | < 1 s | dodecahedron, 1.2 nm |
| solvate | — | < 1 s | 23,004 waters |
| genion | — | 1 s | 67 Na+, 82 Cl- |
| EM | 5,000 | 13 s | steep, -pme cpu |
| NVT | 250,000 (500 ps) | ~9 min | V-rescale, 310 K |
| NPT | 500,000 (1 ns) | ~12 min | Berendsen, 1 bar |
| Production | 50,000 (100 ps) | ~1 min | Parrinello-Rahman |

GPU flags: `-nb gpu -pme gpu -bonded cpu -update gpu` (EM uses `-pme cpu`)

## How to reproduce

Using the full pipeline script:
```bash
conda activate gromacs_env
cd /home/jack/repos/gromacs_notebooks
# Pre-cleaned PDB: data/input.pdb (PDBFixer applied)
gmx pdb2gmx -f data/input.pdb -o prep/processed.gro -p prep/topol.top \
    -ignh -ff amber14sb -water tip3p
gmx editconf -f prep/processed.gro -o prep/box.gro -c -bt dodecahedron -d 1.2
gmx solvate -cp prep/box.gro -cs spc216.gro -o prep/solvated.gro -p prep/topol.top
echo "SOL" | gmx genion -s prep/ions.tpr -o prep/solvated_ions.gro \
    -p prep/topol.top -pname NA -nname CL -neutral -conc 0.15
gmx grompp -f data/templates/minim.mdp -c prep/solvated_ions.gro \
    -p prep/topol.top -o prep/em.tpr
gmx mdrun -v -deffnm prep/em -s prep/em.tpr -nb gpu -pme cpu
# Then follow 02_running.ipynb for NVT → NPT → production
```