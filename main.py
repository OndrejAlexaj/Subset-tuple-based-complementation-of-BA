from hashlib import new
from venv import create
from buchi_automaton import *
from input import *
from draw_automaton import *
from union import *
from emptiness import *
from intersection import *
from output import *
from edit_BA import *

buchiAutomaton_1 = create_automaton("inputs/example.ba")
#draw_graph(buchiAutomaton_1)
buchiAutomaton_2 = create_automaton("inputs/example2.ba")
#draw_graph(buchiAutomaton_2)

unified = union(buchiAutomaton_1, buchiAutomaton_2)
draw_graph(unified)
intersected = intersection(buchiAutomaton_1,buchiAutomaton_2)
#new_inter = intersection(buchiAutomaton_1,buchiAutomaton_2)


draw_graph(buchiAutomaton_2)
create_output(buchiAutomaton_2)
#draw_graph(remove_dead_states(buchiAutomaton_2))
#print(len(new_inter.states))
print("Given automaton is empty: ",empty(buchiAutomaton_2))

