from heuristics.variable_ordering import select_variable
from heuristics.value_ordering import order_values
from propagation.forward_checking import forward_check
from propagation.ac3 import ac3, all_arcs, arcs_into
from search.backtracking import backtrack
from search.trail import Trail


class CSPSolver:
    """Backtracking solver for binary CSPs.

    Propagation options:
      - use_forward_checking: one-step forward checking after an assignment
      - use_mac: full AC-3 before search, then incremental AC-3 after assignments
      - use_full_ac3: run AC-3 over all arcs at each search node

    Heuristics:
      - use_mrv: minimum remaining values
      - use_degree: degree tie-breaker (or degree alone if MRV is disabled)
      - use_lcv: least-constraining value ordering
    """

    def __init__(
        self,
        csp,
        use_forward_checking=False,
        use_mac=False,
        use_full_ac3=False,
        use_mrv=False,
        use_degree=False,
        use_lcv=False,
    ):
        self.csp = csp
        self.use_forward_checking = use_forward_checking
        self.use_mac = use_mac
        self.use_full_ac3 = use_full_ac3
        self.use_mrv = use_mrv
        self.use_degree = use_degree
        self.use_lcv = use_lcv

        self.assignment = {}
        self.nodes_explored = 0
        self.backtracks = 0
        self.trail = Trail(self.csp.domains)

    def is_complete(self):
        return len(self.assignment) == self.csp.num_variables

    def is_consistent(self, var, value):
        """Check the proposed value against already-assigned neighbors."""
        for neighbor in self.csp.neighbors[var]:
            if neighbor in self.assignment:
                if not self.csp.is_allowed(
                    var, value, neighbor, self.assignment[neighbor]
                ):
                    return False
        return True

    def assign_value(self, var, value):
        """Restrict var's domain to {value}, recording removals on the trail."""
        for other_value in list(self.csp.domains[var]):
            if other_value != value:
                self.trail.remove_value(var, other_value)

    def run_full_ac3(self):
        return ac3(
            self.csp,
            self.csp.domains,
            self.trail.remove_value,
            all_arcs(self.csp),
        )

    def run_incremental_ac3(self, var):
        return ac3(
            self.csp,
            self.csp.domains,
            self.trail.remove_value,
            arcs_into(self.csp, var, self.assignment),
        )

    def propagate(self, var, value):
        """Apply the selected propagation methods after var=value."""
        if self.use_forward_checking:
            if not forward_check(
                self.csp,
                self.assignment,
                self.csp.domains,
                self.trail.remove_value,
                var,
                value,
            ):
                return False

        if self.use_mac and not self.run_incremental_ac3(var):
            return False

        return True

    def solve(self):
        """Solve the CSP, returning an assignment or None if unsatisfiable."""
        self.csp.reset_domains()
        self.assignment = {}
        self.nodes_explored = 0
        self.backtracks = 0
        self.trail = Trail(self.csp.domains)

        # MAC includes an initial full AC-3 pass before search.
        if self.use_mac and not self.run_full_ac3():
            self.trail.restore(0)
            return None

        if backtrack(self):
            return self.assignment.copy()

        return None
