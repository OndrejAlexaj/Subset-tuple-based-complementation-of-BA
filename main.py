from buchi_automaton import *
from input import *
from draw_automaton import *
from union import *
from emptiness import *

buchiAutomaton_1 = create_automaton("inputs/example.ba")
draw_graph(buchiAutomaton_1)
#buchiAutomaton_2 = create_automaton("inputs/example2.ba")
#draw_graph(buchiAutomaton_2)

#unified = union(buchiAutomaton_1, buchiAutomaton_2)
#draw_graph(unified)