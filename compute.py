"""
Created in March 28 2025
For firebrand separation from .PLY
@author: Ha-Ninh NGUYEN
"""
import argparse
import os
import csv
import trimesh


def process_directory(dirpath, output_csv=None):
    """
    Process all .ply files in a directory using axis-aligned bounding box (AABB).
    
    Args:
        dirpath: Directory containing .ply files
        output_csv: Optional output CSV path. If None, defaults to mesh_volumes_and_bboxes.csv in dirpath
    
    Returns:
        Number of files processed
    """
    filenames = [
        f for f in os.listdir(dirpath)
        if f.lower().endswith(".ply") and os.path.isfile(os.path.join(dirpath, f))
    ]
    
    if not filenames:
        print(f"No .ply files found in {dirpath}")
        return 0
    
    # Default output filename if not specified
    if output_csv is None:
        output_csv = os.path.join(dirpath, "mesh_volumes_and_bboxes.csv")
    
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header with units
        writer.writerow(['File (ID)', 'Volume (mm3)', 'Surface Area (mm2)', 'Length (mm)', 'Width (mm)', 'Height (mm)', 'Mass (g)'])
        
        # Iterate through all PLY files
        for filename in sorted(filenames):
            try:
                # Load mesh
                mesh = trimesh.load_mesh(os.path.join(dirpath, filename))
                
                # Compute volume and surface area
                volume = abs(mesh.volume)  # mm3
                surface_area = mesh.area  # mm2
                
                # Get the axis-aligned bounding box (AABB)
                bbox_length, bbox_width, bbox_height = mesh.bounding_box.extents  # Length, width, height in mm
                
                # Write the results to CSV (Mass column left empty for manual input)
                writer.writerow([filename, f"{volume:.3f}", f"{surface_area:.3f}", f"{bbox_length:.3f}", f"{bbox_width:.3f}", f"{bbox_height:.3f}", ""])
                
                print(f"Processed {filename} - Volume: {volume:.3f} mm3, Surface Area: {surface_area:.3f} mm2, "
                      f"Size (LxWxH): {bbox_length:.3f} x {bbox_width:.3f} x {bbox_height:.3f} mm")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    print(f"Results saved to {output_csv}")
    return len(filenames)


def main():
    parser = argparse.ArgumentParser(
        description="Extract mesh characteristics (volume, surface area, bounding box) from .ply files using axis-aligned bounding box (AABB)."
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=os.getcwd(),
        help="Directory containing .ply files to process (default: current working directory).",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output CSV file path (default: mesh_volumes_and_bboxes.csv in input directory).",
    )
    args = parser.parse_args()
    
    # Convert to absolute path
    input_dir = os.path.abspath(args.input_dir)
    
    if not os.path.isdir(input_dir):
        print(f"Error: Directory not found: {input_dir}")
        return
    
    process_directory(input_dir, args.output)


if __name__ == "__main__":
    main()
