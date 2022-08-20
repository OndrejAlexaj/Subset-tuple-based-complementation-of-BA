from enum import auto
from buchi_automaton import *
from input import *

def union(ba_1, ba_2):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set())

    # if we assume that the names of the states differ
    automaton.states = (ba_1.states).union(ba_2.states)
    (automaton.states).add("new")

    automaton.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    automaton.initial = "new"    # hardcoded name of initial state
    automaton.accepting = (ba_1.accepting).union(ba_2.accepting)

    automaton.transition = (ba_1.transition).copy()
    (automaton.transition).update(ba_2.transition)
    for in_symbol in ba_1.transition[ba_1.initial]:
        for state in ba_1.transition[ba_1.initial][in_symbol]:
            mark_transition(automaton, ["new",in_symbol,state])
    
    for in_symbol in ba_2.transition[ba_2.initial]:
        for state in ba_2.transition[ba_2.initial][in_symbol]:
            mark_transition(automaton, ["new",in_symbol,state])
    
    complete_automaton(automaton)

    return automaton