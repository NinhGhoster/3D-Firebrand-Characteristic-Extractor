"""
Organize PLY files into prefix folders based on "<prefix>_mesh" naming.
"""
import argparse
import os
import shutil


def extract_prefix(filename):
    stem, _ = os.path.splitext(filename)
    marker = "_mesh"
    if marker not in stem:
        return None
    prefix = stem.split(marker, 1)[0]
    return prefix or None


def collect_ply_paths(root_dir, recursive):
    paths = []
    if recursive:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith(".ply"):
                    paths.append(os.path.join(dirpath, filename))
    else:
        for filename in os.listdir(root_dir):
            if filename.lower().endswith(".ply"):
                paths.append(os.path.join(root_dir, filename))
    return paths


def is_redundant_mesh_1(filename, filenames):
    stem, ext = os.path.splitext(filename)
    if not stem.endswith("_mesh_1"):
        return False

    base_stem = stem[:-2]  # drop trailing "_1"
    base_file = base_stem + ext
    if base_file not in filenames:
        return False

    cluster_prefix = base_stem + "_"
    for candidate in filenames:
        if candidate in (filename, base_file):
            continue
        cand_stem, cand_ext = os.path.splitext(candidate)
        if cand_ext.lower() != ext.lower():
            continue
        if not cand_stem.startswith(cluster_prefix):
            continue
        suffix = cand_stem[len(cluster_prefix):]
        if suffix.isdigit() and suffix != "1":
            return False

    return True


def find_redundant_mesh_1(ply_paths):
    dir_to_files = {}
    for ply_path in ply_paths:
        dirpath = os.path.dirname(ply_path)
        dir_to_files.setdefault(dirpath, set()).add(os.path.basename(ply_path))

    redundant = set()
    for dirpath, filenames in dir_to_files.items():
        for filename in filenames:
            if is_redundant_mesh_1(filename, filenames):
                redundant.add(os.path.join(dirpath, filename))
    return redundant


def organize(root_dir, recursive, dry_run):
    moved = 0
    skipped = 0
    conflicts = 0
    removed = 0

    ply_paths = collect_ply_paths(root_dir, recursive)
    print(f"Found {len(ply_paths)} .ply files under {root_dir}.")

    redundant_mesh_1 = find_redundant_mesh_1(ply_paths)
    if redundant_mesh_1:
        for ply_path in sorted(redundant_mesh_1):
            if dry_run:
                print(f"[dry-run] delete {ply_path}")
            else:
                os.remove(ply_path)
                removed += 1
        if not dry_run:
            ply_paths = [p for p in ply_paths if p not in redundant_mesh_1]

    for ply_path in ply_paths:
        if dry_run and ply_path in redundant_mesh_1:
            continue
        filename = os.path.basename(ply_path)
        prefix = extract_prefix(filename)
        if not prefix:
            skipped += 1
            continue

        parent_dir = os.path.dirname(ply_path)
        if os.path.basename(parent_dir) == prefix:
            skipped += 1
            continue

        dest_dir = os.path.join(parent_dir, prefix)
        dest_path = os.path.join(dest_dir, filename)
        if os.path.exists(dest_path):
            conflicts += 1
            print(f"Conflict (exists): {dest_path}")
            continue

        if dry_run:
            print(f"[dry-run] {ply_path} -> {dest_path}")
        else:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(ply_path, dest_path)
        moved += 1

    print(f"Removed redundant mesh_1: {removed}")
    print(f"Moved: {moved}, Skipped: {skipped}, Conflicts: {conflicts}")


def main():
    parser = argparse.ArgumentParser(
        description="Organize .ply files into prefix folders based on '<prefix>_mesh' naming."
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=os.getcwd(),
        help="Root directory to scan (default: current working directory).",
    )
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Only process the root directory (no recursion).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned moves without changing files.",
    )
    parser.set_defaults(recursive=True)
    args = parser.parse_args()

    organize(args.root_dir, args.recursive, args.dry_run)


if __name__ == "__main__":
    main()
