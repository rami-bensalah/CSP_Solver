from csp import CSPInstance, CSPSolver
from utils.graph_coloring_utils import (
    read_dimacs_graph,
    graph_to_csp,
    visualize_coloring,
)

from search.sequential_search import sequential_search
from search.binary_search import binary_search


# ============================================================
# Configuration
# ============================================================

filename = "Problems/instances/myciel5.col"

# Choose: "fixed", "sequential", or "binary"
search_method = "binary"

# Used only when search_method == "fixed"
k = 31

# Used for sequential and binary search
lower_bound = 1
upper_bound = None  # None means n_vertices

solver_options = {
    "use_forward_checking": False,
    "use_mac": True,
    "use_full_ac3": False,
    "use_mrv": True,
    "use_degree": True,
    "use_lcv": True,
    "time_limit": 300,
}


# ============================================================
# Load graph
# ============================================================

n_vertices, edges = read_dimacs_graph(filename)

print("Number of vertices:", n_vertices)
print("Number of edges:", len(edges))

if n_vertices == 0:
    raise ValueError("The graph must contain at least one vertex.")

if upper_bound is None:
    upper_bound = n_vertices


# ============================================================
# Factory: create a CSP solver for a given number of colors
# ============================================================

def coloring_solver_factory(k):
    domains, constraints = graph_to_csp(
        n_vertices,
        edges,
        k,
    )

    csp = CSPInstance(domains, constraints)

    return CSPSolver(csp, **solver_options)


# ============================================================
# Run selected strategy
# ============================================================

if search_method == "fixed":

    solver = coloring_solver_factory(k)
    solution = solver.solve()

    result = {
        "status": solver.status,
        "candidate": k if solver.status == "SAT" else None,
        "solution": solution,
        "tested": [{
            "candidate": k,
            "status": solver.status,
            "elapsed_time": solver.elapsed_time,
            "nodes_explored": solver.nodes_explored,
            "backtracks": solver.backtracks,
        }],
    }

elif search_method == "sequential":

    result = sequential_search(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        solver_factory=coloring_solver_factory,
        objective="min",
    )

elif search_method == "binary":

    result = binary_search(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        solver_factory=coloring_solver_factory,
        objective="min",
    )

else:
    raise ValueError(
        "search_method must be 'fixed', 'sequential', or 'binary'."
    )


# ============================================================
# Display results
# ============================================================

print("\n========== SEARCH RESULTS ==========")
print("Search method:", search_method)
print("Status:", result["status"])
print("Number of colors:", result["candidate"])

tested = result["tested"]

print("Candidates tested:", len(tested))
print(
    "Total elapsed time:",
    sum(item["elapsed_time"] for item in tested),
    "seconds",
)
print(
    "Total nodes explored:",
    sum(item["nodes_explored"] for item in tested),
)
print(
    "Total backtracks:",
    sum(item["backtracks"] for item in tested),
)

for item in tested:
    print(
        f"k={item['candidate']:>3} | "
        f"status={item['status']:<7} | "
        f"time={item['elapsed_time']:.3f}s | "
        f"nodes={item['nodes_explored']} | "
        f"backtracks={item['backtracks']}"
    )


# ============================================================
# Visualize only when a solution is available
# ============================================================

if result["solution"] is not None:
    visualize_coloring(
        n_vertices,
        edges,
        result["solution"],
        title=f"Graph Coloring with {result['candidate']} Colors",
    )
else:
    print("\nNo solution is available to visualize.")