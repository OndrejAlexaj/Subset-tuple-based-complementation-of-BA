from buchi_automaton import *


# function returns automaton with added transition which is given in form [state1,a,state2]
def mark_transition(automaton, new_transition):
    if(automaton.transition.get(new_transition[0]) is not None):
        if (automaton.transition[new_transition[0]]).get(new_transition[1]) is not None:
            (automaton.transition[new_transition[0]][new_transition[1]]).add(new_transition[2])
        else:
            automaton.transition[new_transition[0]][new_transition[1]] = {new_transition[2]}
    else:
        automaton.transition[new_transition[0]] = {new_transition[1]:{new_transition[2]}}

    return automaton

# returns complete automaton
def complete_automaton(automaton):
    used_sink = "sink" in automaton.states

    for state in automaton.states:
        if automaton.transition.get(state) is None:
            for symbol in automaton.alphabet:
                mark_transition(automaton,[state,symbol,"sink"])
                used_sink = True
        else:
            for symbol in automaton.alphabet:
                if automaton.transition[state].get(symbol) is None:
                    mark_transition(automaton,[state,symbol,"sink"])
                    used_sink = True
    
    if used_sink:
        automaton.states.add("sink")
        for symbol in automaton.alphabet:
            mark_transition(automaton,["sink",symbol,"sink"])

    return automaton

# removes states which cannot be reached
def remove_dead_states(automaton):
    tmp_states = automaton.states.copy()
    tmp_transition = automaton.transition.copy()

    for state in automaton.states:
        ok = False
        for k in automaton.transition.values():
            for j in k.values():
                if state in j:
                    ok = True
                    break
        if not ok and state!=automaton.initial:
            tmp_states.remove(state)
            tmp_transition.pop(state)
    
    automaton.states = tmp_states.copy()
    automaton.transition = tmp_transition.copy()
    
    return automaton