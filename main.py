from hashlib import new
from venv import create
from buchi_automaton import *
from parser import *
from draw_automaton import *
from union import *
from emptiness import *
from intersection import *
from output import *
from edit_BA import *
from complement import *

description_file = "inputs/in.hoa"

buchiAutomaton_1 = HOA_format(description_file)
complemented = complement(buchiAutomaton_1)
draw_graph(complemented)
output_HOA_format(complemented,description_file)