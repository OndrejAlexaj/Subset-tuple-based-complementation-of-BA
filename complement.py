from buchi_automaton import *
from edit_BA import *

pocitadlo = 0

class MyFrozenSet(frozenset):
    def __repr__(self):
        return "{"+'{}'.format(', '.join(map(repr, self)))+"}"

def init_visited(automaton):
    visited = dict()
    for state in automaton.states:
        visited[state] = False

    return visited

def is_breakpoint(state):
    for component in state:
        if component[1]==2:
            return False
    
    return True

#def replace_states_trans(automaton,translation):
#    for state in automaton.transition:
#        for symbol in automaton.transition[state]:
#            for next_state in 

def merge_consecutive(automaton):
    new_state = []
    new_set_1s = set()
    new_set_2s = set()
    new_states = set()

    # firstly merge consecutive 1s and consecutive 2s separately
    for state in automaton.states:
        for set_and_coloring in state:
            if set_and_coloring[1] == 1:
                new_set_1s = new_set_1s.union(new_set_1s,set_and_coloring[0])
            else:
                if len(new_set_1s) != 0:
                    new_state.append((MyFrozenSet(new_set_1s,1)))
                    new_set_1s = set()
                if set_and_coloring[1] == 2:
                    new_set_2s = new_set_2s.union(new_set_2s,set_and_coloring[0])
                else:
                    if len(new_set_2s) != 0:
                        new_state.append((MyFrozenSet(new_set_2s),2))
                        new_set_2s = set()
                    new_state.append(set_and_coloring)
        
        if len(new_set_1s) != 0:
            new_state.append((MyFrozenSet(new_set_1s,1)))
            new_set_1s = set()
        if len(new_set_2s) != 0:
            new_state.append((MyFrozenSet(new_set_2s),2))
            new_set_2s = set()
        
        new_states.add(tuple(new_state))
        translation[state] = tuple(new_state)
        automaton.transition[tuple(new_state)] = automaton.transition[state]
        del automaton.transition[state]
        new_state = []

    automaton.states = new_states
    #automaton = replace_states_trans(automaton,translation)

    # secondly merge 2 followed by 1


def optimise(automaton):
    translation = dict()

    translation = merge_consec(automaton,translation)

    

    return automaton

# parameter "upper" indicates wheter we also build upper automaton or not
def determinise(automaton,interim_automaton,curr_state,upper):
    global pocitadlo
    pocitadlo+=1
    succ_tmp, acc_states, new_states, new_colored = set(), set(), set(), set()
    tmp_states, colored_tmp = [], []
    original_len = len(interim_automaton.states)
    visited = init_visited(automaton) # to preserve disjointness of sets in one state
    breakpoint = is_breakpoint(curr_state)
    accepting = True

    for symbol in interim_automaton.alphabet:
        for states_set_pos in reversed(range(len(curr_state))):
            for state in curr_state[states_set_pos][0]:
                for succ in automaton.transition[state][symbol]:
                    # here we distinguish (and store differently) accepting
                    # and non-accepting states
                    if succ in automaton.accepting:
                        if not visited[succ]:
                            acc_states.add(succ)
                            visited[succ] = True
                    else:
                        if not visited[succ]:
                            succ_tmp.add(succ)
                            visited[succ] = True

            # "tmp_states" stores what state we have build so far.
            if len(acc_states)!=0:
                if upper:
                    tmp_states.append((MyFrozenSet(acc_states),-1))

                # deciding next coloring (based on the paper)
                if breakpoint and (curr_state[states_set_pos][1]==0 or curr_state[states_set_pos][1]==-1):
                    colored_tmp.append((MyFrozenSet(acc_states),2))
                elif not breakpoint and (curr_state[states_set_pos][1]==0 or curr_state[states_set_pos][1]==-1):
                    colored_tmp.append((MyFrozenSet(acc_states),1))
                elif breakpoint and curr_state[states_set_pos][1]==1:
                    colored_tmp.append((MyFrozenSet(acc_states),2))
                else:
                    if curr_state[states_set_pos][1]==-1:
                        colored_tmp.append((MyFrozenSet(acc_states),0))
                    else:
                        colored_tmp.append((MyFrozenSet(acc_states),curr_state[states_set_pos][1])) 

                if colored_tmp[-1][1]==2: # accepting is only the state that doesn't conaint
                    accepting = False        # 2 colored component

            if len(succ_tmp)!=0:
                if upper:
                    tmp_states.append((MyFrozenSet(succ_tmp),-1))    

                # deciding next coloring (based on the paper)
                if breakpoint and curr_state[states_set_pos][1]==1:
                    colored_tmp.append((MyFrozenSet(succ_tmp),2)) 
                else:
                    if curr_state[states_set_pos][1]==-1:
                        colored_tmp.append((MyFrozenSet(succ_tmp),0))
                    else:
                        colored_tmp.append((MyFrozenSet(succ_tmp),curr_state[states_set_pos][1]))    

                if colored_tmp[-1][1]==2:
                    accepting = False

            acc_states = set()
            succ_tmp = set()

        if len(tmp_states)!=0 and upper:
            interim_automaton.states.add(tuple(reversed(tmp_states)))
            mark_transition(interim_automaton,[curr_state,symbol,tuple(reversed(tmp_states))])
            new_states.add(tuple(reversed(tmp_states)))
        
        # "colored_tmp[0][1]!=2" is there because if the rightmost(here it is leftmost, but it will be reversed eventually) 
        # component in state has color 2, then it doesn't need to be stored
        if len(colored_tmp)!=0 and colored_tmp[0][1]!=2:
            interim_automaton.states.add(tuple(reversed(colored_tmp)))
            mark_transition(interim_automaton,[curr_state,symbol,tuple(reversed(colored_tmp))])
            new_colored.add(tuple(reversed(colored_tmp)))
            if accepting:
                interim_automaton.accepting.add(tuple(reversed(colored_tmp)))

        tmp_states = []
        colored_tmp = []
        accepting = True
        visited = init_visited(automaton)
    
    #if pocitadlo>100000:
      #  return interim_automaton

    if original_len!=len(interim_automaton.states):
        for state in new_states:
            interim_automaton = determinise(automaton,interim_automaton,state,True)
        for state in new_colored:
            interim_automaton = determinise(automaton,interim_automaton,state,False)

    return interim_automaton

# Returns complement of the given automaton.
# State name consists of tuple of sets for
# better understanding of output.
def complement(automaton):
    automaton = complete_automaton(automaton)

    upper_part = BuchiAutomaton(set(),set(),dict(),"",set(),automaton.symbols)
    upper_part.alphabet = automaton.alphabet
    upper_part.initial = ((MyFrozenSet({automaton.initial}),-1),)
    upper_part.states.add(upper_part.initial)
    complemented = determinise(automaton,upper_part,upper_part.initial,True)

    optimise(complemented)

    return complemented