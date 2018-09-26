# Ass1 Question1
import os
import sys

def find_all(m, n):
    if m == len(M) - 1:
        return {'Sum': int(M[m][n]) + 0, 'Path': [int(M[m][n])], 'Count': 1}
#
    else:
        left = find_all(m + 1, n)
        right = find_all(m + 1, n + 1)
        if left['Sum'] > right['Sum']:
            return {'Sum': left['Sum'] + int(M[m][n]), 'Path': [int(M[m][n])] + left['Path'], 'Count': left['Count']}
        elif left['Sum'] == right['Sum']:
            return {'Sum': left['Sum'] + int(M[m][n]), 'Path': [int(M[m][n])] + left['Path'], 'Count': left['Count'] + right['Count']}
        else:
            return {'Sum': right['Sum'] + int(M[m][n]), 'Path': [int(M[m][n])] + right['Path'], 'Count': right['Count']}

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


result = find_all(0, 0)
print('The largest sum is:',result['Sum'])
print('The number of paths yielding this sum is:',result['Count'])
print('The leftmost path yielding this sum is:',result['Path'])
