# Counter FSM Integration

## Purpose

The MOD-5 counter works as a synchronous finite state machine.

It uses three D flip-flops to store the current state:

- Q2
- Q1
- Q0

## Clock

All three flip-flops receive the same clock signal.

Therefore, all state changes happen synchronously on the clock edge.

## State Sequence

The FSM follows:

000 → 001 → 010 → 011 → 100 → 000

## Terminal Count

The terminal count signal is generated at state 100.

TC = Q2 · Q1' · Q0'

When the counter reaches 100:

TC = 1

After the next clock pulse, the FSM returns to 000.

## Reset / Handoff

The counter returns to the initial state 000 after reaching the terminal count.

This allows the counter to operate continuously as a MOD-5 counter.

## CircuitVerse Verification

The circuit was simulated in CircuitVerse and the expected state sequence was observed successfully.