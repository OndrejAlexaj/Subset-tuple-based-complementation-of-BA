from enum import auto
from buchi_automaton import *

def union(ba_1, ba_2):
    automaton = BuchiAutomaton(set(),set(),list(),"",set())

    automaton.states = (ba_1.states).union(ba_2.states)
    (automaton.states).add("ns")

    automaton.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    automaton.initial = "ns"    # hardcoded name of initial state
    automaton.accepting = (ba_1.accepting).union(ba_2.accepting)

    automaton.transition = ba_1.transition + ba_2.transition
    for i in automaton.alphabet:
        tmp = ["ns",i,set()]
        for j in ba_1.transition:
            if j[0]==ba_1.initial and j[1]==i:
                tmp[2] = tmp[2].union(j[2])
        for j in ba_2.transition:
            if j[0]==ba_2.initial and j[1]==i:
                tmp[2] = tmp[2].union(j[2])
        automaton.transition.append(tmp)

    return automaton