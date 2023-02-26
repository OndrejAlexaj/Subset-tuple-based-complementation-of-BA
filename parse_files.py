from ast import parse
from enum import auto
from buchi_automaton import *
from edit_BA import *
import re

# returns [q1,a,q2]
def split_line_BA(line):
    tmp = line.split(",")
    parsed = tmp[1].split("->")
    parsed.insert(1, tmp[0])

    return parsed
    
# returns automaton with updated alphabet and states
def update_automaton(automaton, parsed):
    automaton.alphabet.add(parsed[1])
    automaton.states.add(parsed[0])
    automaton.states.add(parsed[2])

    return automaton

# returns BuchiAutomaton created according .ba file
def BA_format(description_file):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set(),set())

    description = open(description_file, "r")
    expecting_initial = True
    in_transitions = False # to know when reading transitions lines

    while True:
        line = description.readline()
        if line == "":
            break

        line = line.strip('\n') # remove '\n'
        if "," in line: # parsing makes sense only when in transitions (sign that we are reading transition is ',')
            parsed = split_line_BA(line)
            in_transitions = True
        else:
            in_transitions = False

        if expecting_initial and not in_transitions:
            automaton.initial = line
            automaton.states.add(line)
        elif expecting_initial and in_transitions:
            automaton.initial = parsed[0]
            update_automaton(automaton, parsed)
            automaton = mark_transition(automaton, parsed) 
            expecting_initial = False
        elif in_transitions:
            update_automaton(automaton, parsed)
            automaton = mark_transition(automaton, parsed)
        elif not in_transitions:
            automaton.accepting.add(line)
            automaton.states.add(line)

    # if in_transitions, it means that there was no explicit accepting state.
    # And by the BA format, in this case all states are considered accepting.
    if in_transitions:
        automaton.accepting = automaton.states.copy()

    description.close()

    return automaton

def parse_body_state_based(description,automaton):
    while True:
        line = description.readline()
        if "--END--" in line:
            break
        
        if "State:" in line:
            tmp = line[6:]
            state = int((tmp.split())[0])
            if '{' in tmp:
                automaton.accepting.add(state)
            automaton.states.add(state)
        else:
            tmp = line.split()
            alphabet_member = tmp[0][1:-1]

            automaton.alphabet.add('!0')
            automaton.alphabet.add('0')
            mark_transition(automaton,[state,alphabet_member,int(tmp[1])])

    return automaton

def parse_body_trans_based(description,automaton):
    while True:
        line = description.readline()
        if "--END--" in line:
            break
        
        if "State:" in line:
            tmp = line[6:]
            state = int((tmp.split())[0])
            #if '{' in tmp:
            #    automaton.accepting.add(state)
            #automaton.states.add(state)
        else:
            tmp = line.split()
            alphabet_member = tmp[0][1:-1]

            automaton.alphabet.add('!0')
            automaton.alphabet.add('0')
            mark_transition(automaton,[state,alphabet_member,int(tmp[1])])

            if '{' in line:
                automaton.accepting.add((state,alphabet_member,int(tmp[1])))

    return automaton

def HOA_format(description_file,acc_type):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set(),[])

    description = open(description_file, "r")

    states_num = 0
    initials = []

    while True:
        line = description.readline()
        if line == "":
            break

        if "States:" in line:
            states_num = line[7:]
            states_num = int(states_num.strip())
            automaton.states = {x for x in range(states_num)}
        elif "Start:" in line:
            tmp = line[6:]
            tmp = tmp.strip()
            initials.append(int(tmp))
            automaton.initial = int(tmp)
        elif "AP:" in line:
            tmp = line[3:]
            tmp = tmp.split()
            APs_num = int(tmp[0])
            automaton.symbols = [tmp[i+1] for i in range(APs_num)]
        elif "--BODY--" in line:
            if acc_type == "state":
                automaton = parse_body_state_based(description,automaton)
            elif acc_type == "trans":
                automaton = parse_body_trans_based(description,automaton)
            break

    return automaton
             