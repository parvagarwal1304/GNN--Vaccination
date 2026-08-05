import networkx as nx


def generate_small_world_network(n_nodes, k, p):
    """
    Generates a Small-World (Watts-Strogatz) network.

    Parameters:
        n_nodes (int): Number of nodes.
        k (int): Number of nearest neighbours.
        p (float): Rewiring probability.

    Returns:
        NetworkX Graph
    """

    if n_nodes <= 0:
        raise ValueError("Number of nodes must be greater than 0.")

    if k >= n_nodes:
        raise ValueError("k must be smaller than number of nodes.")

    if not (0 <= p <= 1):
        raise ValueError("Probability 'p' must be between 0 and 1.")

    return nx.watts_strogatz_graph(
        n_nodes,
        k,
        p
    )