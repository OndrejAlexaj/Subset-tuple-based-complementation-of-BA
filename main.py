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

buchiAutomaton_1 = HOA_format("inputs/in.hoa")
draw_graph(buchiAutomaton_1)