from buchi_automaton import *
from edit_BA import *

class MyFrozenSet(frozenset):
    def __repr__(self):
        return "{"+'{}'.format(', '.join(map(repr, self)))+"}"

def init_visited(automaton):
    visited = dict()
    for state in automaton.states:
        visited[state] = False

    return visited

def is_breakpoint(state):
    for pair in state:
        if pair[1]==2:
            return False
    
    return True

def remove_duplicates(arr):
    result_ls = []
    for item in arr:
        if item not in result_ls:
            result_ls.append(item)
    
    return result_ls

def determinise(automaton,interim_automaton,prev_state,upper):
    succ_tmp, acc_states, new_states, colored = set(), set(), set(), set()
    tmp_states = []
    original_len = len(interim_automaton.states)
    visited = init_visited(automaton)
    colored_states = []
    breakpoint = is_breakpoint(prev_state)
    accepting = True
    
    for symbol in interim_automaton.alphabet:
        for states_set in reversed(range(len(prev_state))):
            for state in prev_state[states_set][0]:
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
                if upper:
                    tmp_states.append((MyFrozenSet(acc_states),-1))

                if breakpoint and (prev_state[states_set][1]==0 or prev_state[states_set][1]==-1):
                    colored_states.append((MyFrozenSet(acc_states),2))
                elif not breakpoint and (prev_state[states_set][1]==0 or prev_state[states_set][1]==-1):
                    colored_states.append((MyFrozenSet(acc_states),1))
                elif breakpoint and prev_state[states_set][1]==1:
                    colored_states.append((MyFrozenSet(acc_states),2))
                else:
                    if prev_state[states_set][1]==-1:
                        colored_states.append((MyFrozenSet(acc_states),0))
                    else:
                        colored_states.append((MyFrozenSet(acc_states),prev_state[states_set][1])) 

                if colored_states[-1][1]==2:
                    accepting = False

            if len(succ_tmp)!=0:
                if upper:
                    tmp_states.append((MyFrozenSet(succ_tmp),-1))    

                if breakpoint and prev_state[states_set][1]==1:
                    colored_states.append((MyFrozenSet(succ_tmp),2)) 
                else:
                    if prev_state[states_set][1]==-1:
                        colored_states.append((MyFrozenSet(succ_tmp),0))
                    else:
                        colored_states.append((MyFrozenSet(succ_tmp),prev_state[states_set][1]))    

                if colored_states[-1][1]==2:
                    accepting = False

            acc_states = set()
            succ_tmp = set()

        if len(tmp_states)!=0:
            if upper:
                tmp_states = remove_duplicates(tmp_states)
                interim_automaton.states.add(tuple(reversed(tmp_states)))
                mark_transition(interim_automaton,[prev_state,symbol,tuple(reversed(tmp_states))])
                new_states.add(tuple(reversed(tmp_states)))
        
        if len(colored_states)!=0:
            colored_states = remove_duplicates(colored_states)
            interim_automaton.states.add(tuple(reversed(colored_states)))
            mark_transition(interim_automaton,[prev_state,symbol,tuple(reversed(colored_states))])
            colored.add(tuple(reversed(colored_states)))
            if accepting:
                interim_automaton.accepting.add(tuple(reversed(colored_states)))

        tmp_states = []
        colored_states = []
        accepting = True
        visited = init_visited(automaton)

    if original_len!=len(interim_automaton.states):
        for state in new_states:
            interim_automaton = determinise(automaton,interim_automaton,state,True)
        for state in colored:
            interim_automaton = determinise(automaton,interim_automaton,state,False)
            
    return interim_automaton

def complement(automaton):
    automaton = complete_automaton(automaton)

    upper_part = BuchiAutomaton(set(),set(),dict(),"",set())
    upper_part.alphabet = automaton.alphabet
    upper_part.initial = ((MyFrozenSet({automaton.initial}),-1),)
    upper_part.states.add(upper_part.initial)
    complemented = determinise(automaton,upper_part,upper_part.initial,True)

    return complemented
