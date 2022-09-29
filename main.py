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

buchiAutomaton_1 = BA_format("inputs/example.ba")
draw_graph(complement(buchiAutomaton_1))