import csv
import os
import sys

# Check for CSV filename argument
if len(sys.argv) != 2:
    print("Usage: python script.py input.csv")
    sys.exit(1)

#  Get the input CSV file path from command-line argument and extract the name to use for the output folder
csv_path = sys.argv[1]
csv_name = os.path.splitext(os.path.basename(csv_path))[0]
output_dir = f"fuzzsat_300_solvers_output/{csv_name}_models"
os.makedirs(output_dir, exist_ok=True)

# Read and process the CSV
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header

    # Read each row in the CSV
    for row in reader:
        filename, result, assignment = row[0], row[1].strip().lower(), row[2]

        # If result is satisfiable, create a file and write the assignment to it
        if result == 'satisfiable':
            file_path = os.path.join(output_dir, filename+'model.txt')
            with open(file_path, 'w') as f:
                f.write(assignment)

# confirmation message
print(f"Files created in folder: {output_dir}")

## When you change the fuzzer you are checking, you need to change the output directory name as well.