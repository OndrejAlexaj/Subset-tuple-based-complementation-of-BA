import graphviz
from buchi_automaton import *

def draw_graph(automaton):
    states = graphviz.Digraph('BA')  
    states.attr(rankdir='LR')
    states.attr('node', shape = 'circle')

    for state in automaton.states:
        if state in automaton.accepting:
            states.attr('node',rankdir='LR', size = '8,5', shape = 'doublecircle')
        else:
            states.attr('node',rankdir='LR', size = '8,5', shape = 'circle')
            
        states.node(state)


    for i in automaton.transition:
        state_1 = i[0]
        in_symbol = i[1]
        for state_2 in i[2]:
            states.edge(state_1, state_2, label = in_symbol)

    states.render(directory='automaton')