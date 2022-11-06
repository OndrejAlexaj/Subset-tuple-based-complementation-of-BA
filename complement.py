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
    for component in state:
        if component[1]==2:
            return False
    
    return True

def replace_states_trans(automaton,translation,new_automaton):
    for state in automaton.transition:
        for symbol in automaton.transition[state]:
            for next_state in automaton.transition[state][symbol]:
                new_automaton = mark_transition(new_automaton,[translation[state],symbol,translation[next_state]])

    return new_automaton

def join2(automaton):
    translation = dict()
    new_state = []
    new_set = set()
    was_color_2 = False
    new_automaton = BuchiAutomaton(set(),set(),dict(),"",set(),automaton.symbols)

    for state in automaton.states:
        for set_and_coloring in state:
            if set_and_coloring[1] == 2:
                if len(new_set) != 0:
                    new_state.append((MyFrozenSet(new_set),2))
                was_color_2 = True
                new_set = set_and_coloring[0]
            elif set_and_coloring[1] == 1 and was_color_2:
                new_set = new_set.union(new_set,set_and_coloring[0])
            else:
                if len(new_set) != 0:
                    new_state.append((MyFrozenSet(new_set),2))
                    new_set = set()
                was_color_2 = False
                new_state.append(set_and_coloring)
        if(len(new_set) != 0):
            new_state.append((MyFrozenSet(new_set),2))
            new_set = set()
        new_automaton.states.add(tuple(new_state))
        translation[state] = tuple(new_state)
        new_state = []
        was_color_2 = False
    new_automaton.initial = translation[automaton.initial]
    return replace_states_trans(automaton,translation,new_automaton)

def join(automaton):
    translation = dict()
    new_state = []
    new_set_1s = set()
    new_set_2s = set()
    new_automaton = BuchiAutomaton(set(),set(),dict(),"",set(),automaton.symbols)

    # firstly merge consecutive 1s and consecutive 2s separately
    for state in automaton.states:
        for set_and_coloring in state:
            if set_and_coloring[1] == 1:
                new_set_1s = new_set_1s.union(new_set_1s,set_and_coloring[0])
            else:
                if len(new_set_1s) != 0:
                    new_state.append((MyFrozenSet(new_set_1s),1))
                    new_set_1s = set()
                if set_and_coloring[1] == 2:
                    new_set_2s = new_set_2s.union(new_set_2s,set_and_coloring[0])
                else:
                    if len(new_set_2s) != 0:
                        new_state.append((MyFrozenSet(new_set_2s),2))
                        new_set_2s = set()
                    new_state.append(set_and_coloring)
        
        if len(new_set_1s) != 0:
            new_state.append((MyFrozenSet(new_set_1s),1))
            new_set_1s = set()
        if len(new_set_2s) != 0:
            new_state.append((MyFrozenSet(new_set_2s),2))
            new_set_2s = set()

        new_automaton.states.add(tuple(new_state))
        translation[state] = tuple(new_state)
        new_state = []

    new_automaton.initial = translation[automaton.initial]
    return replace_states_trans(automaton,translation,new_automaton)

def merge(automaton):
    new_automaton = join(automaton)
    new_automaton = join2(new_automaton)

    return new_automaton

# adds color 3 so each state contains at most one color 3 xor 2
def color_3(automaton):


# parameter "upper" indicates wheter we also build upper automaton or not
def determinise(automaton,interim_automaton,curr_state,upper,rightmost_2s,merge_states,add_color_3):
    succ_tmp, acc_states, new_states, new_colored = set(), set(), set(), set()
    tmp_states, colored_tmp = [], []
    original_len = len(interim_automaton.states)
    visited = init_visited(automaton) # to preserve disjointness of sets in one state
    accepting = True
    keep = True
    processed = set()

    while(1):
        breakpoint = is_breakpoint(curr_state)
        if(curr_state not in processed):    
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
                # component in state has color 2, then it doesn't need to be stored (can be altered by argument --> rightmost_2s)
                if len(colored_tmp)!=0 and (colored_tmp[0][1]!=2 or not rightmost_2s):
                    interim_automaton.states.add(tuple(reversed(colored_tmp)))
                    mark_transition(interim_automaton,[curr_state,symbol,tuple(reversed(colored_tmp))])
                    new_colored.add(tuple(reversed(colored_tmp)))
                    if accepting:
                        interim_automaton.accepting.add(tuple(reversed(colored_tmp)))

                tmp_states = []
                colored_tmp = []
                accepting = True
                visited = init_visited(automaton)

            processed.add(curr_state)
        new_states.discard(curr_state)
        if(len(new_states) == 0):
            upper = False
            new_colored.discard(curr_state)
            if(len(new_colored)==0):
                break
            curr_state = new_colored.pop()  
        else:
            curr_state = new_states.pop()


    #if original_len!=len(interim_automaton.states):
        #for state in new_states:
            #interim_automaton = determinise(automaton,interim_automaton,state,True)
       #for state in new_colored:
            #interim_automaton = determinise(automaton,interim_automaton,state,False)

    return interim_automaton

# Returns complement of the given automaton.
# State name consists of tuple of sets for
# better understanding of output.
def complement(automaton,rightmost_2s,merge_states,add_color_3):
    automaton = complete_automaton(automaton)

    upper_part = BuchiAutomaton(set(),set(),dict(),"",set(),automaton.symbols)
    upper_part.alphabet = automaton.alphabet
    upper_part.initial = ((MyFrozenSet({automaton.initial}),-1),)
    upper_part.states.add(upper_part.initial)
    complemented = determinise(automaton,upper_part,upper_part.initial,True,rightmost_2s,merge_states,add_color_3)

    if merge_states:
        complemented = merge(complemented)
    
    if add_color_3:
        complemented = color_3(complemented)

    print(len(complemented.states))

    return complemented