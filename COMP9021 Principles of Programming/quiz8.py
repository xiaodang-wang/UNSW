# Randomly fills a grid of size 10 x 10 with 0s and 1s,
# in an estimated proportion of 1/2 for each,
# and computes the longest leftmost path that starts
# from the top left corner -- a path consisting of
# horizontally or vertically adjacent 1s --,
# visiting every point on the path once only.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange

from queue_adt import *
from copy import deepcopy


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

def leftmost_longest_path_from_top_left_corner():
    # modify grid?
    new_grid = [[0]*12 for _ in range (12)]
    for i in range (1, 11):
        for j in range (1, 11):
            new_grid[i][j] = grid[i-1][j-1]
    #print(new_grid)

    longest_path = []
    # queue
    queue=Queue()
    # (path, next tree leaves)
    tree = {}
    path = []
    if new_grid[1][1] == 1:
        tree = {(1,1): []}
        path = [(1,1)]
        if new_grid[2][1] == 1:
            tree[(1,1)].append((2,1))
        if new_grid[1][2] == 1:
            tree[(1,1)].append((1,2))

    #print(tree)
    # tree = {(1,1):[[(2,1),(1,2)]}

    queue.enqueue((path,tree,new_grid))
    while not queue.is_empty():
        path, tree, new_grid = queue.dequeue()
        if len(path) >= len(longest_path):
            longest_path = path
        #print(path)
        #print(tree)
        #print(new_grid)
        if tree:
            for last_pos in tree:
                if tree[last_pos]:
                    for now_pos in tree[last_pos]:
                        # check direction
                        (a,b) = last_pos
                        (c,d) = now_pos

                        changed_grid = deepcopy(new_grid)
                        changed_grid[a][b] = '*'
                        #print(changed_grid)
                        
                        # east
                        if c-a == 0 and d-b == 1:
                            new_tree = {(c,d): []}
                            if changed_grid[c+1][d] == 1:
                                new_tree[(c,d)].append((c+1,d))
                            if changed_grid[c][d+1] == 1:
                                new_tree[(c,d)].append((c,d+1))
                            if changed_grid[c-1][d] == 1:
                                new_tree[(c,d)].append((c-1,d))
                        #print(new_tree)
                            queue.enqueue((path + [(c,d)],new_tree,changed_grid))
                        #print(path + [(c,d)])
                            continue
                    
                        # south
                        if c-a == 1 and d-b == 0:
                            new_tree = {(c,d): []}
                            if changed_grid[c][d-1] == 1:
                                new_tree[(c,d)].append((c,d-1))
                            if changed_grid[c+1][d] == 1:
                                new_tree[(c,d)].append((c+1,d))
                            if changed_grid[c][d+1] == 1:
                                new_tree[(c,d)].append((c,d+1))                                
                            queue.enqueue((path + [(c,d)],new_tree,changed_grid))
                            continue

                        # west
                        if c-a == 0 and b-d == 1:
                            new_tree = {(c,d): []}
                            if changed_grid[c-1][d] == 1:
                                new_tree[(c,d)].append((c-1,d))
                            if changed_grid[c][d-1] == 1:
                                new_tree[(c,d)].append((c,d-1))
                            if changed_grid[c+1][d] == 1:
                                new_tree[(c,d)].append((c+1,d))                                
                            queue.enqueue((path + [(c,d)],new_tree,changed_grid))
                            continue

                        # north
                        if a-c == 1 and d-b == 0:
                            new_tree = {(c,d): []}
                            if changed_grid[c][d+1] == 1:
                                new_tree[(c,d)].append((c,d+1))
                            if changed_grid[c-1][d] == 1:
                                new_tree[(c,d)].append((c-1,d))
                            if changed_grid[c][d-1] == 1:
                                new_tree[(c,d)].append((c,d-1))                                
                            queue.enqueue((path + [(c,d)],new_tree,changed_grid))
                            continue
    longest_leftmost_path = []
    for t in longest_path:
        (x,y)=t
        longest_leftmost_path.append((x-1,y-1))
    return longest_leftmost_path
    
    # Replace pass above with your code


provided_input = input('Enter one integer: ')
try:
    for_seed = int(provided_input)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(2) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
path = leftmost_longest_path_from_top_left_corner()
if not path:
    print('There is no path from the top left corner.')
else:
    print(f'The leftmost longest path from the top left corner is: {path})')
           
