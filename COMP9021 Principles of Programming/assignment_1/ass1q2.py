#Assignment1 Question2

import os
import sys
import math
import copy

def positive(M):
    for j in range(len(M)):
        if M[j] > 0:
            continue
        else:
            return True
    return False

file_name = input('Which data file do you want to use? ')

if not os.path.exists(file_name):
    print(f'error')
    sys.exit()

# open files
with open(file_name) as data:
    #read line
    M = []
    for line in data:
        M.append(line.split())

min_quantity = min(int(M[i][1]) for i in range(len(M)))
max_quantity = math.floor(sum(int(M[i][1]) for i in range(len(M))) / len(M))
ave_quantity = math.floor((max_quantity + min_quantity) / 2)

while min_quantity != ave_quantity:
    L = copy.deepcopy(M)
    for i in range(len(L)-1):
        trans = ave_quantity - int(L[i][1])
        distance = int(L[i+1][0]) - int(L[i][0])
        if trans <= 0:
            if abs(trans) <= abs(distance):
                trans = 0
                distance = 0
        L[i+1][1] = int(L[i+1][1]) - trans - distance

    if int(L[len(L)-1][1]) == ave_quantity or L[len(L)-1][1] == ave_quantity + 1:
        break
    elif L[len(L)-1][1] == ave_quantity - 1:
        ave_quantity = min_quantity
        break
    elif L[len(L)-1][1] > ave_quantity + 1:
        min_quantity = ave_quantity
        ave_quantity = math.floor((max_quantity + min_quantity) / 2)
    elif L[len(L)-1][1] < ave_quantity - 1 and L[len(L)-1][1] > 0:
        max_quantity = ave_quantity
        ave_quantity = math.floor((max_quantity + min_quantity) / 2)
    else:#lastnum<0
        max_quantity = ave_quantity
        ave_quantity = math.floor((max_quantity + min_quantity) / 2)

print(f'The maximum quantity of fish that each town can have is {ave_quantity}.')

