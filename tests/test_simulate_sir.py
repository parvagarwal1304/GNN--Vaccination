import networkx as nx
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "network"))

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


def test_population_conserved():
    """S + I + R must always equal total node count — no one disappears."""
    g = nx.erdos_renyi_graph(n=40, p=0.1, seed=1)
    history = simulate_sir(g, beta=0.3, gamma=0.1, timesteps=30, seed=0)
    counts = counts_per_timestep(history)
    total = g.number_of_nodes()
    for t, c in enumerate(counts):
        assert c['S'] + c['I'] + c['R'] == total, \
            f"population not conserved at timestep {t}"
    print("PASSED: population conservation test")


def test_zero_beta_no_spread():
    """With beta=0, infection should never spread beyond the initial case."""
    g = nx.erdos_renyi_graph(n=30, p=0.1, seed=1)
    history = simulate_sir(g, beta=0.0, gamma=0.1, timesteps=20,
                            initial_infected=[0], seed=0)
    counts = counts_per_timestep(history)
    max_infected = max(c['I'] for c in counts)
    assert max_infected <= 1, "infection spread even though beta=0"
    print("PASSED: zero beta no-spread test")


def test_gamma_one_immediate_recovery():
    """With gamma=1, any infected node should recover by the very next timestep."""
    g = nx.erdos_renyi_graph(n=20, p=0.1, seed=1)
    history = simulate_sir(g, beta=0.0, gamma=1.0, timesteps=5,
                            initial_infected=[0], seed=0)
    assert history[0][0] == 'I'
    assert history[1][0] == 'R', "node did not recover immediately with gamma=1"
    print("PASSED: gamma=1 immediate recovery test")


def test_no_reinfection():
    """Once a node reaches 'R', it must never change state again."""
    g = nx.erdos_renyi_graph(n=30, p=0.15, seed=1)
    history = simulate_sir(g, beta=0.4, gamma=0.2, timesteps=30, seed=0)
    for node in g.nodes():
        states_over_time = [snapshot[node] for snapshot in history]
        if 'R' in states_over_time:
            first_r_index = states_over_time.index('R')
            after = states_over_time[first_r_index:]
            assert all(s == 'R' for s in after), \
                f"node {node} left recovered state after reaching R"
    print("PASSED: no reinfection test")


def test_epidemic_curve_rises_then_declines():
    """
    Core validation: on a reasonably connected network with real transmission,
    infection count should rise, peak, then decline — the classic SIR shape.
    """
    g = nx.erdos_renyi_graph(n=100, p=0.08, seed=2)
    history = simulate_sir(g, beta=0.3, gamma=0.1, timesteps=60,
                            initial_infected=[0], seed=1)
    counts = counts_per_timestep(history)
    infected_over_time = [c['I'] for c in counts]

    peak_index = infected_over_time.index(max(infected_over_time))

    assert peak_index > 0, "infection peaked at t=0 — no rise phase observed"
    assert peak_index < len(infected_over_time) - 1, \
        "infection still rising at final timestep — no decline phase observed"
    assert infected_over_time[-1] < max(infected_over_time), \
        "infection did not decline from its peak by the end of the simulation"

    print("PASSED: epidemic curve rise/peak/decline test")
if __name__ == "__main__":
    test_spread_direction_path_graph()
    test_population_conserved()
    test_zero_beta_no_spread()
    test_gamma_one_immediate_recovery()
    test_no_reinfection()
    test_epidemic_curve_rises_then_declines()
   
    