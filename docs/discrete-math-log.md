## Week 2 — The Discrete-Time SIR Update as a Formal Dynamical System

The SIR simulation implemented this week can be described formally as a
discrete-time dynamical system.

**State:** At each timestep `t`, the system state is a function
`state_t : V → {S, I, R}`, assigning one of three states to every node
`v` in the network `V`.

**Transition function:** The state at `t+1` is produced from the state at
`t` by a transition function applied independently to each node:

- If `state_t(v) = S`: for each infected neighbor `u ∈ N(v)`, node `v`
  transitions to `I` with probability `β` (independently per neighbor).
- If `state_t(v) = I`: node `v` transitions to `R` with probability `γ`,
  otherwise remains `I`.
- If `state_t(v) = R`: node `v` remains `R` (absorbing state).

This is a stochastic, node-level Markov process: each node's next state
depends only on its own current state and the current states of its
graph neighbors (not on the full history), and transitions are governed
by fixed probabilities `β` and `γ`.

**Group membership as a modifier:** When `transmission_mode="group"` is
introduced (planned for a later module), group membership acts as a
modification to the transition rule for susceptible nodes — infection
risk becomes a function not just of individual infected neighbors, but
of the *fraction* of a node's group currently infected. Formally, this
extends the transition function's input from `N(v)` (graph neighbors)
to `N(v) ∪ G(v)` (graph neighbors and group co-members), with a
different (typically higher) effective transmission weight applied
within the group subset — group membership itself can be viewed as an
additional subset relation layered on top of the base graph structure.