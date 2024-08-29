import os
import shutil
import pandas as pd

# Paths
base_folder = "results/DENV2/primer_scheme"
destination_folder = os.path.join(base_folder, "all_amplicon_stats")
total = 10

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Traverse through the base_folder
for folder in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder)
    
    # Check if the folder follows the {sample_1}_{double}_{sample_2}_{double} pattern
    if os.path.isdir(folder_path) and len(folder.split("_")) == 4:
        # Extract parts of the folder name
        sample_1, double_1, sample_2, double_2 = folder.split("_")
        
        # Build paths to results/{sample1}/amplicons/amplicon_stats.csv and results/{sample2}/amplicons/amplicon_stats.csv
        sample_1_stats = os.path.join(folder_path, "results", sample_1, "amplicons", "amplicon_stats.csv")
        sample_2_stats = os.path.join(folder_path, "results", sample_2, "amplicons", "amplicon_stats.csv")
        
        # Create new file names for copying
        sample_1_copy_name = f"{sample_1}_{double_1}_{sample_2}_{double_2}_amplicon_stats.csv"
        sample_2_copy_name = f"{sample_2}_{double_2}_{sample_1}_{double_1}_amplicon_stats.csv"
        
        # Copy the files to the destination folder with the new names
        shutil.copy(sample_1_stats, os.path.join(destination_folder, sample_1_copy_name))
        shutil.copy(sample_2_stats, os.path.join(destination_folder, sample_2_copy_name))

    # Check if the folder follows the {sample_1}_{double} pattern
    elif os.path.isdir(folder_path) and len(folder.split("_")) == 2:
        sample_1, double_1 = folder.split("_")
        sample_1_stats = os.path.join(folder_path, "results", sample_1, "amplicons", "amplicon_stats.csv")
        sample_1_copy_name = f"{sample_1}_{double_1}_amplicon_stats.csv"
        shutil.copy(sample_1_stats, os.path.join(destination_folder, sample_1_copy_name))

print("Amplicon stats files have been copied and renamed.")



# Initialize a dictionary to store the counts and details
amplicon_data = {}

# Iterate through all files in the folder
for filename in os.listdir(destination_folder):
    if filename.endswith("_amplicon_stats.csv"):
        # Read the CSV file into a DataFrame
        file_path = os.path.join(destination_folder, filename)
        df = pd.read_csv(file_path)
        
        # Filter rows where primer_start, primer_end, and amplicon_length are all 0
        filtered_df = df[(df['primer_start'] == 0) & 
                         (df['primer_end'] == 0) & 
                         (df['amplicon_length'] == 0)]
        
        # Iterate over the filtered rows and count occurrences
        for _, row in filtered_df.iterrows():
            amplicon_number = row['amplicon_number']
            
            # If the amplicon_number is already in the dictionary, increment the count
            if amplicon_number in amplicon_data:
                amplicon_data[amplicon_number]['count'] += 1
            else:
                # If not, initialize the entry with count = 1 and store other details
                amplicon_data[amplicon_number] = {
                    'count': 1,
                    'primer_start': row['primer_start'],
                    'primer_end': row['primer_end'],
                    'amplicon_length': row['amplicon_length'],
                    'primer_seq_x': row['primer_seq_x'],
                    'primer_seq_y': row['primer_seq_y']
                }

# Convert the result to a df for easier display
output_data = []
for amplicon_number, data in amplicon_data.items():
    proportion = data['count'] / total
    output_data.append([
        amplicon_number, 
        data['count'], 
        proportion,
        data['primer_seq_x'], 
        data['primer_seq_y']
    ])

output_df = pd.DataFrame(output_data, columns=[
    'amplicon_number', 
    'count', 
    'proportion',
    'primer_seq_x', 
    'primer_seq_y'
])

# Sort the df by amplicon_number for readability
output_df.sort_values(by='amplicon_number', inplace=True)

print(output_df)
save_to = os.path.join(destination_folder, "all_amplicon_stats.csv")
output_df.to_csv(save_to, index=False)