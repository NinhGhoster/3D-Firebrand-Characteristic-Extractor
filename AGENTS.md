# AGENTS.md

Project notes for automation helpers.

- Working directory: /Users/firecaster/3D-Firebrand-Characteristic-Extractor
- Environment: Python 3.11.x (conda env `firebrand-extractor`).
- CSV output format: `File (ID), Volume (mm3), Surface Area (mm2), Length (mm), Width (mm), Height (mm), Mass (g)`.
- `compute.py`: uses `abs(mesh.volume)`; header units are `mm3`/`mm2`.
- `computer new backup.py`: uses smallest oriented bounding box for L/W/H; no mesh export.
- `characteristic extract.py`: scans recursively and writes one CSV per folder named `<folder>.csv`; uses PCA-rotated mesh exports in a temp folder to compute smallest OBB lengths; errors are written into L/W/H cells; `--keep-temp` keeps the temp folder.
- `seperation v2.py`: scans recursively; writes outputs in the same folder unless `--output-subdir` is set.
- `organize_ply_by_prefix.py`: groups `<prefix>_mesh*.ply` into `<prefix>/` and removes redundant `_mesh_1` when no other clusters exist.
