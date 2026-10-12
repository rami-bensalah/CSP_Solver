import time

from heuristics.variable_ordering import select_variable
from heuristics.value_ordering import order_values
from propagation.forward_checking import forward_check
from propagation.ac3 import ac3, all_arcs, arcs_into
from search.backtracking import backtrack
from search.trail import Trail


class SearchTimeout(Exception):
    """Raised when the CSP search exceeds its time limit."""


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

    Time limit:
      - time_limit: maximum solving time in seconds, or None for no limit

    Result status:
      - SAT: a solution was found
      - UNSAT: the CSP was proved unsatisfiable
      - UNKNOWN: the search timed out
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
        time_limit=None,
    ):
        if time_limit is not None and time_limit <= 0:
            raise ValueError("time_limit must be positive or None.")

        self.csp = csp
        self.use_forward_checking = use_forward_checking
        self.use_mac = use_mac
        self.use_full_ac3 = use_full_ac3
        self.use_mrv = use_mrv
        self.use_degree = use_degree
        self.use_lcv = use_lcv
        self.time_limit = time_limit

        self.assignment = {}
        self.nodes_explored = 0
        self.backtracks = 0
        self.trail = Trail(self.csp.domains)

        self.start_time = None
        self.elapsed_time = 0.0
        self.timed_out = False
        self.status = None

    def check_timeout(self):
        """Raise SearchTimeout if the time limit has been reached."""
        if self.start_time is None:
            return

        if self.time_limit is None:
            return

        if time.monotonic() - self.start_time >= self.time_limit:
            raise SearchTimeout

    def is_complete(self):
        return len(self.assignment) == self.csp.num_variables

    def is_consistent(self, var, value):
        """Check the proposed value against already-assigned neighbors."""
        self.check_timeout()

        for neighbor in self.csp.neighbors[var]:
            self.check_timeout()

            if neighbor in self.assignment:
                if not self.csp.is_allowed(
                    var,
                    value,
                    neighbor,
                    self.assignment[neighbor],
                ):
                    return False

        return True

    def assign_value(self, var, value):
        """Restrict var's domain to {value}, recording removals on the trail."""
        self.check_timeout()

        for other_value in list(self.csp.domains[var]):
            self.check_timeout()

            if other_value != value:
                self.trail.remove_value(var, other_value)

    def run_full_ac3(self):
        """Run AC-3 over all arcs."""
        self.check_timeout()

        return ac3(
            self.csp,
            self.csp.domains,
            self.trail.remove_value,
            all_arcs(self.csp),
            check_timeout=self.check_timeout,
        )

    def run_incremental_ac3(self, var):
        """Run incremental AC-3 after assigning var."""
        self.check_timeout()

        return ac3(
            self.csp,
            self.csp.domains,
            self.trail.remove_value,
            arcs_into(self.csp, var, self.assignment),
            check_timeout=self.check_timeout,
        )

    def propagate(self, var, value):
        """Apply the selected propagation methods after var=value."""
        self.check_timeout()

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

        self.check_timeout()

        if self.use_mac and not self.run_incremental_ac3(var):
            return False

        return True

    def solve(self):
        """Solve the CSP, returning an assignment or None.

        Check self.status to distinguish SAT, UNSAT, and UNKNOWN.
        """
        self.csp.reset_domains()
        self.assignment = {}
        self.nodes_explored = 0
        self.backtracks = 0
        self.trail = Trail(self.csp.domains)

        self.start_time = time.monotonic()
        self.elapsed_time = 0.0
        self.timed_out = False
        self.status = None

        try:
            self.check_timeout()

            # MAC includes an initial full AC-3 pass before search.
            if self.use_mac and not self.run_full_ac3():
                self.status = "UNSAT"
                return None

            if backtrack(self):
                self.status = "SAT"
                return self.assignment.copy()

            self.status = "UNSAT"
            return None

        except SearchTimeout:
            self.timed_out = True
            self.status = "UNKNOWN"
            return None

        finally:
            self.elapsed_time = time.monotonic() - self.start_time