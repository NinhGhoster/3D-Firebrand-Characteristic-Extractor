"""
Created in March 28 2025
For firebrand seperation from .PLY
@author: Ha-Ninh NGUYEN
"""
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

def process_all_ply_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ply_files = [f for f in os.listdir(script_dir) if f.endswith(".ply")]
    output_folder = os.path.join(script_dir, "segmented_mesh_objects")
    
    total_files = len(ply_files)
    print(f"Found {total_files} PLY files. Processing...")
    
    for ply_file in ply_files:
        print(f"Processing {ply_file}...")
        num_clusters, saved_count, skipped_count = segment_mesh_objects(
            os.path.join(script_dir, ply_file), output_folder, distance_threshold=50, min_cluster_size=1000)
        print(f"{ply_file}: Found {num_clusters} objects, saved {saved_count}, skipped {skipped_count} small clusters.")
    
    print("Processing complete.")

if __name__ == "__main__":
    process_all_ply_files()
