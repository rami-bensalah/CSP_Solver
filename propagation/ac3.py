
from collections import deque


def revise(csp, domains, remove_value, var1, var2, check_timeout=None):
    """Remove values from var1 that have no supporting value in var2."""
    revised = False

    for value1 in list(domains[var1]):
        if check_timeout is not None:
            check_timeout()

        supported = False

        for value2 in domains[var2]:
            if check_timeout is not None:
                check_timeout()

            if csp.is_allowed(var1, value1, var2, value2):
                supported = True
                break

        if not supported:
            remove_value(var1, value1)
            revised = True

    return revised


def ac3(csp, domains, remove_value, initial_arcs, check_timeout=None):
    """Run AC-3 starting from the supplied directed arcs.

    Args:
        csp: The CSP instance.
        domains: Current variable domains.
        remove_value: Function used to remove a value and record it on the trail.
        initial_arcs: Initial directed arcs to process.
        check_timeout: Optional callback that raises an exception on timeout.
    """
    queue = deque(initial_arcs)

    while queue:
        if check_timeout is not None:
            check_timeout()

        var1, var2 = queue.popleft()

        if revise(
            csp,
            domains,
            remove_value,
            var1,
            var2,
            check_timeout=check_timeout,
        ):
            if not domains[var1]:
                return False

            for neighbor in csp.neighbors[var1]:
                if check_timeout is not None:
                    check_timeout()

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

