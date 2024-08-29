import os
import shutil
import pandas as pd

# Paths
base_folder = "results/DENV3/primer_scheme"
destination_folder = os.path.join(base_folder, "demix")
total = 9

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Traverse through the base_folder
for folder in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder)
    
    # Check if the folder follows the {sample_1}_{double}_{sample_2}_{double} pattern
    if os.path.isdir(folder_path) and len(folder.split("_")) == 4:
        sample_1, double_1, sample_2, double_2 = folder.split("_")
        stats = os.path.join(folder_path, "freyja_demix.txt")
        demix_copy_name = f"{sample_1}_{double_1}_{sample_2}_{double_2}_freyja_demix.txt"
        
        # Copy the files to the destination folder with the new names
        shutil.copy(stats, os.path.join(destination_folder, demix_copy_name))
    elif os.path.isdir(folder_path) and len(folder.split("_")) == 2:
        sample_1, double_1 = folder.split("_")
        stats = os.path.join(folder_path, "freyja_demix.txt")
        demix_copy_name = f"{sample_1}_{double_1}_freyja_demix.txt"
        
        # Copy the files to the destination folder with the new names
        shutil.copy(stats, os.path.join(destination_folder, demix_copy_name))