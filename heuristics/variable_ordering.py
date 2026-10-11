import random


def select_variable(csp, assignment, domains, use_mrv=False, use_degree=False):
    """Choose an unassigned variable using MRV and/or degree.

    MRV + degree: smallest domain first, then most unassigned neighbors.
    Degree alone: most unassigned neighbors.
    Neither: randomly select an unassigned variable.
    """
    unassigned = [
        var for var in csp.domains
        if var not in assignment
    ]

    if not unassigned:
        return None

    def mrv_score(var):
        return len(domains[var])

    def degree_score(var):
        return sum(
            1 for neighbor in csp.neighbors[var]
            if neighbor not in assignment
        )

    if use_mrv and use_degree:
        return min(
            unassigned,
            key=lambda var: (mrv_score(var), -degree_score(var))
        )

    if use_mrv:
        return min(unassigned, key=mrv_score)

    if use_degree:
        return max(unassigned, key=degree_score)

    # Random selection when neither heuristic is enabled
    return random.choice(unassigned)