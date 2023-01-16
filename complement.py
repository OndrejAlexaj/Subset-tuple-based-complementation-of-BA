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

###############################
# Algorithms for optimization #
###############################

def merge_4s(state):
    new_state = []
    new_set_4s = set()

    for set_and_coloring in state:
        if set_and_coloring[1] == 4:
            new_set_4s = new_set_4s.union(new_set_4s,set_and_coloring[0])
        else:
            if len(new_set_4s) != 0:
                new_state.append((MyFrozenSet(new_set_4s),4))
                new_set_4s = set()
            new_state.append(set_and_coloring)

    if len(new_set_4s) != 0:
        new_state.append((MyFrozenSet(new_set_4s),4))
        new_set_4s = set()
    
    return new_state


# what if something like 2 1 2 occurs -> 2 2 ?? or 2 ??
def merge_state(state):
    new_state = []
    new_set_1s = set()
    new_set_2s = set()

    for set_and_coloring in state:
        if set_and_coloring[1] == 1:
            if len(new_set_2s) != 0:
                new_state.append((MyFrozenSet(new_set_2s),2))
                new_set_2s = set()
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
    
    res_state = []
    new_set = set()
    was_color_2 = False
    finish = False

    while not finish:
        finish = True
        for set_and_coloring in new_state:
            if set_and_coloring[1] == 2:
                if len(new_set) != 0:
                    res_state.append((MyFrozenSet(new_set),2))
                was_color_2 = True
                new_set = set_and_coloring[0]
            elif set_and_coloring[1] == 1 and was_color_2:
                new_set = new_set.union(new_set,set_and_coloring[0])
                finish = False
            else:
                if len(new_set) != 0:
                    res_state.append((MyFrozenSet(new_set),2))
                    new_set = set()
                was_color_2 = False
                res_state.append(set_and_coloring)
        if(len(new_set) != 0):
            res_state.append((MyFrozenSet(new_set),2))
            new_set = set()
        
        res_state = []
        new_set = set()
        was_color_2 = False
    
    return tuple(res_state)

def mikrostates_in_makro(state):
    acc = 0
    for component in state:
        acc += len(component[0])
    
    return acc

def where_to_start(amount_to_right,state):
    index = 0
    if amount_to_right==0:
        return index

    states_cnt = 0
    for i in reversed(range(len(state))):
        index = i
        states_cnt += len(state[i][0])
        if(states_cnt >= amount_to_right):
            return (index)%len(state)

    return 0

def contains_multiple(state):
    count = 0
    for i in state:
        if i[1]==3 or i[1]==2:
            count+=1
    
    return count>=2


# adds color 3 so each state contains at most one color 3 xor 2
def color_3(automaton,interim_automaton,curr_state,upper):
    succ_tmp, has_acc_states, new_states, new_colored = set(), set(), set(), set()
    tmp_states, colored_tmp = [], []
    visited = init_visited(automaton) # to preserve disjointness of sets in one state
    accepting = True
    processed = set()

    is_acc_part = False
    nonacc_part = False

    while(1):
        if(curr_state not in processed): 
            was_2_in_pred = not is_breakpoint(curr_state) 
            for symbol in interim_automaton.alphabet:
                discontinued_2 = False
                was_zero = False
                find_right = False
                for states_set_pos in reversed(range(len(curr_state))):
                    for state in curr_state[states_set_pos][0]:
                        for succ in automaton.transition[state][symbol]:
                            # here we distinguish (and store differently) accepting
                            # and non-accepting states
                            if succ in automaton.accepting:
                                if not visited[succ]:
                                    has_acc_states.add(succ)
                                    visited[succ] = True
                            else:
                                if not visited[succ]:
                                    succ_tmp.add(succ)
                                    visited[succ] = True

                    # "tmp_states" stores what state we have build so far.

                    if len(has_acc_states)!=0:
                        is_acc_part = True
                        if upper:
                            tmp_states.insert(0,(MyFrozenSet(has_acc_states),-1))

                        if (curr_state[states_set_pos][1]==0 or curr_state[states_set_pos][1]==-1):
                            colored_tmp.insert(0,(MyFrozenSet(has_acc_states),1))
                        elif curr_state[states_set_pos][1]==3:
                            colored_tmp.insert(0,(MyFrozenSet(has_acc_states),2))
                        else:
                            if curr_state[states_set_pos][1]==1:
                                colored_tmp.insert(0,(MyFrozenSet(has_acc_states),4)) # to know which 1s were present in the predecessor
                            else:
                                colored_tmp.insert(0,(MyFrozenSet(has_acc_states),curr_state[states_set_pos][1]))

                        if colored_tmp[0][1]==2: # accepting is only the state that doesn't conaint
                            accepting = False        # 2 colored component

                    if len(succ_tmp)!=0:
                        nonacc_part = True
                        if upper:
                            tmp_states.insert(0,(MyFrozenSet(succ_tmp),-1))    

                        if curr_state[states_set_pos][1]==3:
                            colored_tmp.insert(0,(MyFrozenSet(succ_tmp),2))
                        elif curr_state[states_set_pos][1]==-1:
                            colored_tmp.insert(0,(MyFrozenSet(succ_tmp),0))
                        else:
                            if curr_state[states_set_pos][1]==1:
                                colored_tmp.insert(0,(MyFrozenSet(succ_tmp),4)) # to know which 1s are continued
                            else:
                                colored_tmp.insert(0,(MyFrozenSet(succ_tmp),curr_state[states_set_pos][1]))

                        if colored_tmp[0][1]==2: # accepting is only the state that doesn't conaint
                            accepting = False        # 2 colored component
                    
        
                    if not is_acc_part and not nonacc_part and curr_state[states_set_pos][1]==2:
                        discontinued_2 = True
                        for i in range(len(colored_tmp)):
                            if colored_tmp[i][1]==0:
                                find_right = True
                                colored_tmp[i] = (colored_tmp[i][0],10)
                                break

                    has_acc_states = set()
                    succ_tmp = set()
                    is_acc_part = False
                    nonacc_part = False

                if len(colored_tmp)!=0:
                    colored_tmp = list(merge_4s(colored_tmp))
                    colored_tmp = list(merge_state(colored_tmp))
                
                breakp = is_breakpoint(colored_tmp)
                
                if (discontinued_2 and breakp):
                    was_zero = False
                    changed = False
                    if find_right:
                        for i in range(len(colored_tmp)):
                            if colored_tmp[i][1]==10:
                                was_zero = True
                                colored_tmp[i] = (colored_tmp[i][0],0)
                            if colored_tmp[i][1]==4 and was_zero:
                                colored_tmp[i] = (colored_tmp[i][0],3)
                                changed = True
                                break
                    if not find_right or not changed:
                        for i in range(len(colored_tmp)):
                            if colored_tmp[i][1]==0:
                                was_zero = True
                            if colored_tmp[i][1]==4 and was_zero:
                                colored_tmp[i] = (colored_tmp[i][0],3)
                                break
                    if not was_zero:
                        for i in range(len(colored_tmp)):
                            if colored_tmp[i][1]==4:
                                colored_tmp[i] = (colored_tmp[i][0],3)
                                break
                elif(not was_2_in_pred and breakp):
                    for i in range(len(colored_tmp)):
                        if colored_tmp[i][1]==4:
                            colored_tmp[i] = (colored_tmp[i][0],3)
                            break

                for i in range(len(colored_tmp)):
                    if colored_tmp[i][1]==4:
                        colored_tmp[i] = (colored_tmp[i][0],1)
                
                if len(colored_tmp)!=0:
                    colored_tmp = list(merge_state(colored_tmp))
                    colored_tmp = list(merge_state(colored_tmp))

                if len(tmp_states)!=0 and upper:
                    interim_automaton.states.add(tuple(tmp_states))
                    mark_transition(interim_automaton,[curr_state,symbol,tuple(tmp_states)])
                    new_states.add(tuple(tmp_states))

                # "colored_tmp[-1][1]!=2" is there because if the rightmost(here it is leftmost, but it will be reversed eventually) 
                # component in state has color 2, then it doesn't need to be stored (can be altered by argument --> rightmost_2s)
                if len(colored_tmp)!=0 and (colored_tmp[-1][1]!=2):
                    interim_automaton.states.add(tuple(colored_tmp))
                    mark_transition(interim_automaton,[curr_state,symbol,tuple(colored_tmp)])
                    new_colored.add(tuple(colored_tmp))
                    if accepting:
                        interim_automaton.accepting.add(tuple(colored_tmp))

                tmp_states = []
                colored_tmp = []
                accepting = True
                visited = init_visited(automaton)
        # keeping track of processed states
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
    
    return interim_automaton

#############################
# Main complementation part #
#############################

# parameter "upper" indicates wheter we also build upper automaton or not
def determinise(automaton,interim_automaton,curr_state,upper,rightmost_2s,merge_states,delay):
    succ_tmp, has_acc_states, new_states, new_colored = set(), set(), set(), set()
    tmp_states, colored_tmp = [], []
    visited = init_visited(automaton) # to preserve disjointness of sets in one state
    accepting = True
    processed = set()

    waiting_states = set()
    waiting_states.add(interim_automaton.initial)
    waiting_trans = dict()

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
                                    has_acc_states.add(succ)
                                    visited[succ] = True
                            else:
                                if not visited[succ]:
                                    succ_tmp.add(succ)
                                    visited[succ] = True

                    # "tmp_states" stores what state we have build so far.
                    if len(has_acc_states)!=0:
                        if upper:
                            tmp_states.insert(0,(MyFrozenSet(has_acc_states),-1))

                        # deciding next coloring (based on the paper)
                        if breakpoint and (curr_state[states_set_pos][1]==0 or curr_state[states_set_pos][1]==-1):
                            colored_tmp.insert(0,(MyFrozenSet(has_acc_states),2))
                        elif not breakpoint and (curr_state[states_set_pos][1]==0 or curr_state[states_set_pos][1]==-1):
                            colored_tmp.insert(0,(MyFrozenSet(has_acc_states),1))
                        elif breakpoint and curr_state[states_set_pos][1]==1:
                            colored_tmp.insert(0,(MyFrozenSet(has_acc_states),2))
                        else:
                            if curr_state[states_set_pos][1]==-1:
                                colored_tmp.insert(0,(MyFrozenSet(has_acc_states),0))
                            else:
                                colored_tmp.insert(0,(MyFrozenSet(has_acc_states),curr_state[states_set_pos][1])) 

                        if colored_tmp[0][1]==2: # accepting is only the state that doesn't conaint
                            accepting = False        # 2 colored component

                    if len(succ_tmp)!=0:
                        if upper:
                            tmp_states.insert(0,(MyFrozenSet(succ_tmp),-1))    

                        # deciding next coloring (based on the paper)
                        if breakpoint and curr_state[states_set_pos][1]==1:
                            colored_tmp.insert(0,(MyFrozenSet(succ_tmp),2)) 
                        else:
                            if curr_state[states_set_pos][1]==-1:
                                colored_tmp.insert(0,(MyFrozenSet(succ_tmp),0))
                            else:
                                colored_tmp.insert(0,(MyFrozenSet(succ_tmp),curr_state[states_set_pos][1]))    

                        if colored_tmp[0][1]==2:
                            accepting = False
                    

                    has_acc_states = set()
                    succ_tmp = set()

                if len(tmp_states)!=0 and upper:
                    interim_automaton.states.add(tuple(tmp_states))
                    mark_transition(interim_automaton,[curr_state,symbol,tuple(tmp_states)])
                    new_states.add(tuple(tmp_states))

                    waiting_states.add(tuple(tmp_states))
                    if(waiting_trans.get(curr_state) is not None):
                        if (waiting_trans[curr_state]).get(symbol) is not None:
                            (waiting_trans[curr_state][symbol]).add(tuple(tmp_states))
                        else:
                            waiting_trans[curr_state][symbol] = {tuple(tmp_states)}
                    else:
                        waiting_trans[curr_state] = {symbol:{tuple(tmp_states)}}

                # "colored_tmp[0][1]!=2" is there because if the rightmost(here it is leftmost, but it will be reversed eventually) 
                # component in state has color 2, then it doesn't need to be stored (can be altered by argument --> rightmost_2s)
                if len(colored_tmp)!=0 and (colored_tmp[-1][1]!=2 or not rightmost_2s):
                    if curr_state[-1][1]==-1 and delay:
                        if state_in_scc(waiting_states, waiting_trans, symbol, tuple(curr_state), tuple(tmp_states)):
                        #visited = dict()
                        #rec_stack = dict()
                        #for state in waiting_states:
                        #    visited[state] = False
                        #    rec_stack[state] = False
                        #visited[curr_state] = True
                        #rec_stack[curr_state] = True
#
                        #if closes_cycle(waiting_states,waiting_trans,tuple(tmp_states),visited,rec_stack,tuple(curr_state)):
                            if merge_states:
                                colored_tmp = merge_state(tuple(colored_tmp))
                            else:
                                colored_tmp = tuple(colored_tmp)
                            interim_automaton.states.add(colored_tmp)
                            mark_transition(interim_automaton,[curr_state,symbol,colored_tmp])
                            new_colored.add(colored_tmp)

                            if accepting:
                                interim_automaton.accepting.add(colored_tmp)
                    else:
                        if merge_states:
                            colored_tmp = merge_state(tuple(colored_tmp))
                        else:
                            colored_tmp = tuple(colored_tmp)
                        interim_automaton.states.add(colored_tmp)
                        mark_transition(interim_automaton,[curr_state,symbol,colored_tmp])
                        new_colored.add(colored_tmp)

                        if accepting:
                            interim_automaton.accepting.add(colored_tmp)

                tmp_states = []
                colored_tmp = []
                accepting = True
                visited = init_visited(automaton)
        # keeping track of processed states
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
    return interim_automaton

# source:
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
# section - The algorithm in pseudocode
def state_in_scc(states, trans, symbol, state_to_check1, state_to_check2):
    index = 0
    sccs, stack, all_sccs = [], [], []
    indices, lowlinks, on_stack = dict(), dict(), dict()

    params_stack = []

    for v in states:
        indices[v] = -1
        on_stack[v] = False
    
    #params_stack.append(state_to_check1)
    def in_strongconnect(v):
        nonlocal index
    #while len(params_stack)>0:
        #v = params_stack.pop()
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        if trans.get(v) is not None: # to catch if the automaton is not complete
            for tmp in trans[v].values():
                for succ in tmp: # it is guaranteed that this cycle is performed
                    if indices[succ] == -1:
                        #params_stack.append(succ)
                        #continue
                        if in_strongconnect(succ):
                            return True
                        lowlinks[v] = min(lowlinks[v],lowlinks[succ])
                    elif on_stack[succ]:
                        lowlinks[v] = min(lowlinks[v],indices[succ])

        if lowlinks[v] == indices[v]:
            scc = set()
            while True:
                w = stack.pop()
                scc.add(w)
                on_stack[w] = False
                if(w == v):
                    break

            if not is_trivial(trans, scc, symbol) and (state_to_check1 in scc) and (state_to_check2 in scc):
                return True
            else:
                return False
        return False

    # in pseudocode this part is above the strongconnect(),
    # but to make it run it needs to be after definition
    #for state in states:
    #    stack = []
    if indices[state_to_check1] == -1:
        if in_strongconnect(state_to_check1):
            return True 

    return False

# returns True if the SCC is trivial, False otherwise
def is_trivial(trans, component, symbol):
    # component which contains only 1 state Q is non-trivial
    # iff there exists edge from Q to Q
    if len(component) == 1:
        for state_1 in component:
            if trans.get(state_1) is None: # if automaton is not complete
                return False
            for set_of_succ in trans[state_1].values():
                for state_2 in set_of_succ:
                    if state_1==state_2:
                        return False
    else:
        return False

    return True

def closes_cycle(states,trans,state_to_check,visited,rec_stack,end_state):
    visited[state_to_check] = True
    rec_stack[state_to_check] = True

    if trans.get(state_to_check) is not None: # to catch if the automaton is not complete
        for tmp in trans[state_to_check].values():
            for succ in tmp: # it is guaranteed that this cycle is performed
                if succ != end_state and not visited[succ]:
                    if closes_cycle(states,trans,succ,visited,rec_stack,end_state):
                        return True
                elif succ == end_state:
                    return True

    return False
# Returns complement of the given automaton.
# State name consists of tuple of sets for
# better understanding of output.
def complement(automaton,rightmost_2s,merge_states,add_color_3,delay):
    upper_part = BuchiAutomaton(set(),set(),dict(),"",set(),automaton.symbols)
    upper_part.alphabet = automaton.alphabet
    upper_part.initial = ((MyFrozenSet({automaton.initial}),-1),)
    upper_part.states.add(upper_part.initial)
    automaton = complete_automaton(automaton)

    if add_color_3:
        complemented = color_3(automaton,upper_part,upper_part.initial,True)
    else:
        complemented = determinise(automaton,upper_part,upper_part.initial,True,rightmost_2s,merge_states,delay)

    return complemented