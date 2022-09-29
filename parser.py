from enum import auto
from buchi_automaton import *
from edit_BA import *

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

# returns BuchiAutomaton created according file with its description
def BA_format(description_file):
    automaton = BuchiAutomaton(set(),set(),dict(),"",set())

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
