# 3D-Firebrand-Characteristic-Extractor

Tools to segment firebrand meshes and extract geometric characteristics from .ply files.

## Project Structure

```
.
├── compute.py                   # Extract mesh characteristics (AABB) to CSV
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

Extract mesh characteristics from a directory of .ply files:
```bash
python compute.py /path/to/folder
```

Results are saved to `/path/to/folder/mesh_volumes_and_bboxes.csv`

## Usage

### Extract characteristics (AABB)
```bash
python compute.py /path/to/ply_files
```
Uses axis-aligned bounding box (AABB) for Length/Width/Height.

**Output location**: Creates `mesh_volumes_and_bboxes.csv` in the input directory

Optional arguments:
- `-o, --output`: Specify custom output CSV path
  ```bash
  python compute.py /path/to/ply_files -o /custom/path/results.csv
  ```
  Output will be saved to the specified path instead of the default location

### Extract characteristics (OBB, no mesh export)
```bash
python "computer new backup.py" /path/to/ply_files
```
Uses smallest oriented bounding box (OBB) instead of AABB.

### Folder-by-folder extraction with PCA
```bash
python "characteristic extract.py" /path/to/root
```
Scans recursively, writes one CSV per folder using PCA-rotated mesh to compute smallest OBB.

Keep temp PCA exports:
```bash
python "characteristic extract.py" /path/to/root --keep-temp
```

## Typical Workflow

### Step 1: Segment connected components
```bash
python "seperation v2.py" "/path/to/root"
```
Scans recursively and writes segmented outputs into the same folder as each source file.

### Step 2 (Optional): Organize outputs by prefix
```bash
python "organize_ply_by_prefix.py" "/path/to/root" --dry-run
python "organize_ply_by_prefix.py" "/path/to/root"
```
Moves `<prefix>_mesh*.ply` into a `<prefix>/` folder and removes redundant `*_mesh_1.ply` when no other clusters exist.

### Step 3: Extract characteristics
Use any of the extraction scripts:

**AABB (simplest, fastest)**
```bash
python compute.py /path/to/segmented_files
```

**OBB (oriented bounding box)**
```bash
python "computer new backup.py" /path/to/segmented_files
```

**Per-folder with PCA (most detailed)**
```bash
python "characteristic extract.py" /path/to/root
```

## Output Format

CSV file includes:
- File (ID)
- Volume (mm3) — using absolute value to avoid negative volumes from flipped normals
- Surface Area (mm2)
- Length, Width, Height (mm) — from bounding box (AABB or OBB depending on script)
- Mass (g) — manual input column

## Notes

- Volume is absolute (`abs(mesh.volume)`) to avoid negative values from flipped normals
- AABB (axis-aligned bounding box) is the default for Length/Width/Height in `compute.py`
- OBB (oriented bounding box) is available in `computer new backup.py` and `characteristic extract.py`
- If you want different thresholds or folder rules, update script arguments and re-run

