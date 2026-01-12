import argparse
import os
import re
import shutil
import tempfile

import numpy as np
import trimesh

def pca_bounding_box(mesh):
    points = np.array(mesh.vertices)
    mean = points.mean(axis=0)
    centered = points - mean
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    rotation = Vt.T
    rotated = centered @ rotation
    min_bounds = rotated.min(axis=0)
    max_bounds = rotated.max(axis=0)
    extents = max_bounds - min_bounds
    return extents, rotation, mean

SEGMENTED_RE = re.compile(r".*_mesh_\d+\.ply$", re.IGNORECASE)
BASE_RE = re.compile(r".*_mesh\.ply$", re.IGNORECASE)


def select_ply_files(filenames):
    segmented = sorted([f for f in filenames if SEGMENTED_RE.match(f)])
    if segmented:
        return segmented

    base = sorted([f for f in filenames if BASE_RE.match(f)])
    if base:
        return base

    return sorted(filenames)


def process_directory(dirpath, keep_temp):
    filenames = [
        f for f in os.listdir(dirpath)
        if f.lower().endswith(".ply") and os.path.isfile(os.path.join(dirpath, f))
    ]
    if not filenames:
        return 0

    selected_files = select_ply_files(filenames)
    if not selected_files:
        return 0

    folder_name = os.path.basename(os.path.abspath(dirpath))
    output_csv = os.path.join(dirpath, f"{folder_name}.csv")

    import csv
    temp_dir = tempfile.mkdtemp(prefix="pca_tmp_", dir=dirpath)
    try:
        with open(output_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "File (ID)", "Volume (mm3)", "Surface Area (mm2)",
                "Length (mm)", "Width (mm)", "Height (mm)", "Mass (g)",
            ])

            for filename in selected_files:
                mesh = trimesh.load_mesh(os.path.join(dirpath, filename))
                volume = abs(mesh.volume)
                surface_area = mesh.area

                # PCA OBB via exported rotated mesh (temp files are cleared after CSV is done)
                obb = None
                error_message = ""
                try:
                    pca_extents, rotation, mean = pca_bounding_box(mesh)
                    transformed_vertices = (np.array(mesh.vertices) - mean) @ rotation
                    mesh_pca = mesh.copy()
                    mesh_pca.vertices = transformed_vertices
                    fd, temp_path = tempfile.mkstemp(
                        prefix=f"{os.path.splitext(filename)[0]}_pca_",
                        suffix=".ply",
                        dir=temp_dir,
                    )
                    os.close(fd)
                    mesh_pca.export(temp_path)
                    obb = mesh_pca.bounding_box.extents
                except Exception as exc:
                    obb = [np.nan, np.nan, np.nan]
                    error_message = f"PCA export failed: {exc}"
                if obb is None:
                    obb = [np.nan, np.nan, np.nan]
                    error_message = "PCA export failed: unknown error"

                if error_message:
                    length_val = error_message
                    width_val = error_message
                    height_val = error_message
                else:
                    length_val = f"{obb[0]:.3f}"
                    width_val = f"{obb[1]:.3f}"
                    height_val = f"{obb[2]:.3f}"

                writer.writerow([
                    filename, f"{volume:.3f}", f"{surface_area:.3f}",
                    length_val, width_val, height_val, "",
                ])

                status = f"Processed {os.path.join(dirpath, filename)} | Smallest OBB: {np.round(obb,3)}"
                if error_message:
                    status += f" | ERROR: {error_message}"
                print(status)
    finally:
        if keep_temp:
            print(f"Temp folder kept: {temp_dir}")
        else:
            shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"Results saved to {output_csv}")
    return len(selected_files)


def process_tree(root_dir, keep_temp):
    total_dirs = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not any(f.lower().endswith(".ply") for f in filenames):
            continue
        count = process_directory(dirpath, keep_temp)
        if count:
            total_dirs += 1
            total_files += count
    print(f"Processed {total_files} files across {total_dirs} folders.")


def main():
    parser = argparse.ArgumentParser(
        description="Extract mesh characteristics for all .ply files under a directory tree."
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=os.getcwd(),
        help="Root directory to scan (default: current working directory).",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary PCA export folders for inspection.",
    )
    args = parser.parse_args()
    process_tree(args.root_dir, args.keep_temp)


if __name__ == "__main__":
    main()
