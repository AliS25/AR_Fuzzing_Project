import os
from z3 import *

def load_cnf(filename):
    clauses = []
    num_vars = 0
    with open(filename) as f:
        for line in f:
            if line.startswith('c') or line.strip() == '':
                continue
            if line.startswith('p'):
                _, _, vars_str, _ = line.split()
                num_vars = int(vars_str)
                continue
            clause = [int(x) for x in line.strip().split() if x != '0']
            clauses.append(clause)
    return num_vars, clauses

def load_model(filename):
    with open(filename) as f:
        for line in f:
            tokens = line.strip().split()
            return set(int(x) for x in tokens if x != '0')
    raise ValueError("Model file is empty or missing valid integers")

def validate_model(num_vars, clauses, model):
    z3_vars = {i: Bool(f"x{i}") for i in range(1, num_vars + 1)}
    z3_clauses = []

    for clause in clauses:
        literals = []
        for lit in clause:
            var = z3_vars[abs(lit)]
            literals.append(var if lit > 0 else Not(var))
        z3_clauses.append(Or(*literals))

    formula = And(*z3_clauses)

    assumptions = []
    for i in range(1, num_vars + 1):
        var = z3_vars[i]
        if i in model:
            assumptions.append(var)
        elif -i in model:
            assumptions.append(Not(var))

    s = Solver()
    s.add(formula)
    s.add(assumptions)
    return s.check() == sat

def batch_validate(cnf_folder, model_folder, output_file="validation_results.txt"):
    with open(output_file, "w") as out:
        for cnf_file in os.listdir(cnf_folder):
            if not cnf_file.endswith(".cnf"):
                continue

            cnf_path = os.path.join(cnf_folder, cnf_file)
            model_name = cnf_file + "model.txt"
            model_path = os.path.join(model_folder, model_name)

            if not os.path.isfile(model_path):
                out.write(f"[MISSING MODEL] {cnf_file}: model file '{model_name}' not found\n")
                continue

            try:
                num_vars, clauses = load_cnf(cnf_path)
                model = load_model(model_path)
                valid = validate_model(num_vars, clauses, model)

                if valid:
                    out.write(f"[VALID]   {cnf_file}\n")
                else:
                    out.write(f"[INVALID] {cnf_file}: model does not satisfy CNF\n")

            except Exception as e:
                out.write(f"[ERROR]   {cnf_file}: {str(e)}\n")

    print(f"✅ Validation complete. Results saved to '{output_file}'.")

# run the batch validation:

# 1) Used for 3sat fuzzer on the cadical solver
#batch_validate("3sat_solvers_output\\3sat_cnf_instances", "3sat_solvers_output\\cadical_models", "3sat_solvers_output\\cadical_validation_results.txt")

# 2) Used for fuzzsat fuzzer on the esa solver
batch_validate("fuzzsat_solvers_output\\cnf_instances", "fuzzsat_solvers_output\\esa_models", "fuzzsat_solvers_output\\esa_validation_results.txt")

# When you change the fuzzer you are checking, you need to change the output directory name as well for all three arguments
# When you change the solver you are checking, you need to change the name of the solver for the second and third arguments