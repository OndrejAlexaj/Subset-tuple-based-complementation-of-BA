from enum import auto
from buchi_automaton import *
from itertools import product

def intersection(ba_1, ba_2):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set())

    automaton.alphabet = (ba_1.alphabet).union(ba_2.alphabet)
    automaton.states = set(product(ba_1.states,ba_2.states,{'1','2'}))
    automaton.initial = (ba_1.initial,ba_2.initial,'1') 
    automaton.accepting = set(product(ba_1.states,ba_2.accepting,{'2'}))

    for state in automaton.states:
        for symbol in automaton.alphabet:
            if state[2] == 1:
                if (state[0] not in ba_1.accepting):
                        next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{'1'})
                        if(automaton.transition.get(state) is None):
                            automaton.transition[state] = {symbol:set(next_states)}
                        else:
                            automaton.transition[state][symbol] = set(next_states)
                else:
                    next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{'2'})
                    if(automaton.transition.get(state) is None):
                            automaton.transition[state] = {symbol:set(next_states)}
                    else:
                        automaton.transition[state][symbol] = set(next_states)
            else:
                if (state[0] not in ba_2.accepting):
                    next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{'2'})
                    if(automaton.transition.get(state) is None):
                            automaton.transition[state] = {symbol:set(next_states)}
                    else:
                        automaton.transition[state][symbol] = set(next_states)
                else:
                    next_states = product(ba_1.transition[state[0]][symbol],ba_2.transition[state[1]][symbol],{'1'})
                    if(automaton.transition.get(state) is None):
                            automaton.transition[state] = {symbol:set(next_states)}
                    else:
                        automaton.transition[state][symbol] = set(next_states)
    return automaton