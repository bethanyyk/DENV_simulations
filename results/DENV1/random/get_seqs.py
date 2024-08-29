import random
from Bio import SeqIO

def generate_random_numbers(total, num_to_select):
    return random.sample(range(1, total), num_to_select)

def extract_sequences(fasta_file, indices):
    sequences = list(SeqIO.parse(fasta_file, "fasta"))
    selected_sequences = [sequences[i - 1] for i in indices]
    return selected_sequences

def write_sequences_to_files(sequences):
    file_names = []
    for seq in sequences:
        file_name = f"{seq.id}.fasta"
        with open(file_name, "w") as output_handle:
            SeqIO.write(seq, output_handle, "fasta")
        file_names.append(file_name)
    return file_names

def generate_command(file_names, output_directory):
    sample_names = [name.split('.')[0] for name in file_names]
    sample_proportions = ','.join(['{:.2f}'.format(1/len(sample_names))]*len(sample_names))
    command = (
        f"python workflow/scripts/amplicon_simulator_wrapper.py "
        f"-s {','.join(sample_names)} "
        f"-sp {','.join(file_names)} "
        f"-pr {sample_proportions} "
        f"-p DENV1.bed "
        f"-n 10000 "
        f"-o {output_directory}"
    )
    return command

def main():
    total_sequences = 8357
    num_to_select = 20
    fasta_file = "genbank.fasta"
    output_directory = "output2"

    # Step 1: Generate random numbers
    random_indices = generate_random_numbers(total_sequences, num_to_select)

    # Step 2: Extract sequences and write to new files
    selected_sequences = extract_sequences(fasta_file, random_indices)
    file_names = write_sequences_to_files(selected_sequences)

    # Step 3: Generate the command
    command = generate_command(file_names, output_directory)
    print("Generated Command:", command)

if __name__ == "__main__":
    main()