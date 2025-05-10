
import os
import random

def generate_3sat(n_vars, n_clauses, seed=None):
    """
    Generate a random 3-SAT instance.

    Args:
        n_vars (int): Number of variables.
        n_clauses (int): Number of clauses.
        seed (int, optional): Random seed.

    Returns:
        List[List[int]]: A list of clauses, each clause is a list of 3 integers.
    """
    if seed is not None:
        random.seed(seed)

    clauses = []

    for _ in range(n_clauses):
        # Pick 3 distinct variables
        vars_in_clause = random.sample(range(1, n_vars + 1), 3)
        # Randomly assign each a positive or negative sign
        clause = [var if random.choice([True, False]) else -var for var in vars_in_clause]
        clauses.append(clause)

    return clauses

def write_cnf(clauses, n_vars, filename):
    """
    Write the clauses to a DIMACS CNF file.

    Args:
        clauses (List[List[int]]): The list of clauses.
        n_vars (int): Number of variables.
        filename (str): Output filename.
    """
    with open(filename, 'w') as f:
        f.write(f"p cnf {n_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(' '.join(map(str, clause)) + ' 0\n')

if __name__ == "__main__":
    n_files = 1000        # how many CNF files you want to generate
    min_vars = 10       # minimum number of variables
    max_vars = 100      # maximum number of variables

    output_dir = "output_cnf"
    os.makedirs(output_dir, exist_ok=True)  # Create output folder if it doesn't exist

    for i in range(n_files):
        # Randomly pick number of variables between min_vars and max_vars
        n_vars = random.randint(min_vars, max_vars)

        # Randomly pick a seed
        seed = random.randint(0, 100000)

        # Number of clauses could be 3 to 5 times the number of variables for good hardness
        n_clauses = random.randint(3 * n_vars, 5 * n_vars)
        # Generate clauses
        clauses = generate_3sat(n_vars, n_clauses, seed=seed)

        # Create filename with information
        filename = f"{output_dir}/3sat_{i}.cnf"

        # Write to CNF file
        write_cnf(clauses, n_vars, filename)

        print(f"Generated {filename} with {n_vars} variables and seed {seed}")

