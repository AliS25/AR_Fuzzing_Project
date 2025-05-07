import csv
import os

# Input CSV file path
csv_path = 'cryptominisat.csv'

# Output directory
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Read and process the CSV
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header if present

    for row in reader:
        filename, result, assignment = row[0], row[1].strip().lower(), row[2]

        if result == 'satisfiable':
            file_path = os.path.join(output_dir, filename+'model.txt')
            with open(file_path, 'w') as f:
                f.write(assignment)

print("Files created for satisfiable rows.")
