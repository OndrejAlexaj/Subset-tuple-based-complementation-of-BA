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