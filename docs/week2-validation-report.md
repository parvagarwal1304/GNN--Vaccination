# Week 2 — SIR Simulator Validation Report (Module D)

## What was validated
Module A's `simulate_sir()` function was tested against 6 automated checks
confirming correct epidemic behavior, not just visual inspection.

## Tests

| Test | What it confirms |
|---|---|
| `test_spread_direction_path_graph` | Infection only spreads one hop per timestep, along real edges |
| `test_population_conserved` | S + I + R always equals total node count at every timestep |
| `test_zero_beta_no_spread` | With beta=0, infection never spreads beyond the initial case |
| `test_gamma_one_immediate_recovery` | With gamma=1, infected nodes recover the very next step |
| `test_no_reinfection` | Once a node reaches 'R', it never changes state again |
| `test_epidemic_curve_rises_then_declines` | On a realistic network, infection count rises, peaks, then declines — the expected SIR shape |

## Result
All 6 tests pass. `simulate_sir()` is confirmed to behave correctly and is
safe for the rest of the team to build on for Week 3 (vaccination strategies)
and beyond.

## How to run these tests
```
python tests\test_simulate_sir.py
```