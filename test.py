from csp import CSPInstance, CSPSolver

domains = {
    0: {1, 2, 3},
    1: {1, 2, 3},
    2: {1, 2, 3},
}

constraints = {
    (0, 1): {
        (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2),
    },
    (1, 2): {
        (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2),
    },
}

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