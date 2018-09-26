import os
import sys
import copy

# inside return True
# outside return False
def check_point(x,y,self):
    N = copy.deepcopy(L)
    N.remove(self)
    for i in N:
        if i[0] <= x <= i[2] and i[1] <= y <= i[3]:
            return i
    return False

def check_retangle(retangle):
    R = copy.deepcopy(L)
    R.remove(retangle)
    for i in R:
        if i[0] <= retangle[0] and retangle[2] <= i[2] and i[1] <= retangle[1] and retangle[3] <= i[3]:
            return True
    return False

file_name = input('Which data file do you want to use? ')
if not os.path.exists(file_name):
    print(f'error')
    sys.exit()
# open files
with open(file_name) as data:
    #read line
    L = []
    for line in data:
        M = line.split()
        m = []
        for i in M:
            m.append(int(i))
        L.append(m)

# is the point inside of the rectangle?
perimeter = 0
for i in L:
    if i[0] < i[2] and i[1] < i[3]:
        x1 = i[0]
        y1 = i[1]
        x2 = i[2]
        y2 = i[3]
    if i[0] < i[2] and i[1] > i[3]:
        x1 = i[0]
        y1 = i[3]
        x2 = i[2]
        y2 = i[1]
    if i[0] > i[2] and i[1] < i[3]:
        x1 = i[2]
        y1 = i[1]
        x2 = i[0]
        y2 = i[3]
    if i[0] > i[2] and i[1] > i[3]:
        x1 = i[2]
        y1 = i[3]
        x2 = i[0]
        y2 = i[1]

    if check_retangle(i):
        continue

    # left line
    x = x1
    y = y1
    while y < y2:
        if not check_point(x, y, i):
            perimeter = perimeter + 1
        else:
            if not check_point(x, y+1, i):
                perimeter = perimeter + 1
        y = y + 1


    # lower line
    x = x1
    y = y1
    while x < x2:
        if not check_point(x, y, i):
            perimeter = perimeter + 1
        else:
            if not check_point(x+1, y, i):
                perimeter = perimeter +1
        x = x + 1


    # right line
    x = x2
    y = y1
    while y < y2:
        if not check_point(x, y, i):
            perimeter = perimeter + 1
        else:
            if not check_point(x, y+1, i):
                perimeter = perimeter + 1
        y = y + 1


    # upper line
    x = x1
    y = y2
    while x < x2:
        if not check_point(x, y, i):
            perimeter = perimeter + 1
        else:
            if not check_point(x+1, y, i):
                perimeter = perimeter + 1
        x = x + 1


print(f'The perimeter is: {perimeter}')
