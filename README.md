# 3D-Firebrand-Characteristic-Extractor

Tools to segment firebrand meshes and extract geometric characteristics from .ply files.

## Project Structure

```
.
├── segmented_mesh_objects/      # Input folder: place your segmented .ply files here
├── compute.py                   # Main script: extracts mesh characteristics to CSV
├── computer new backup.py       # Alternative: uses oriented bounding box (OBB)
├── characteristic extract.py    # Advanced: per-folder CSV output with PCA rotation
├── seperation v2.py             # Utility: segments connected components
├── organize_ply_by_prefix.py    # Utility: organizes outputs by prefix
├── README.md                    # This file
├── AGENTS.md                    # Detailed script documentation
└── environment.yml              # Conda environment configuration
```

## Requirements

- Python 3.11.x (recommended), open3d doesn't run with newer Python
- Packages: `open3d`, `trimesh`, `numpy`, plus plotting/tools as needed

If you use conda, this repo includes `environment.yml`.

## Setup (conda)

```bash
conda env create -f environment.yml
conda activate firebrand-extractor
```

## Quick Start

1. **Place your segmented mesh files** in the `segmented_mesh_objects/` folder
2. **Run the extraction script**:
   ```bash
   python compute.py
   ```
3. **Check results** in `mesh_volumes_and_bboxes.csv`

The CSV output includes:
- File (ID)
- Volume (mm3) — using absolute value to avoid negative volumes from flipped normals
- Surface Area (mm2)
- Length, Width, Height (mm) — from axis-aligned bounding box (AABB)
- Mass (g) — manual input column

## Typical Workflow

### Step 1: Segment connected components
```bash
python "seperation v2.py" "/path/to/root"
```
This scans recursively and writes segmented outputs into the same folder as each source file.

### Step 2 (Optional): Organize outputs by prefix
```bash
python "organize_ply_by_prefix.py" "/path/to/root" --dry-run
python "organize_ply_by_prefix.py" "/path/to/root"
```
This moves `<prefix>_mesh*.ply` into a `<prefix>/` folder and removes redundant `*_mesh_1.ply` when no other clusters exist.

### Step 3: Extract characteristics
Place your segmented `.ply` files in `segmented_mesh_objects/`, then:
```bash
python compute.py
```
Outputs `mesh_volumes_and_bboxes.csv` with axis-aligned bounding box dimensions and absolute volume.

### Alternative: Smallest OBB (no mesh export)
```bash
python "computer new backup.py"
```
Uses the smallest oriented bounding box for Length/Width/Height instead of AABB.

### Advanced: Folder-by-folder CSV with PCA export
```bash
python "characteristic extract.py" "/path/to/root"
```
This scans all subfolders under the root, writes one CSV per folder (named after the folder), uses a PCA-rotated mesh to compute smallest OBB lengths, and deletes temp files after the CSV.

Keep the temp PCA exports for inspection:
```bash
python "characteristic extract.py" "/path/to/root" --keep-temp
```

CLI options:
- `root_dir`: root folder to scan recursively (defaults to the current working directory)
- `--keep-temp`: keep the per-folder PCA temp exports for inspection

## Notes

- Volume is absolute (`abs(mesh.volume)`) to avoid negative values from flipped normals
- AABB (axis-aligned bounding box) is the default for Length/Width/Height in `compute.py`
- OBB (oriented bounding box) is available in `computer new backup.py` and `characteristic extract.py`
- If you want different thresholds or folder rules, update script arguments and re-run
