
def lcv_score(csp, assignment, domains, var, value, check_timeout=None):
    """Count values eliminated from unassigned neighbors by var=value."""
    eliminated = 0

    for neighbor in csp.neighbors[var]:
        if check_timeout is not None:
            check_timeout()

        if neighbor in assignment:
            continue

        for neighbor_value in domains[neighbor]:
            if check_timeout is not None:
                check_timeout()

            if not csp.is_allowed(var, value, neighbor, neighbor_value):
                eliminated += 1

    return eliminated


def order_values(
    csp,
    assignment,
    domains,
    var,
    use_lcv=False,
    check_timeout=None,
):
    """Return domain values, optionally ordered by least-constraining value."""

    if check_timeout is not None:
        check_timeout()

    values = list(domains[var])

    if not use_lcv:
        return values

    # Calculate scores explicitly so timeout checks can run between values.
    scored_values = []

    for value in values:
        if check_timeout is not None:
            check_timeout()

        score = lcv_score(
            csp,
            assignment,
            domains,
            var,
            value,
            check_timeout=check_timeout,
        )

        scored_values.append((value, score))

    # Lower scores mean fewer values eliminated, so those values are preferred.
    scored_values.sort(key=lambda item: item[1])

    if check_timeout is not None:
        check_timeout()

    return [value for value, score in scored_values]

