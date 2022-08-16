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
        for j in i[2]:
            states.edge(i[0], j, label = i[1])

    states.render(directory='automaton')