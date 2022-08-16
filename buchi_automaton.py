from dataclasses import dataclass

@dataclass
class BuchiAutomaton:
    states: set
    alphabet: set
    transition: set
    initial: set
    accepting: set