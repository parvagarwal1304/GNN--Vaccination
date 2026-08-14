# MOD-5 Counter State Table and Derivation

## Counter Sequence

The counter follows this sequence:

000 → 001 → 010 → 011 → 100 → 000

Therefore, it is a MOD-5 counter because it has 5 valid states.

## State Table

| Present State | Next State |
|---------------|------------|
| 000 | 001 |
| 001 | 010 |
| 010 | 011 |
| 011 | 100 |
| 100 | 000 |

## State Variables

Q2 = MSB  
Q1 = Middle bit  
Q0 = LSB

## Next-State Equations

D2 = Q1Q0

D1 = Q2'Q0 + Q2Q0'

D0 = Q0'

## Terminal Count

The terminal count is generated when the counter reaches 100.

TC = Q2 · Q1' · Q0'

Therefore:

TC = 1 only when the state is 100.