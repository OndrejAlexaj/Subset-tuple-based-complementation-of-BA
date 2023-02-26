from hashlib import new
from venv import create
from buchi_automaton import *
from parse_files import *
from draw_automaton import *
from parse_files import HOA_format
from union import *
from emptiness import *
from intersection import *
from output import *
from edit_BA import *
from complement import *

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

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
delay = False

if sys.argv[2] == "1":
    rightmost_2s = True
elif sys.argv[2] == "2":
    merge_states = True
elif sys.argv[2] == "3":
    rightmost_2s = True
    merge_states = True
elif sys.argv[2] == "4":
    add_color_3 = True
elif sys.argv[2] == "5":
    rightmost_2s = True
    merge_states = True
    delay = True
else:
    print("Invalid arguments!\n")
    exit(1)

acc_type = ""
if sys.argv[3] == "state":
    acc_type = "state"
elif sys.argv[3] == "trans":
    acc_type = "trans"
else:
    print("Invalid arguments!\n")
    exit(1)
#######################################################
#                END OF PARSING ARGS                  #           
#######################################################

if format == 0:
    buchiAutomaton = HOA_format(description_file,acc_type)
else:
    buchiAutomaton = BA_format(description_file)

complemented = complement(buchiAutomaton,rightmost_2s,merge_states,add_color_3,delay,acc_type)

draw_graph(complemented, "")
if(acc_type == "state"):
    output_HOA_format_state(complemented)
else:
    output_HOA_format_trans(complemented)

f = open("output.hoa", "r")
print(f.read())
f.close()

#print(complemented.states)