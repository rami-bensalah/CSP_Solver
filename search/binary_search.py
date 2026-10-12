def binary_search(
    lower_bound,
    upper_bound,
    solver_factory,
    objective="min",
):
    if lower_bound > upper_bound:
        raise ValueError("lower_bound must not exceed upper_bound")

    if objective not in ("min", "max"):
        raise ValueError("objective must be 'min' or 'max'")

    left = lower_bound
    right = upper_bound
    best_candidate = None
    best_solution = None
    tested = []

    while left <= right:
        candidate = (left + right) // 2

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
                "candidate": best_candidate,
                "solution": best_solution,
                "tested": tested,
            }

        if solver.status == "SAT":
            best_candidate = candidate
            best_solution = solution

            if objective == "min":
                right = candidate - 1
            else:
                left = candidate + 1

        else:  # UNSAT
            if objective == "min":
                left = candidate + 1
            else:
                right = candidate - 1

    if best_candidate is None:
        return {
            "status": "INFEASIBLE",
            "candidate": None,
            "solution": None,
            "tested": tested,
        }

    return {
        "status": "OPTIMAL",
        "candidate": best_candidate,
        "solution": best_solution,
        "tested": tested,
    }