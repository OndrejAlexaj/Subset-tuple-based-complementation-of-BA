import graphviz
from buchi_automaton import *

def draw_graph(automaton):
    state = graphviz.Digraph('BA')  
    states = list(automaton.states)

    state.attr('node',rankdir='LR', size = '8,5', shape = 'circle')
    state.attr(rankdir='LR', size='8,5')
    for i in range(len(states)):
        if states[i] in list(automaton.accepting):
            state.attr('node',rankdir='LR', size = '8,5', shape = 'doublecircle')
        state.node(states[i])
        state.attr('node',rankdir='LR', size = '8,5', shape = 'circle')


    for i in automaton.transition:
        sets = list(i[2])
        for j in sets:
            state.edge(i[0], j, label = i[1])

    state.render(directory='doctest-output').replace('\\', '/')