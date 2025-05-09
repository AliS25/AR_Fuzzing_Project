import csv
import sys
import os
from collections import defaultdict

# Update the name of the output file to the respective fuzzer name
output_file = "fuzzsat_combined_results.csv"
# Update the name of the folder containing the CSV files to the respective fuzzer name
csv_folder = "fuzzsat_solvers_output"

# Usage check
if len(sys.argv) < 3:
    print("Usage: python compare_csvs.py csv1.csv csv2.csv ...")
    sys.exit(1)

csv_files = sys.argv[1:]
results_by_filename = defaultdict(dict)

# Read each CSV file and collect results
for csv_file in csv_files:
    csv_file = os.path.join(csv_folder, csv_file)
    label = f"result_{os.path.splitext(os.path.basename(csv_file))[0]}"
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            filename = row[0]
            result = row[1].strip().lower()
            results_by_filename[filename][label] = result

# All result column labels
all_labels = sorted({label for r in results_by_filename.values() for label in r})
all_filenames = sorted(results_by_filename.keys())


# Write output
with open(output_file, "w", newline='') as out:
    writer = csv.writer(out)
    writer.writerow(["filename"] + all_labels + ["mismatch"])

    for filename in all_filenames:
        results = [results_by_filename[filename].get(label, "") for label in all_labels]
        core_results = {r for r in results if r in {"satisfiable", "unsatisfiable"}}
        mismatch = "yes" if len(core_results) > 1 else "no"
        writer.writerow([filename] + results + [mismatch])

print("Combined results saved to ", output_file)
