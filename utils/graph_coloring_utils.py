import matplotlib.pyplot as plt 
import networkx as nx
def read_dimacs_graph(filename):
    """
    Read a graph-coloring instance in DIMACS .col format.

    ```
    Parameters
    ----------
    filename : str
        Path to the DIMACS .col file.

    Returns
    -------
    n_vertices : int
        Number of vertices.
    edges : list[tuple[int, int]]
        List of edges, using zero-based vertex indices.
    """
    n_vertices = None
    declared_edges = None
    edges = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Ignore blank lines and comments
            if not line or line.startswith("c"):
                continue

            parts = line.split()

            if parts[0] == "p":
                if len(parts) != 4 or parts[1] != "edge":
                    raise ValueError(
                        f"Invalid problem declaration at line {line_number}: {line}"
                    )

                if n_vertices is not None:
                    raise ValueError("Multiple problem declarations found.")

                n_vertices = int(parts[2])
                declared_edges = int(parts[3])

                if n_vertices < 0 or declared_edges < 0:
                    raise ValueError("The number of vertices and edges must be non-negative.")

            elif parts[0] == "e":
                if len(parts) != 3:
                    raise ValueError(
                        f"Invalid edge declaration at line {line_number}: {line}"
                    )

                if n_vertices is None:
                    raise ValueError("The problem declaration must appear before edges.")

                u = int(parts[1]) - 1
                v = int(parts[2]) - 1

                if not (0 <= u < n_vertices and 0 <= v < n_vertices):
                    raise ValueError(
                        f"Vertex index out of range at line {line_number}: {line}"
                    )

                if u == v:
                    raise ValueError(
                        f"Self-loop found at line {line_number}: {line}"
                    )

                # Store edges consistently and avoid duplicates
                edges.add((min(u, v), max(u, v)))

            else:
                raise ValueError(
                    f"Unknown declaration at line {line_number}: {line}"
                )

    if n_vertices is None:
        raise ValueError("No problem declaration found.")

    if len(edges) != declared_edges:
        raise ValueError(
            f"Expected {declared_edges} distinct edges, "
            f"but read {len(edges)}."
        )

    return n_vertices, sorted(edges)

def graph_to_csp(n_vertices, edges, k, break_symmetry=False):
    """
    Convert a graph-coloring instance into a binary CSP.

    Parameters
    ----------
    n_vertices : int
        Number of vertices in the graph.
    edges : iterable[tuple[int, int]]
        Edges using zero-based vertex indices.
    k : int
        Number of available colors.
    break_symmetry : bool, default=False
        If True, fix the first vertex to color 0 to break
        color-permutation symmetry.

    Returns
    -------
    CSPInstance
        A CSP representing the graph-coloring problem.
    """
    if n_vertices < 0:
        raise ValueError("The number of vertices must be non-negative.")

    if k < 1:
        raise ValueError("The number of colors must be at least 1.")

    # Create one variable per vertex.
    domains = {
        v: set(range(k))
        for v in range(n_vertices)
    }

    # Break color-permutation symmetry by fixing vertex 0.
    if break_symmetry and n_vertices > 0:
        domains[0] = {0}

    # Every edge requires its endpoints to have different colors.
    allowed_pairs = {
        (color_u, color_v)
        for color_u in range(k)
        for color_v in range(k)
        if color_u != color_v
    }

    constraints = {}

    for u, v in edges:
        if not (0 <= u < n_vertices and 0 <= v < n_vertices):
            raise ValueError(f"Invalid edge: {(u, v)}")

        if u == v:
            raise ValueError(f"Self-loop found at vertex {u}")

        constraints[(u, v)] = allowed_pairs

    return domains, constraints



def visualize_coloring(n_vertices, edges, solution, title="Graph Coloring"):
    """
    Visualize a graph with vertices colored according to a CSP solution.

    Parameters
    ----------
    n_vertices : int
        Number of vertices.
    edges : iterable[tuple[int, int]]
        Graph edges using zero-based vertex indices.
    solution : dict
        Mapping {vertex: color} returned by the CSP solver.
    title : str
        Title of the visualization.
    """
    if solution is None:
        print("No solution to visualize.")
        return

    graph = nx.Graph()
    graph.add_nodes_from(range(n_vertices))
    graph.add_edges_from(edges)

    # Use a force-directed layout.
    # A fixed seed makes the layout reproducible.
    pos = nx.spring_layout(graph, seed=42)

    # Get each vertex's color from the solution.
    node_colors = [solution[v] for v in graph.nodes()]

    plt.figure(figsize=(12, 9))

    nx.draw_networkx(
        graph,
        pos=pos,
        node_color=node_colors,
        cmap=plt.cm.tab20,
        vmin=0,
        vmax=max(node_colors, default=0) if len(set(node_colors)) > 20 else None,
        with_labels=True,
        node_size=500 if n_vertices <= 50 else 100,
        font_size=9 if n_vertices <= 50 else 5,
        edge_color="gray",
        width=0.7,
    )

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()