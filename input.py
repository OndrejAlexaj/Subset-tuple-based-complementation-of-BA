from enum import auto
from buchi_automaton import *

# todo -> make automaton complete


# redundant function when marking transition one by one ->
# -> not having something like [[q0,a,{q1,q2}]] but [[q0,a,q1], [q0,a,q2]]
def mark_transition(automaton, new_transition):
    # finding if there exists non-determinism (more states from one state)
    for i in range(len(automaton.transition)):
        if automaton.transition[i][0] == new_transition[0] and automaton.transition[i][1] == new_transition[1]:
            automaton.transition[i][2].add(new_transition[2])
            return automaton
    # if not, it is the new transition --> we make "set" from destination state for further adding (might also be list)
    tmp = new_transition[2]
    new_transition[2] = set()
    new_transition[2].add(tmp)
    automaton.transition.append(new_transition)
    return automaton

# todo - optimise
# returns [q1,a,q2]
def parse(line):
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
def create_automaton(description_file):
    automaton = BuchiAutomaton(set(),set(),list(),set(),set())

    description = open(description_file, "r")
    expecting_initial = True
    in_transitions = False # to know when reading transitions lines

    while True:
        line = description.readline()
        if line == "":
            break

        line = line.strip('\n') # remove '\n'
        if "," in line: # parsing makes sense only when in transitions (sign that we are reading transition is ',')
            parsed = parse(line)
            in_transitions = True
        else:
            in_transitions = False

        if expecting_initial and not in_transitions:
            automaton.initial.add(line)
            automaton.states.add(line)
        elif expecting_initial and in_transitions:
            automaton.initial.add(parsed[0])
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