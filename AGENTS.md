# AGENTS.md

Project notes for automation helpers.

- Working directory: `/Users/firecaster/3D-Firebrand-Characteristic-Extractor`
- Environment: Python 3.11.x (conda env `firebrand-extractor`)
- Output format: `File (ID), Volume (mm3), Surface Area (mm2), Length (mm), Width (mm), Height (mm), Mass (g)`

## Scripts Overview

- `compute.py`: Extracts mesh characteristics using axis-aligned bounding box (AABB). Accepts a directory path as argument or defaults to current directory. Outputs `mesh_volumes_and_bboxes.csv` in the target directory.
  - Usage: `python compute.py /path/to/ply_files`
  - Optional: `-o` or `--output` to specify custom CSV path
  
- `computer new backup.py`: Similar to `compute.py` but uses smallest oriented bounding box (OBB) for L/W/H instead of AABB; no mesh export.

- `characteristic extract.py`: Scans directories recursively and writes one CSV per folder named `<folder>.csv`; uses PCA-rotated mesh exports in a temp folder to compute smallest OBB lengths; errors are written into L/W/H cells; `--keep-temp` keeps the temp folder.

- `seperation v2.py`: Scans recursively; writes outputs in the same folder unless `--output-subdir` is set.

- `organize_ply_by_prefix.py`: Groups `<prefix>_mesh*.ply` into `<prefix>/` and removes redundant `_mesh_1` when no other clusters exist.

## Workflow Steps

1. Segment your mesh files (if needed): `python "seperation v2.py" "/path/to/raw_meshes"`
2. Extract characteristics using one of:
   - `python compute.py /path/to/segmented_files` (AABB - fastest)
   - `python "computer new backup.py" /path/to/segmented_files` (OBB)
   - `python "characteristic extract.py" /path/to/root` (PCA per-folder)
3. Results are saved in each directory as `mesh_volumes_and_bboxes.csv` or `<folder>.csv`

