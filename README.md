# 3D-Firebrand-Characteristic-Extractor

Tools to segment firebrand meshes and extract geometric characteristics from .ply files.

## Requirements
- Python 3.11.x (recommended), opend3d doesn't run with newer Python
- Packages: `open3d`, `trimesh`, `numpy`, plus plotting/tools as needed

If you use conda, this repo includes `environment.yml`.

## Setup (conda)
```bash
conda env create -f environment.yml
conda activate firebrand-extractor
```

## Typical workflow
1) Segment connected components from each .ply:
```bash
python "seperation v2.py" "/path/to/root"
```
This scans recursively and writes segmented outputs into the same folder as each source file.

2) (Optional) Organize outputs into prefix folders:
```bash
python "organize_ply_by_prefix.py" "/path/to/root" --dry-run
python "organize_ply_by_prefix.py" "/path/to/root"
```
This moves `<prefix>_mesh*.ply` into a `<prefix>/` folder and removes redundant
`*_mesh_1.ply` when no other clusters exist.

3) Extract CSV characteristics:
```bash
python "compute.py"
```
Outputs `mesh_volumes_and_bboxes.csv` with:
`File (ID), Volume (mm3), Surface Area (mm2), Length (mm), Width (mm), Height (mm), Mass (g)`
using axis-aligned bounding box (AABB) dimensions and absolute volume.

Alternative smallest-OBB CSV (no mesh export):
```bash
python "computer new backup.py"
```
This uses the smallest oriented bounding box for Length/Width/Height and writes the same CSV format.

Folder-by-folder CSV with PCA export (temp files):
```bash
python "characteristic extract.py" "/path/to/root"
```
This scans subfolders, writes one CSV per folder named after the folder (e.g., `0609_10.csv`),
uses a PCA-rotated mesh to compute smallest OBB lengths, and deletes temp files after the CSV.

Keep the temp PCA exports for inspection:
```bash
python "characteristic extract.py" "/path/to/root" --keep-temp
```

## Notes
- Volume is absolute (`abs(mesh.volume)`) to avoid negative values from flipped normals.
- If you want different thresholds or folder rules, update script arguments and re-run.
