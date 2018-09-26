import os
import sys

def last_point(x):
    if x in last_path_dict:
        M = last_path_dict.get(x)
        N = M
        for m in M:
            N = N.union(last_point(m))
    else:
        return set()
    return N

file_name = input('Which data file do you want to use? ')
if not os.path.exists(file_name):
    print(f'error')
    sys.exit()

# open files
with open(file_name) as data:
    #read line
    last_path_dict = {}
    reach_dict = {}
    L = set()
    origin_list = []
    for line in data:
        B = line.split()[0][2:-1].split(',')
        fr = B[0]
        to = B[1]
        L.add(fr)
        L.add(to)
        origin_list.append([fr,to])
        if to in last_path_dict:
            F = last_path_dict.get(to)
            F.add(fr)
            last_path_dict[to] = F
        else:
            last_path_dict[to] = set([fr])

        if fr in reach_dict:
            F = reach_dict.get(fr)
            F.add(to)
            reach_dict[fr] = F
        else:
            reach_dict[fr] = set([to])

path_dict = {}
remove_list = []

for i in L:
    path_dict[i] = last_point(i)
x = 0
for i in origin_list:
    if reach_dict[i[0]].intersection(path_dict[i[1]]):
        remove_list.append(i)
    if i in origin_list[0:x]:
        remove_list.append(i)
    x = x + 1
for i in remove_list:
    origin_list.remove(i)

print('The nonredundant facts are:')
for i in origin_list:
    print(f'R({i[0]},{i[1]})')


