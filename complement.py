from buchi_automaton import *
from edit_BA import *

def init_visited(automaton):
    visited = dict()
    for state in automaton.states:
        visited[state] = False

    return visited

def determinise(automaton,interim_automaton,prev_state,contained_states):
    succ_tmp, acc_states, new_states = set(), set(), set()
    tmp_states = []
    original_len = len(interim_automaton.states)
    visited = init_visited(automaton)
    
    for symbol in interim_automaton.alphabet:
        for states_set in reversed(range(len(prev_state))):
            for state in prev_state[states_set]:
                for succ in automaton.transition[state][symbol]:
                    if succ in automaton.accepting:
                        if not visited[succ]:
                            acc_states.add(succ)
                            visited[succ] = True
                    else:
                        if not visited[succ]:
                            succ_tmp.add(succ)
                            visited[succ] = True
            if len(acc_states)!=0:
                tmp_states.append(frozenset(acc_states))
            if len(succ_tmp)!=0:
                tmp_states.append(frozenset(succ_tmp))           
            acc_states = set()
            succ_tmp = set()

        if len(tmp_states)!=0:
            interim_automaton.states.add(tuple(reversed(tmp_states)))
            mark_transition(interim_automaton,[prev_state,symbol,tuple(reversed(tmp_states))])
            new_states.add(tuple(reversed(tmp_states)))

        tmp_states = []
        visited = init_visited(automaton)

    if original_len!=len(interim_automaton.states):
        for state in new_states:
            interim_automaton = determinise(automaton,interim_automaton,state,contained_states)
            
    
    return interim_automaton


def complement(automaton):
    automaton = complete_automaton(automaton)

    interim_automaton = BuchiAutomaton(set(),set(),dict(),"",set())
    interim_automaton.alphabet = automaton.alphabet
    interim_automaton.initial = (frozenset({automaton.initial}),)
    interim_automaton.states.add(interim_automaton.initial)

    interim_automaton = determinise(automaton,interim_automaton,interim_automaton.initial,contained_states)

    return interim_automaton
