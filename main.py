from hashlib import new
from venv import create
from buchi_automaton import *
from input import *
from draw_automaton import *
from union import *
from emptiness import *
from intersection import *
from output import *

buchiAutomaton_1 = create_automaton("inputs/example.ba")
#draw_graph(buchiAutomaton_1)
buchiAutomaton_2 = create_automaton("inputs/example2.ba")
#draw_graph(buchiAutomaton_2)

unified = union(buchiAutomaton_1, buchiAutomaton_2)
draw_graph(unified)
#intersected = intersection(buchiAutomaton_1,buchiAutomaton_2)
#new_inter = intersection(buchiAutomaton_1,buchiAutomaton_2)

#remove dead nodes
#for state in intersected.states:
 #   ok = False
 #   for k in intersected.transition.values():
 #       for j in k.values():
  #          if state in j:
   #             ok = True
  #              break
 #   if not ok and state!=intersected.initial:
  #      new_inter.states.remove(state)
  #      new_inter.transition.pop(state)

#draw_graph(new_inter)
create_output(unified)
#print(len(new_inter.states))
#print("Given automaton is empty: ",empty(unified))

