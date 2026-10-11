from heuristics.variable_ordering import select_variable
from heuristics.value_ordering import order_values


def backtrack(solver):
    """Recursive backtracking search, coordinated through the solver API."""
    if solver.is_complete():
        return True

    solver.nodes_explored += 1

    # Optional expensive mode: run full AC-3 at every search node.
    if solver.use_full_ac3:
        ac3_position = solver.trail.position()
        if not solver.run_full_ac3():
            solver.trail.restore(ac3_position)
            return False

    var = select_variable(
        solver.csp,
        solver.assignment,
        solver.csp.domains,
        use_mrv=solver.use_mrv,
        use_degree=solver.use_degree,
    )

    values = order_values(
        solver.csp,
        solver.assignment,
        solver.csp.domains,
        var,
        use_lcv=solver.use_lcv,
    )

    for value in values:
        if not solver.is_consistent(var, value):
            continue

        trail_position = solver.trail.position()

        solver.assignment[var] = value
        solver.assign_value(var, value)

        if solver.propagate(var, value) and backtrack(solver):
            return True

        solver.trail.restore(trail_position)
        del solver.assignment[var]
        solver.backtracks += 1

    return False
