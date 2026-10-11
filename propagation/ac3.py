from collections import deque


def revise(csp, domains, remove_value, var1, var2):
    """Remove values from var1 that have no supporting value in var2."""
    revised = False

    for value1 in list(domains[var1]):
        supported = any(
            csp.is_allowed(var1, value1, var2, value2)
            for value2 in domains[var2]
        )

        if not supported:
            remove_value(var1, value1)
            revised = True

    return revised


def ac3(csp, domains, remove_value, initial_arcs):
    """Run AC-3 starting from the supplied directed arcs."""
    queue = deque(initial_arcs)

    while queue:
        var1, var2 = queue.popleft()

        if revise(csp, domains, remove_value, var1, var2):
            if not domains[var1]:
                return False

            for neighbor in csp.neighbors[var1]:
                if neighbor != var2:
                    queue.append((neighbor, var1))

    return True


def all_arcs(csp):
    """Return every directed arc in the constraint graph."""
    return [
        (var1, var2)
        for var1 in csp.neighbors
        for var2 in csp.neighbors[var1]
    ]


def arcs_into(csp, var, assignment):
    """Initial arcs for MAC after assigning var: (neighbor, var)."""
    return [
        (neighbor, var)
        for neighbor in csp.neighbors[var]
        if neighbor not in assignment
    ]
