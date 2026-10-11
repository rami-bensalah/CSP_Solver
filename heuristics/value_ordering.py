def lcv_score(csp, assignment, domains, var, value):
    """Count values eliminated from unassigned neighbors by var=value."""
    eliminated = 0

    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            continue

        for neighbor_value in domains[neighbor]:
            if not csp.is_allowed(var, value, neighbor, neighbor_value):
                eliminated += 1

    return eliminated


def order_values(csp, assignment, domains, var, use_lcv=False):
    """Return domain values, optionally ordered by least-constraining value."""
    values = list(domains[var])

    if not use_lcv:
        return values

    return sorted(
        values,
        key=lambda value: lcv_score(csp, assignment, domains, var, value),
    )
