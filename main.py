from hashlib import new
from venv import create
from buchi_automaton import *
from parse_BA_format import *
from draw_automaton import *
from union import *
from emptiness import *
from intersection import *
from output_BA_format import *
from edit_BA import *
from complement import *

buchiAutomaton_1 = create_automaton("inputs/example.ba")
draw_graph(complement(buchiAutomaton_1))