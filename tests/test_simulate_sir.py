import networkx as nx
from simulate_sir import simulate_sir, counts_per_timestep


def test_spread_direction_path_graph():
    """
    Path graph 1 - 2 - 3. Node 1 starts infected.
    Node 3 is only reachable through node 2, so node 3 must not become
    infected before node 2 does. beta=1.0, gamma=0.0 makes this deterministic.
    """
    g = nx.path_graph([1, 2, 3])  # edges: (1,2), (2,3)

    history = simulate_sir(g, beta=1.0, gamma=0.0, timesteps=3,
                            initial_infected=[1], seed=0)

    # t=0: only node 1 infected
    assert history[0] == {1: 'I', 2: 'S', 3: 'S'}

    # t=1: infection reaches node 2 (direct neighbor of 1), NOT node 3 yet
    assert history[1][1] == 'I'
    assert history[1][2] == 'I'
    assert history[1][3] == 'S', "node 3 infected too early — one-hop-per-step violated"

    # t=2: infection now reaches node 3, via node 2
    assert history[2][3] == 'I'

    # Sanity: infection count is non-decreasing since gamma=0
    counts = counts_per_timestep(history)
    infected_over_time = [c['I'] for c in counts]
    assert infected_over_time == sorted(infected_over_time), \
        "infected count should never decrease when gamma=0"

    print("PASSED: spread direction test")


if __name__ == "__main__":
    test_spread_direction_path_graph()
