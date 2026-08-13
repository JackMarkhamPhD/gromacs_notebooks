#!/usr/bin/env python3
"""
convert_ipynb.py — Convert Jupyter notebook .py scripts to .ipynb
Usage: python convert_ipynb.py script.py notebook.ipynb
"""
import json, sys, re

def py_to_ipynb(py_path, ipynb_path):
    with open(py_path) as f:
        text = f.read()
    
    # Split into cells on markdown/heading markers
    cells = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('# %% [markdown]') or lines[i].startswith('# %%'):
            # Read content until next cell marker
            cell_lines = []
            cell_type = 'code'
            if 'markdown' in lines[i]:
                cell_type = 'markdown'
            i += 1
            while i < len(lines) and not lines[i].startswith('# %%'):
                if cell_type == 'code' and lines[i].strip().startswith('# '):
                    cell_lines.append(lines[i][2:])
                else:
                    cell_lines.append(lines[i])
                i += 1
            # Strip trailing empty lines
            while cell_lines and cell_lines[-1].strip() == '':
                cell_lines.pop()
            source = '\n'.join(cell_lines) + '\n' if cell_lines else ''
            if cell_type == 'markdown':
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [source]
                })
            else:
                cells.append({
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [source]
                })
        else:
            i += 1
    
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (gromacs_env)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0"
            }
        },
        "cells": cells
    }
    
    with open(ipynb_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    print(f'Wrote {len(cells)} cells to {ipynb_path}')

if __name__ == '__main__':
    py_to_ipynb(sys.argv[1], sys.argv[2])