"""
Created in March 28 2025
For firebrand seperation from .PLY
@author: Ha-Ninh NGUYEN
"""
import argparse
import open3d as o3d
import numpy as np
import os

def segment_mesh_objects(ply_file, output_folder, distance_threshold=0.02, min_cluster_size=100):
    mesh = o3d.io.read_triangle_mesh(ply_file)
    if not mesh.is_edge_manifold():
        mesh.remove_duplicated_vertices()
        mesh.remove_duplicated_triangles()
        mesh.remove_degenerate_triangles()

    triangle_clusters, cluster_n_triangles, _ = mesh.cluster_connected_triangles()
    triangle_clusters = np.asarray(triangle_clusters)
    num_clusters = len(np.unique(triangle_clusters))
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(ply_file))[0]
    saved_count, skipped_count = 0, 0

    for i, cluster_size in enumerate(cluster_n_triangles):
        if cluster_size < min_cluster_size:
            skipped_count += 1
            continue

        mask = triangle_clusters == i
        triangle_indices = np.where(mask)[0]
        cluster_mesh = o3d.geometry.TriangleMesh()
        cluster_mesh.vertices = mesh.vertices
        cluster_mesh.triangles = o3d.utility.Vector3iVector(np.asarray(mesh.triangles)[triangle_indices])
        cluster_mesh.compute_vertex_normals()

        bounding_box = cluster_mesh.get_axis_aligned_bounding_box()
        if bounding_box.get_max_extent() < distance_threshold:
            skipped_count += 1
            continue

        output_file = os.path.join(output_folder, f"{base_name}_{saved_count + 1}.ply")
        o3d.io.write_triangle_mesh(output_file, cluster_mesh)
        saved_count += 1

    return num_clusters, saved_count, skipped_count

def process_all_ply_files(root_dir, output_subdir, distance_threshold, min_cluster_size):
    ply_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if output_subdir:
            # Skip any existing output folders to avoid re-processing segmented meshes.
            if output_subdir in dirpath.split(os.sep):
                continue
        for filename in filenames:
            if filename.endswith(".ply"):
                ply_paths.append(os.path.join(dirpath, filename))

    total_files = len(ply_paths)
    print(f"Found {total_files} PLY files under {root_dir}. Processing...")

    for ply_path in ply_paths:
        parent_dir = os.path.dirname(ply_path)
        output_folder = parent_dir if not output_subdir else os.path.join(parent_dir, output_subdir)
        print(f"Processing {ply_path}...")
        num_clusters, saved_count, skipped_count = segment_mesh_objects(
            ply_path,
            output_folder,
            distance_threshold=distance_threshold,
            min_cluster_size=min_cluster_size,
        )
        print(
            f"{os.path.basename(ply_path)}: Found {num_clusters} objects, "
            f"saved {saved_count}, skipped {skipped_count} small clusters."
        )

    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Segment all PLY files under a directory tree.")
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Root directory to scan for .ply files (default: script directory).",
    )
    parser.add_argument(
        "--output-subdir",
        default="",
        help="Output folder name created next to each .ply file (default: same folder).",
    )
    parser.add_argument(
        "--distance-threshold",
        type=float,
        default=50,
        help="Minimum max extent for a cluster to be saved.",
    )
    parser.add_argument(
        "--min-cluster-size",
        type=int,
        default=1000,
        help="Minimum number of triangles in a cluster to be saved.",
    )
    args = parser.parse_args()

    process_all_ply_files(
        root_dir=args.root_dir,
        output_subdir=args.output_subdir,
        distance_threshold=args.distance_threshold,
        min_cluster_size=args.min_cluster_size,
    )
