from dataclasses import dataclass

@dataclass
class BuchiAutomaton:
    states: set
    alphabet: set
    transition: dict   
    initial: str
    final: set