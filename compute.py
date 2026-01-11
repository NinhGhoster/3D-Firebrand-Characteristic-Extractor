"""
Created in March 28 2025
For firebrand seperation from .PLY
@author: Ha-Ninh NGUYEN
"""
import trimesh
import os
import csv

# Set the working directory dynamically
current_directory = os.getcwd()  # Gets the directory where the script is running
ply_folder = os.path.join(current_directory, "segmented_mesh_objects")  # Folder inside working directory
output_file = os.path.join(current_directory, "mesh_volumes_and_bboxes.csv")  # Output file in the same directory

# Prepare the CSV file for writing results
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header with units
    writer.writerow(['File (ID)', 'Volume (mm³)', 'Surface Area (mm²)', 'Length (mm)', 'Width (mm)', 'Height (mm)', 'Mass (g)'])

    # Iterate through all PLY files
    for filename in os.listdir(ply_folder):
        if filename.endswith(".ply"):
            # Load mesh
            mesh = trimesh.load_mesh(os.path.join(ply_folder, filename))
            
            # Compute volume and surface area
            volume = mesh.volume  # mm³
            surface_area = mesh.area  # mm²
            
            # Get the axis-aligned bounding box (AABB)
            bbox_length, bbox_width, bbox_height = mesh.bounding_box.extents  # Length, width, height in mm
            
            # Write the results to CSV (Mass column left empty for manual input)
            writer.writerow([filename, f"{volume:.3f}", f"{surface_area:.3f}", f"{bbox_length:.3f}", f"{bbox_width:.3f}", f"{bbox_height:.3f}", ""])

            print(f"Processed {filename} - Volume: {volume:.3f} mm³, Surface Area: {surface_area:.3f} mm², "
                  f"Size (LxWxH): {bbox_length:.3f} x {bbox_width:.3f} x {bbox_height:.3f} mm")

print(f"Results saved to {output_file}")
