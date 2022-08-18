from dataclasses import dataclass

@dataclass
class BuchiAutomaton: # Example:
    states: set       # {"state1","state2",...}
    alphabet: set     # {"a1","a2",...}
    transition: dict  # {"state1":{"a1":{"state3","state4"},"a2":{"state1"}}, ...}
    initial: str      # ""state1""
    accepting: set        # {"state1", "state2", ...}