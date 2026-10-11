class Trail:
    """Record domain removals so they can be undone after a failed branch."""

    def __init__(self, domains):
        self.domains = domains
        self.changes = []

    def position(self):
        return len(self.changes)

    def remove_value(self, var, value):
        """Remove value and record it; return True only if removed."""
        if value not in self.domains[var]:
            return False

        self.domains[var].remove(value)
        self.changes.append((var, value))
        return True

    def restore(self, position):
        """Undo all removals made after the given trail position."""
        while len(self.changes) > position:
            var, value = self.changes.pop()
            self.domains[var].add(value)
