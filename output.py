from enum import auto
from buchi_automaton import *

def output_BA_format(automaton):
    f = open("output.ba","w")

    f.write(str(automaton.initial)+"\n")

    for state_1 in automaton.states:
        for symbol in automaton.transition[state_1]:
            for state_2 in automaton.transition[state_1][symbol]:
                f.write(str(symbol)+","+str(state_1)+"->"+str(state_2)+"\n")
    
    for state in automaton.accepting:
        f.write(str(state)+"\n")
        
    f.close()

def output_HOA_format(automaton):
    translation = dict()
    number = 0
    for i in automaton.states:
        translation[i] = number
        number+=1

    new_name = "output.hoa"
    f = open(new_name, "w")
    f.write("HOA: v1\n")
    f.write(f"States: {len(automaton.states)}\n")
    f.write("Start: "+str(translation[automaton.initial])+"\n")
    f.write("acc-name: Buchi\n")
    f.write("Acceptance: 1 Inf(0)\n")
    f.write("properties: explicit-labels state-acc trans-labels\n")

    f.write(f"AP: {len(automaton.symbols)}")
    for i in automaton.symbols:
        f.write(i+" ")
    f.write("\n")

    # body
    f.write("--BODY--\n")
    for state in automaton.states:
        f.write("State: "+str(translation[state]))
        if state in automaton.accepting:
            f.write(" {0}")
        f.write("\n")

        if automaton.transition.get(state) is not None:
            for alph_member in automaton.transition[state]:
                if automaton.transition[state].get(alph_member) is not None:
                    for next_state in automaton.transition[state][alph_member]:
                        f.write(f"\t[{alph_member}] {translation[next_state]}\n")

    f.write("--END--\n")
    f.close()