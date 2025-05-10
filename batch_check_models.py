import os
from z3 import *

# Load CNF file in DIMACS format and return number of variables and clauses
def load_cnf(filename):
    clauses = []
    num_vars = 0
    with open(filename) as f:
        for line in f:
            if line.startswith('c') or line.strip() == '':
                 # Skip comments and blank lines
                continue 
            if line.startswith('p'):
                _, _, vars_str, _ = line.split()
                #  Read number of variables
                num_vars = int(vars_str)
                continue
            # Parse literals in each clause
            clause = [int(x) for x in line.strip().split() if x != '0']
            clauses.append(clause)
    return num_vars, clauses

# Load model file (list of assigned literals) as a set of integers
def load_model(filename):
    with open(filename) as f:
        for line in f:
            tokens = line.strip().split()
            return set(int(x) for x in tokens if x != '0')
    raise ValueError("Model file is empty or missing valid integers")

# Check if a model satisfies a given CNF using Z3
def validate_model(num_vars, clauses, model):
    # Create Z3 variables
    z3_vars = {i: Bool(f"x{i}") for i in range(1, num_vars + 1)}
    z3_clauses = []

    for clause in clauses:
        literals = []
        for lit in clause:
            var = z3_vars[abs(lit)]
            # Build clause expression
            literals.append(var if lit > 0 else Not(var))
        z3_clauses.append(Or(*literals))

    # Combine all clauses into full formula
    formula = And(*z3_clauses)

    # Add model assignments to Z3
    assumptions = []
    for i in range(1, num_vars + 1):
        var = z3_vars[i]
        if i in model:
            assumptions.append(var)
        elif -i in model:
            assumptions.append(Not(var))

    # Check satisfiability under the given assignment
    s = Solver()
    s.add(formula)
    s.add(assumptions)
    return s.check() == sat

# Validate all CNF/model pairs and save results to a file
def batch_validate(cnf_folder, model_folder, output_file="validation_results.txt"):
    with open(output_file, "w") as out:
        for cnf_file in os.listdir(cnf_folder):
            if not cnf_file.endswith(".cnf"):
                # Skip non-CNF files
                continue

            cnf_path = os.path.join(cnf_folder, cnf_file)
            model_name = cnf_file + "model.txt"
            model_path = os.path.join(model_folder, model_name)

            if not os.path.isfile(model_path):
                out.write(f"[MISSING MODEL] {cnf_file}: model file '{model_name}' not found\n")
                continue

            try:
                # Load CNF and corresponding model
                num_vars, clauses = load_cnf(cnf_path)
                model = load_model(model_path)

                 # Validate model
                valid = validate_model(num_vars, clauses, model)

                # Log result
                if valid:
                    out.write(f"[VALID]   {cnf_file}\n")
                else:
                    out.write(f"[INVALID] {cnf_file}: model does not satisfy CNF\n")

            # Log any errors
            except Exception as e:
                out.write(f"[ERROR]   {cnf_file}: {str(e)}\n")

    print(f"Validation complete. Results saved to '{output_file}'.")

# run the batch validation:

# 1) Used for 3sat fuzzer on the cadical solver
#batch_validate("3sat_solvers_output\\3sat_cnf_instances", "3sat_solvers_output\\cadical_models", "3sat_solvers_output\\cadical_validation_results.txt")

# 2) Used for fuzzsat fuzzer on the esa solver
batch_validate("fuzzsat_300_solvers_output\\cnf_instances", "fuzzsat_300_solvers_output\\sc2024_models", "fuzzsat_300_solvers_output\\sc2024_validation_results.txt")

# When you change the fuzzer you are checking, you need to change the output directory name as well for all three arguments
# When you change the solver you are checking, you need to change the name of the solver for the second and third arguments