import math
import numpy as np
import sys
import time
str_list = '59777098810822000809394624382157501556909810502346287077282177428724322323272236375412105805609092414782740710425184516236183547622345203164275191671720865872461284041797089470080366457723972985763645873208418782378044815481530554798953528896905275975178449123276858904407462285078456817038667669183420974001025093760473977009037844415364079145612611938513254763581971458140349825585640285658557835032882311363817855746737733934576748280568150394709654438729776867932430014255649458605325527757230466997043406136400716198065838842158274093116050506775489075879316061475634889155814030818530064869767243196343272137745926937355015378474209347100518533'*10000
# str_list = "03081770884921959731165446850517"*10000
sequence = list(str_list)
start_num = int(str_list[:7])

output_sequence = []
for i in range(start_num, len(sequence)):
    output_sequence.append(int(sequence[i]))
sequence = np.array(output_sequence)

for i in range(100):
    running_sum = 0
    for sequence_num in range(len(sequence) - 1, -1, -1):
        running_sum = int(str(running_sum + sequence[sequence_num])[-1])
        sequence[sequence_num] = running_sum
    print_str = ""
    for j in range(0, 8):
        print_str += str(sequence[j])
    print(print_str)
    sys.stdout.flush()