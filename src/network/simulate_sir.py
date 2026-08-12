"""
EDI Module A — Core Pairwise Transmission Loop
simulate_sir(network, beta, gamma, timesteps)

Network-based, discrete-time, stochastic SIR simulation.
Infection spreads along graph edges only (no homogeneous mixing assumption).
"""

import random
import networkx as nx


def simulate_sir(network, beta, gamma, timesteps, initial_infected=None, seed=None):
    """
    Simulate SIR spread over a networkx graph.

    Parameters
    ----------
    network : networkx.Graph
        The contact network. Nodes = individuals, edges = possible contacts.
    beta : float
        Per-timestep, per-edge probability an infected node infects a
        susceptible neighbor.
    gamma : float
        Per-timestep probability an infected node recovers.
    timesteps : int
        Number of discrete steps to simulate.
    initial_infected : list, optional
        Nodes infected at t=0. Defaults to a single arbitrary node.
    seed : int, optional
        RNG seed for reproducibility (essential for deterministic tests).

    Returns
    -------
    history : list[dict]
        history[t] = {node: state} for t = 0..timesteps.
        state is one of 'S', 'I', 'R'.
    """
    if seed is not None:
        random.seed(seed)

    # 1. Initialize state
    state = {node: 'S' for node in network.nodes()}
    if initial_infected is None:
        initial_infected = [next(iter(network.nodes()))]
    for node in initial_infected:
        state[node] = 'I'

    history = [state.copy()]

    # 2. Step forward
    for _ in range(timesteps):
        new_state = state.copy()  # write into a copy — never mutate `state` mid-loop

        # --- Transmission: driven off last timestep's snapshot ---
        for node in network.nodes():
            if state[node] == 'I':
                for neighbor in network.neighbors(node):
                    if state[neighbor] == 'S' and random.random() < beta:
                        new_state[neighbor] = 'I'

        # --- Recovery: also driven off last timestep's snapshot ---
        for node in network.nodes():
            if state[node] == 'I' and random.random() < gamma:
                new_state[node] = 'R'

        state = new_state
        history.append(state.copy())

    return history


def counts_per_timestep(history):
    """Convenience: turn per-node history into S/I/R counts per timestep."""
    counts = []
    for snapshot in history:
        s = sum(1 for v in snapshot.values() if v == 'S')
        i = sum(1 for v in snapshot.values() if v == 'I')
        r = sum(1 for v in snapshot.values() if v == 'R')
        counts.append({'S': s, 'I': i, 'R': r})
    return counts
