from buchi_automaton import *

# todo -> make automaton complete


# redundant when marking transition one by one
def mark_transition(automaton, new_transition):
    # finding if there exists non-determinism (more states from one state)
    for i in range(len(automaton.transition)):
        if automaton.transition[i][0] == new_transition[0] and automaton.transition[i][1] == new_transition[1]:
            automaton.transition[i][2].add(new_transition[2])
            return automaton
    # if not, it is the new transition --> we make "set" from destination state for further adding (might also be "list")
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
    transitions = False
    while True:
        # "," not in line ----> vytiahnut predtym do boolu
        line = description.readline()
        contains_comma = "," in line
        if line == "":
            break

        line = line.strip('\n') # remove '\n'
        if contains_comma: # parsing makes sense only when transitions (sign that we are reading transition is ',')
            parsed = parse(line)
            transitions = True

        if (contains_comma) and (not transitions):
            automaton.initial.add(parsed[0])
            update_automaton(automaton, parsed)
            automaton = mark_transition(automaton, parsed)   
        elif (contains_comma) and (transitions):
            update_automaton(automaton, parsed)
            automaton = mark_transition(automaton, parsed)
        elif not transitions:
            automaton.initial.add(line)
            automaton.states.add(line)   
        elif (not contains_comma) and (transitions):
            automaton.accepting.add(line)
            automaton.states.add(line)
            transitions = False

    # if transitions == True, it means that there was no explicit accepting state.
    # And by the BA format, in this case all states are considered accepting.
    if transitions:
        automaton.accepting = automaton.states.copy()

    description.close()
    return automaton