import networkx as nx


def generate_random_network(n_nodes, p):
    """
    Generates a Random (Erdos-Renyi) network.

    Parameters:
        n_nodes (int): Number of nodes.
        p (float): Probability of edge creation.

    Returns:
        NetworkX Graph
    """

    if n_nodes <= 0:
        raise ValueError("Number of nodes must be greater than 0.")

    if not (0 <= p <= 1):
        raise ValueError("Probability 'p' must be between 0 and 1.")

    return nx.erdos_renyi_graph(n_nodes, p)