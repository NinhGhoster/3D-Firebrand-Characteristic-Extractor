import trimesh
import numpy as np
import os

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

# Set working directory
current_directory = os.getcwd()
ply_folder = os.path.join(current_directory, "segmented_mesh_objects")
output_csv = os.path.join(current_directory, "mesh_volumes_and_bboxes.csv")
output_pca_folder = os.path.join(current_directory, "pca_obb_meshes")
os.makedirs(output_pca_folder, exist_ok=True)

import csv
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'File (ID)', 'Volume (mm³)', 'Surface Area (mm²)',
        'AABB L', 'AABB W', 'AABB H',
        'Trimesh OBB L', 'Trimesh OBB W', 'Trimesh OBB H',
        'PCA-OBB L', 'PCA-OBB W', 'PCA-OBB H'
    ])

    for filename in os.listdir(ply_folder):
        if filename.endswith(".ply"):
            mesh = trimesh.load_mesh(os.path.join(ply_folder, filename))
            volume = mesh.volume
            surface_area = mesh.area

            # AABB
            aabb = mesh.bounding_box.extents

            # Trimesh OBB
            try:
                obb = mesh.bounding_box_oriented.extents
            except Exception:
                obb = [np.nan, np.nan, np.nan]

            # PCA OBB
            try:
                pca_extents, rotation, mean = pca_bounding_box(mesh)
            except Exception:
                pca_extents = [np.nan, np.nan, np.nan]
                rotation = np.eye(3)
                mean = np.zeros(3)

            # Save mesh rotated to PCA axes for inspection
            transformed_vertices = (np.array(mesh.vertices) - mean) @ rotation
            mesh_pca = trimesh.Trimesh(vertices=transformed_vertices, faces=mesh.faces)
            output_mesh_path = os.path.join(output_pca_folder, filename)
            mesh_pca.export(output_mesh_path)

            # Write CSV
            writer.writerow([
                filename, f"{volume:.3f}", f"{surface_area:.3f}",
                f"{aabb[0]:.3f}", f"{aabb[1]:.3f}", f"{aabb[2]:.3f}",
                f"{obb[0]:.3f}", f"{obb[1]:.3f}", f"{obb[2]:.3f}",
                f"{pca_extents[0]:.3f}", f"{pca_extents[1]:.3f}", f"{pca_extents[2]:.3f}"
            ])

            print(f"Processed {filename} | AABB: {aabb.round(3)} | "
                  f"Trimesh OBB: {np.round(obb,3)} | PCA OBB: {np.round(pca_extents,3)}")

print(f"Results saved to {output_csv} and PCA meshes saved to {output_pca_folder}")
