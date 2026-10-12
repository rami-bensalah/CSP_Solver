
def forward_check(
    csp,
    assignment,
    domains,
    remove_value,
    var,
    value,
    check_timeout=None,
):
    """Prune unsupported values from unassigned neighbors of var."""

    for neighbor in csp.neighbors[var]:
        if check_timeout is not None:
            check_timeout()

        if neighbor in assignment:
            continue

        for neighbor_value in list(domains[neighbor]):
            if check_timeout is not None:
                check_timeout()

            if not csp.is_allowed(
                var,
                value,
                neighbor,
                neighbor_value,
            ):
                remove_value(neighbor, neighbor_value)

        if not domains[neighbor]:
            return False

    return True
