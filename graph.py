import graphviz
from buchi_automaton import *

def draw_graph(automaton):
    automaton_image = graphviz.Digraph('BA')  
    automaton_image.attr(rankdir='LR')
    automaton_image.attr('node', shape = 'circle')

    for state in automaton.automaton_image:
        if state in automaton.accepting:
            automaton_image.attr('node',rankdir='LR', size = '8,5', shape = 'doublecircle')
        else:
            automaton_image.attr('node',rankdir='LR', size = '8,5', shape = 'circle')
            
        automaton_image.node(state)


    for i in automaton.transition:
        state_1 = i[0]
        in_symbol = i[1]
        for state_2 in i[2]:
            automaton_image.edge(state_1, state_2, label = in_symbol)

    automaton_image.render(directory='automaton')