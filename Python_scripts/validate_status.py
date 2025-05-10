import csv
import sys
import os
from collections import defaultdict

# Update the name of the output file to the respective fuzzer name
output_file = "3sat_1000_combined_results.csv"
# Update the name of the folder containing the CSV files to the respective fuzzer name
csv_folder = "3sat_1000_solvers_output"

# Check if the user provided at least two CSV files as arguments
if len(sys.argv) < 3:
    print("Usage: python compare_csvs.py csv1.csv csv2.csv ...")
    sys.exit(1)

# List of input CSV files
csv_files = sys.argv[1:]

# Dictionary to store results for each filename from all CSVs
results_by_filename = defaultdict(dict)

# Read each CSV file and collect results
for csv_file in csv_files:
    # Update file path to include the folder
    csv_file = os.path.join(csv_folder, csv_file)

    # Generate a label based on the CSV filename
    label = f"result_{os.path.splitext(os.path.basename(csv_file))[0]}"
    
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        # Read each row in the CSV
        for row in reader:
            filename = row[0]   # First column:the filename
            result = row[1].strip().lower() # Second column: the result
            results_by_filename[filename][label] = result # Store result under the corresponding label

# All result column labels
all_labels = sorted({label for r in results_by_filename.values() for label in r})
# All filenames across all CSVs
all_filenames = sorted(results_by_filename.keys())


# Write output
with open(output_file, "w", newline='') as out:
    writer = csv.writer(out)

    # Write the header: filename + one column for each input CSV + a final mismatch column
    writer.writerow(["filename"] + all_labels + ["mismatch"])

    # Process each filename row-by-row
    for filename in all_filenames:
        # Get the list of results in order of all_labels (to keep columns aligned)
        results = [results_by_filename[filename].get(label, "") for label in all_labels]
        
        # Filter out only the results we care about for mismatch: satisfiable vs unsatisfiable
        core_results = {r for r in results if r in {"satisfiable", "unsatisfiable"}}
       
        # Mark as "yes" only if both "satisfiable" and "unsatisfiable" appear
        mismatch = "yes" if len(core_results) > 1 else "no"
        
        # Write the full row to the output CSV
        writer.writerow([filename] + results + [mismatch])

# Print confimation message
print("Combined results saved to ", output_file)
