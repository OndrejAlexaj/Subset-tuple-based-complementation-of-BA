from enum import auto
from buchi_automaton import *
from input import *  

# source:
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
# section - The algorithm in pseudocode
def tarjan(automaton):
    global index
    index = 0
    sccs, stack = [], []
    indices, lowlinks, on_stack = dict(), dict(), dict()

    for v in automaton.states:
        indices[v] = -1
        on_stack[v] = False
    
    def strongconnect(v):
        global index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for succ in automaton.transition[v].values(): # it is guaranteed that this cycle is performed
            for w in succ:                            # just once (just one set of successors)
                if indices[w] == -1:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v],lowlinks[w])
                elif on_stack[w]:
                    lowlinks[v] = min(lowlinks[v],indices[w])
        
        if lowlinks[v] == indices[v]:
            tmp = set()
            while True:
                w = stack.pop()
                on_stack[w] = False
                tmp.add(w)
                if(w == v):
                    break
            sccs.append(tmp)

    # in pseudocode this part is above the strongconnect(),
    # but to make it run it needs to be after definition
    for v in automaton.states:
        if indices[v] == -1:
            strongconnect(v)

    return sccs

# function returns array of sccs which contain accepting state
def with_accepting(automaton,sccs):
    new_sccs = []

    # Setting values in dictionary to easily
    # distinguish between accepting and non-accepting
    # states. Runs in linear time since each state is 
    # "touched" at most twice
    states_appearance = dict()
    for state in automaton.states:
        states_appearance[state] = False 
    for state in automaton.accepting:
        states_appearance[state] = True

    # these nested for loops run in linear time
    # since each state is "touched" at most once
    # and "if" condition is O(1) thanks to dictionary
    for component in sccs:
        for state in component:
            if states_appearance[state]:
                new_sccs.append(component)
                break
    
    return new_sccs

def dfs(automaton,from_state,was_in):
    for succ in automaton.transition[from_state].values():
        for state in succ:
            if not was_in[state]:
                was_in[state] = True
                was_in = dfs(automaton,state,was_in)
    return was_in

def reachable_from(automaton,sccs,from_state):
    was_in = dict()
    new_sccs = []

    for state in automaton.states:
        was_in[state] = False

    was_in = dfs(automaton,from_state,was_in)
    for component in sccs:
        for state in component:
            if was_in[state]:
                new_sccs.append(component)
                break

    return new_sccs

# returns True if given automaton doesn't recognize
# any language, False otherwise
def empty(automaton):
    sccs = tarjan(automaton)   
    sccs = with_accepting(automaton,sccs)
    sccs = reachable_from(automaton,sccs,automaton.initial)
    
    # looking for non-trivial (having some successor)
    for component in sccs:
        for state in component:
            if automaton.transition[state] is not None:
                return False
    return True