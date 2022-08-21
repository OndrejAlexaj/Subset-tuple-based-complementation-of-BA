from enum import auto
from buchi_automaton import *
from input import *  

# source:
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
# section - The algorithm in pseudocode
# Modified to compute SCCs just from desired state
def tarjan(automaton,from_state):
    end_algo = False
    index = 0
    sccs, stack = [], []
    indices, lowlinks, on_stack = dict(), dict(), dict()

    ##############################################
    # to easily distinguish between accepting
    # and non-accepting states just by their names
    accepting = dict()
    for state in automaton.states:
        accepting[state] = False 
    for state in automaton.accepting:
        accepting[state] = True
    ##############################################

    for v in automaton.states:
        indices[v] = -1
        on_stack[v] = False
    
    def strongconnect(v):
        nonlocal index, end_algo
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        if automaton.transition.get(v) is not None: # to catch if the automaton is not complete
            for succ in automaton.transition[v].values(): # it is guaranteed that this cycle is performed
                for w in succ:                            # just once (just one set of successors)
                    if indices[w] == -1:
                        strongconnect(w)
                        if end_algo: # if we found desired SCC, there is no need to continue in algorithm
                            return
                        lowlinks[v] = min(lowlinks[v],lowlinks[w])
                    elif on_stack[w]:
                        lowlinks[v] = min(lowlinks[v],indices[w])
            
            visited_accepting = False
            if lowlinks[v] == indices[v]:
                tmp = set()
                while True:
                    w = stack.pop()
                    if accepting[w]:
                        visited_accepting = True
                    tmp.add(w)
                    on_stack[w] = False
                    if(w == v):
                        break

                if visited_accepting and not is_trivial(automaton,tmp):
                    sccs.append(tmp)
                    end_algo = True

    # in pseudocode this part is above the strongconnect(),
    # but to make it run it needs to be after definition
    if indices[from_state] == -1:
        strongconnect(from_state)

    return sccs

# returns True if the SCC is trivial, False otherwise
def is_trivial(automaton,component):
    # component which contains only 1 state Q is non-trivial
    # iff there exists edge from Q to Q
    if len(component) == 1:
        for state_1 in component:
            if automaton.transition.get(state_1) is None: # if automaton is not complete
                return False
            for set_of_succ in automaton.transition[state_1].values():
                for state_2 in set_of_succ:
                    if state_1==state_2:
                        return False
    else:
        return False

    return True

# returns True if given automaton doesn't recognize
# any language, False otherwise
def empty(automaton):
    sccs = tarjan(automaton,automaton.initial) 

    return len(sccs)==0