from enum import auto
from buchi_automaton import *
from itertools import product

from edit_BA import complete_automaton

# returns automaton with new transitions
# param. "state" is tuple (Q1,R2,copy) 
# where Q1 is from ba_1 states and R2 from ba_2 ...
# copy indicates in which copy we are
def update_transitions(automaton,ba_1,ba_2,in_copy,state,symbol):
    if in_copy == 1:
        curr_automaton = ba_1
    else:
        curr_automaton = ba_2

    if (state[in_copy-1] not in curr_automaton.accepting):
        next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{in_copy})
        if(automaton.transition.get(state) is None):
            automaton.transition[state] = {symbol:set(next_states)}
        else:
            automaton.transition[state][symbol] = set(next_states)
    else:
        next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{3-in_copy})
        if(automaton.transition.get(state) is None):
                automaton.transition[state] = {symbol:set(next_states)}
        else:
            automaton.transition[state][symbol] = set(next_states)
    
    return automaton

def intersection(ba_1, ba_2):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set())

    ba_1.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    complete_automaton(ba_1)
    ba_2.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    complete_automaton(ba_2)
    automaton.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    automaton.states = set(product(ba_1.states,ba_2.states,{1,2}))
    automaton.initial = (ba_1.initial,ba_2.initial,1) 
    automaton.accepting = set(product(ba_1.states,ba_2.accepting,{2}))

    for state in automaton.states:
        for symbol in automaton.alphabet:
            in_copy = state[2]
            automaton = update_transitions(automaton,ba_1,ba_2,in_copy,state,symbol)

    return automaton