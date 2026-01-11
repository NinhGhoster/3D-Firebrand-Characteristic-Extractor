"""
Created in Nov 28 2024
For Point Cloud PLY
@author: Ha-Ninh NGUYEN
"""
import open3d as o3d
import numpy as np
import os

def segment_objects_in_ply(ply_file, output_folder, distance_threshold=1, min_points=10):
    """
    Segments objects in a PLY file and saves each segmented object as a separate PLY file.

    Parameters:
    - ply_file (str): Path to the input PLY file.
    - output_folder (str): Directory to save the segmented object files.
    - distance_threshold (float): Distance threshold for clustering (in the same units as the PLY file).
    - min_points (int): Minimum number of points to consider a cluster valid.

    Returns:
    - None
    """
    # Load the PLY file
    pcd = o3d.io.read_point_cloud(ply_file)
    print("Loaded point cloud:", pcd)

    # Estimate normals for better clustering
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    # Perform DBSCAN clustering
    labels = np.array(pcd.cluster_dbscan(eps=distance_threshold, min_points=min_points, print_progress=True))
    max_label = labels.max()
    print(f"Detected {max_label + 1} clusters.")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract and save each cluster
    for i in range(max_label + 1):
        cluster_indices = (labels == i)
        cluster = pcd.select_by_index(np.where(cluster_indices)[0])
        output_file = os.path.join(output_folder, f"cluster_{i}.ply")
        o3d.io.write_point_cloud(output_file, cluster)
        print(f"Saved cluster {i} to {output_file}")

    print("Segmentation completed and files saved.")

# Example usage
ply_file_path = "scanned_firebrands.ply"  # Replace with your PLY file path
output_directory = "segmented_objects"  # Replace with desired output folder
segment_objects_in_ply(ply_file_path, output_directory)