# AGENTS.md

Project notes for automation helpers.

- Working directory: `/Users/firecaster/3D-Firebrand-Characteristic-Extractor`
- Environment: Python 3.11.x (conda env `firebrand-extractor`)
- **Input folder**: `segmented_mesh_objects/` — place your segmented `.ply` files here
- **Output**: `mesh_volumes_and_bboxes.csv`
- CSV output format: `File (ID), Volume (mm3), Surface Area (mm2), Length (mm), Width (mm), Height (mm), Mass (g)`

## Scripts Overview

- `compute.py`: Reads `.ply` files from `segmented_mesh_objects/`, computes volume (using `abs(mesh.volume)` for absolute values), surface area, and bounding box dimensions. Outputs single CSV file.
  
- `computer new backup.py`: Similar to `compute.py` but uses smallest oriented bounding box (OBB) for L/W/H instead of axis-aligned bounding box (AABB); no mesh export.

- `characteristic extract.py`: Scans recursively and writes one CSV per folder named `<folder>.csv`; uses PCA-rotated mesh exports in a temp folder to compute smallest OBB lengths; errors are written into L/W/H cells; `--keep-temp` keeps the temp folder.

- `seperation v2.py`: Scans recursively; writes outputs in the same folder unless `--output-subdir` is set.

- `organize_ply_by_prefix.py`: Groups `<prefix>_mesh*.ply` into `<prefix>/` and removes redundant `_mesh_1` when no other clusters exist.

## Workflow Steps

1. Place your segmented mesh files (`.ply` format) into the `segmented_mesh_objects/` folder
2. Run `python compute.py` to extract characteristics
3. Results are written to `mesh_volumes_and_bboxes.csv`
