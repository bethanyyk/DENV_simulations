import itertools
import pandas as pd
import subprocess
import random

ISOLATES = [i for i in open("unique_isolates.txt").read().split('\n') if len(i) >0]

# Generate 4 random proportion combinations
isolate_combinations = list(itertools.combinations(ISOLATES, 2))
primer_bed_file = "results/DENV2/DENV2.bed"
for isolate_combination in isolate_combinations:
    proportion1 = round(random.uniform(0, 1), 2)
    proportion2 = round(1.0 - proportion1, 2)
    file1_path = isolate_combination[0] + ".fasta"
    file2_path = isolate_combination[1] + ".fasta"
    output_path = "results/DENV2/lineage_combine/" + isolate_combination[0] + "_" + str(proportion1) + "_" +  isolate_combination[1] + "_" + str(proportion2)
    command = [
            "python3", "workflow/scripts/amplicon_simulator_wrapper.py",
            "-s",f"{isolate_combination[0]},{isolate_combination[1]}" ,
            "-sp", f"{file1_path},{file2_path}",
            "-pr", f"{proportion1},{proportion2}",
            "-p", primer_bed_file,
            "-n", "100000",
            "-o", output_path
        ]
    # Execute the command
    subprocess.run(command, check=True)