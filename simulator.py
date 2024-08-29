import os
import subprocess

# Define the directory containing the files
directory = 'results/DENV3'

# Define the path to the DENV3.bed file
bed_file = os.path.join(directory, 'DENV3.bed')

# Define the path for the results folder
results_dir = os.path.join(directory, 'primer_scheme')

# Create the results directory if it doesn't exist
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Iterate over the files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Check if the file has a .fasta extension
    if filename.endswith('.fasta') and filename != 'reference.fasta' and filename != 'genbank.fasta':
        sample = filename[:-6]

        # Define the output folder for this specific fasta file
        output_folder = os.path.join(results_dir, f'{filename}_1.0')

        # Run the command for the amplicon simulator wrapper
        command = [
            'python', 'workflow/scripts/amplicon_simulator_wrapper.py', 
            '-s', filename, 
            '-sp', file_path, 
            '-pr', '1', 
            '-p', bed_file, 
            '-n', '100000', 
            '-o', output_folder
        ]

        subprocess.run(command)