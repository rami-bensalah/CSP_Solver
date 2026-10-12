
import random


def select_variable(
    csp,
    assignment,
    domains,
    use_mrv=False,
    use_degree=False,
    check_timeout=None,
):
    """Choose an unassigned variable using MRV and/or degree.

    MRV + degree: smallest domain first, then most unassigned neighbors.
    Degree alone: most unassigned neighbors.
    Neither: randomly select an unassigned variable.

    Args:
        csp: The CSP instance.
        assignment: Current variable assignments.
        domains: Current variable domains.
        use_mrv: Whether to use the minimum remaining values heuristic.
        use_degree: Whether to use the degree heuristic.
        check_timeout: Optional callback that raises an exception on timeout.
    """

    if check_timeout is not None:
        check_timeout()

    unassigned = []

    for var in csp.domains:
        if check_timeout is not None:
            check_timeout()

        if var not in assignment:
            unassigned.append(var)

    if not unassigned:
        return None

    def mrv_score(var):
        if check_timeout is not None:
            check_timeout()

        return len(domains[var])

    def degree_score(var):
        if check_timeout is not None:
            check_timeout()

        degree = 0

        for neighbor in csp.neighbors[var]:
            if check_timeout is not None:
                check_timeout()

            if neighbor not in assignment:
                degree += 1

        return degree

    if use_mrv and use_degree:
        # Minimum domain size, breaking ties by maximum degree.
        best_var = None
        best_score = None

        for var in unassigned:
            if check_timeout is not None:
                check_timeout()

            score = (mrv_score(var), -degree_score(var))

            if best_score is None or score < best_score:
                best_var = var
                best_score = score

        return best_var

    if use_mrv:
        return min(unassigned, key=mrv_score)

    if use_degree:
        # Keep the first variable in case of a tie, as max() does.
        return max(unassigned, key=degree_score)

    # Random selection when neither heuristic is enabled.
    if check_timeout is not None:
        check_timeout()

    return random.choice(unassigned)

