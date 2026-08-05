import networkx as nx
import random


def generate_scale_free_network(n_nodes, m=3, seed=None):
    """
    Generates a scale-free network using the Barabasi-Albert model.
    n_nodes: number of people (nodes) in the network
    m: number of edges each new node forms when added (controls density)
    """
    graph = nx.barabasi_albert_graph(n=n_nodes, m=m, seed=seed)
    return graph


def assign_groups(graph, group_size=4, seed=None):
    """
    Splits the network's nodes into small groups (e.g. households/classrooms)
    for higher-order (group-based) transmission modeling later.
    Returns a dict: {group_id: [list of node ids]}
    """
    rng = random.Random(seed)
    nodes = list(graph.nodes())
    rng.shuffle(nodes)

    groups = {}
    group_id = 0
    for i in range(0, len(nodes), group_size):
        groups[group_id] = nodes[i:i + group_size]
        group_id += 1

    return groups


if __name__ == "__main__":
    # Quick manual test — run this file directly to sanity check
    g = generate_scale_free_network(n_nodes=100, m=3, seed=42)
    print(f"Generated scale-free network: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")

    groups = assign_groups(g, group_size=4, seed=42)
    print(f"Created {len(groups)} groups")
    print(f"Example group: {groups[0]}")