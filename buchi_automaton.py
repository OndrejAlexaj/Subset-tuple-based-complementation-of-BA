from dataclasses import dataclass

@dataclass
class BuchiAutomaton:
    states: set
    alphabet: set
    transition: list    # looks like [[q0,a,{q1,q2}], [q1,b,{q0,q3}], ...]
    initial: set
    accepting: set