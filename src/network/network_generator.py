"""
Network Generator Module

Generates different network types used in the project.
"""

from .random_network import generate_random_network
from .small_world_network import generate_small_world_network


def generate_network(network_type, n_nodes, params):
    """
    Generates a network graph.

    Parameters:
        network_type (str): Type of graph.
        n_nodes (int): Number of nodes.
        params (dict): Parameters required.

    Returns:
        NetworkX Graph
    """

    if network_type == "random":

        if "p" not in params:
            raise ValueError("Random graph requires parameter 'p'.")

        return generate_random_network(
            n_nodes,
            params["p"]
        )

    elif network_type == "small_world":

        if "k" not in params or "p" not in params:
            raise ValueError(
                "Small-World graph requires parameters 'k' and 'p'."
            )

        return generate_small_world_network(
            n_nodes,
            params["k"],
            params["p"]
        )

    else:
        raise ValueError(
            "Supported network types are 'random' and 'small_world'."
        )