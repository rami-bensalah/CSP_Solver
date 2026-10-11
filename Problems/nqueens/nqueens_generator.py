import pickle
from pathlib import Path
def generate_nqueens(n):

    domains = {
        i: set(range(1, n + 1))
        for i in range(n)
    }

    constraints = {}

    for i in range(n):

        for j in range(i + 1, n):

            allowed_pairs = set()

            for col_i in range(1, n + 1):

                for col_j in range(1, n + 1):

                    # Same column
                    if col_i == col_j:
                        continue

                    # Same diagonal \
                    if i - col_i == j - col_j:
                        continue

                    # Same diagonal /
                    if i + col_i == j + col_j:
                        continue

                    allowed_pairs.add(
                        (col_i, col_j)
                    )

            constraints[(i, j)] = allowed_pairs

    return domains, constraints
def save_nqueens_instances(min_n=4, max_n=12):
    # Create a directory to store the instances
    output_dir = Path("nqueens_instances")
    output_dir.mkdir(exist_ok=True)

    for n in range(min_n, max_n + 1):
        domains, constraints = generate_nqueens(n)

        instance = {
            "n": n,
            "domains": domains,
            "constraints": constraints
        }

        filename = output_dir / f"nqueens_{n}.pkl"

        with open(filename, "wb") as file:
            pickle.dump(instance, file)

        print(f"Saved N-Queens {n} to {filename}")


if __name__ == "__main__":
    save_nqueens_instances()