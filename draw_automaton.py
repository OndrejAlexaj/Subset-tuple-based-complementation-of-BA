import graphviz
from buchi_automaton import *

def draw_initial(automaton, automaton_image):
    automaton_image.attr('node', shape='none')
    automaton_image.node("")
    if(automaton.initial in automaton.accepting):
        automaton_image.attr('node',rankdir='LR', shape = 'doublecircle')
    else:
        automaton_image.attr('node',rankdir='LR', shape = 'circle')
    automaton_image.node(str(automaton.initial))
    automaton_image.edge("", str(automaton.initial))

def draw_states(automaton, automaton_image):
    for state in automaton.states:
        if state in automaton.accepting:
            automaton_image.attr('node',rankdir='LR', shape = 'doublecircle')
        else:
            automaton_image.attr('node',rankdir='LR', shape = 'circle')
            
        automaton_image.node(str(state))

def draw_edges(automaton, automaton_image):
    for state_1 in automaton.transition:
        for in_symbol in automaton.transition[state_1]:
            for state_2 in automaton.transition[state_1][in_symbol]:
                automaton_image.edge(str(state_1), str(state_2), label = str(in_symbol))

def draw_graph(automaton, name):
    automaton_image = graphviz.Digraph('BA')
    automaton_image.attr(rankdir='LR')
    automaton_image.attr('node', shape = 'circle')
    draw_initial(automaton, automaton_image)  
    draw_states(automaton, automaton_image)
    draw_edges(automaton, automaton_image)

    automaton_image.render(directory='automaton'+str(name))