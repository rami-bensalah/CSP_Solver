class CSPInstance:
    """A binary CSP represented by domains and allowed value pairs."""

    def __init__(self, domains, constraints):
        # Keep a private copy so callers' original domain sets are not mutated.
        self.initial_domains = {
            var: set(domain) for var, domain in domains.items()
        }
        self.domains = {
            var: set(domain) for var, domain in domains.items()
        }
        self.num_variables = len(self.domains)

        # constraints[(var1, var2)] is a set of allowed (value1, value2) pairs.
        self.constraints = {
            (var1, var2): set(pairs)
            for (var1, var2), pairs in constraints.items()
        }

        self.neighbors = {var: set() for var in self.domains}
        self.relation = {}

        for (var1, var2), pairs in self.constraints.items():
            if var1 not in self.domains or var2 not in self.domains:
                raise ValueError(f"Constraint refers to unknown variable: {(var1, var2)}")

            self.neighbors[var1].add(var2)
            self.neighbors[var2].add(var1)

            self.relation[(var1, var2)] = pairs
            self.relation[(var2, var1)] = {
                (value2, value1) for value1, value2 in pairs
            }

    def is_allowed(self, var1, value1, var2, value2):
        """Return True if the value pair satisfies the binary constraint."""
        relation = self.relation.get((var1, var2))

        # No constraint between these variables means every pair is allowed.
        if relation is None:
            return True

        return (value1, value2) in relation

    def reset_domains(self):
        """Restore the original domains."""
        self.domains = {
            var: set(domain)
            for var, domain in self.initial_domains.items()
        }
