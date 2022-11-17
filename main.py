from hashlib import new
from venv import create
from buchi_automaton import *
from parser import *
#from draw_automaton import *
from parser import HOA_format
from union import *
from emptiness import *
from intersection import *
from output import *
from edit_BA import *
from complement import *

import sys

#######################################################
#              START OF PARSING ARGS                  #           
#######################################################
description_file = sys.argv[1]
if description_file[-4:] == ".hoa":
    format = 0
elif description_file[-3:] == ".ba":
    format = 1
else:
    pass
    #print("Invalid arguments!\n")
    #exit(1)

format = 0

rightmost_2s = False
merge_states = False
add_color_3 = False
for i in sys.argv[2:]:
    if i == "0":
        rightmost_2s = True
        break
    elif i == "1":
        merge_states = True
    elif i == "2":
        add_color_3 = True
        break
    else:
        print("Invalid arguments!\n")
        exit(1)
#######################################################
#                END OF PARSING ARGS                  #           
#######################################################

if format == 0:
    buchiAutomaton = HOA_format(description_file)
else:
    buchiAutomaton = BA_format(description_file)

complemented = complement(buchiAutomaton,rightmost_2s,merge_states,add_color_3)

#draw_graph(complemented)
output_HOA_format(complemented)

f = open("output.hoa", "r")
print(f.read())
f.close()