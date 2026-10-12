def sequential_search(
    lower_bound,
    upper_bound,
    solver_factory,
    objective="min",
):
    if lower_bound > upper_bound:
        raise ValueError("lower_bound must not exceed upper_bound")

    if objective == "min":
        candidates = range(lower_bound, upper_bound + 1)
    elif objective == "max":
        candidates = range(upper_bound, lower_bound - 1, -1)
    else:
        raise ValueError("objective must be 'min' or 'max'")

    tested = []

    for candidate in candidates:
        solver = solver_factory(candidate)
        solution = solver.solve()

        tested.append({
            "candidate": candidate,
            "status": solver.status,
            "elapsed_time": solver.elapsed_time,
            "nodes_explored": solver.nodes_explored,
            "backtracks": solver.backtracks,
        })

        if solver.status == "UNKNOWN":
            return {
                "status": "UNKNOWN",
                "candidate": None,
                "solution": None,
                "tested": tested,
            }

        if solver.status == "SAT":
            return {
                "status": "OPTIMAL",
                "candidate": candidate,
                "solution": solution,
                "tested": tested,
            }

    return {
        "status": "INFEASIBLE",
        "candidate": None,
        "solution": None,
        "tested": tested,
    }