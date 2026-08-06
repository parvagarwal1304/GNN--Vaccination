import networkx as nx
import matplotlib.pyplot as plt


def draw_network(G, title="Network", node_color_by_degree=True, save_path=None):
    """
    Draws a NetworkX graph with nodes sized/colored sensibly.
    """
    pos = nx.spring_layout(G, seed=42)

    if node_color_by_degree:
        degrees = dict(G.degree())
        node_colors = [degrees[n] for n in G.nodes()]
        node_sizes = [50 + degrees[n] * 10 for n in G.nodes()]
    else:
        node_colors = "lightblue"
        node_sizes = 100

    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        cmap=plt.cm.viridis,
        with_labels=False,
        edge_color="gray",
        alpha=0.8
    )
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    plt.show()


def network_stats(G):
    """
    Returns a dict of basic descriptive stats for a network.
    """
    stats = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
        "average_clustering": nx.average_clustering(G),
    }

    if nx.is_connected(G):
        stats["average_path_length"] = nx.average_shortest_path_length(G)
    else:
        stats["average_path_length"] = None
        stats["note"] = "Graph is disconnected; path length computed on largest component instead."
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        stats["average_path_length_largest_component"] = nx.average_shortest_path_length(subgraph)

    return stats


def analyze_network(G, title="Network"):
    """
    Given any network, produces a plot and a printed stats summary.
    """
    stats = network_stats(G)
    print(f"--- {title} ---")
    for key, value in stats.items():
        print(f"{key}: {value}")
    draw_network(G, title=title)
    return stats


if __name__ == "__main__":
    G_test = nx.erdos_renyi_graph(n=30, p=0.1, seed=1)
    analyze_network(G_test, title="Test Network")