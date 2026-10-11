import pickle
from pathlib import Path
from csp import CSPInstance, CSPSolver


def load_instance(filename):
    """Load a previously saved CSP instance."""
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"Instance not found: {path}")

    with open(path, "rb") as file:
        instance = pickle.load(file)

    return instance["n"], instance["domains"], instance["constraints"]


n, domains, constraints = load_instance(
    "Problems/nqueens/nqueens_instances/nqueens_8.pkl"
)

print("N =", n)
print("Domains:", domains)
print("Number of constraints:", len(constraints))

csp = CSPInstance(domains, constraints)

solver = CSPSolver(
    csp,
    use_forward_checking=False,
    use_mac=True,
    use_full_ac3=False,
    use_mrv=True,
    use_degree=True,
    use_lcv=True,
)

solution = solver.solve()

print("Solution:", solution)
print("Nodes explored:", solver.nodes_explored)
print("Backtracks:", solver.backtracks)