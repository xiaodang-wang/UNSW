# Randomly fills a grid of size 10 x 10 with 0s and 1s and computes:
# - the size of the largest homogenous region starting from the top left corner,
#   so the largest region consisting of connected cells all filled with 1s or
#   all filled with 0s, depending on the value stored in the top left corner;
# - the size of the largest area with a checkers pattern.
#
# Written by Xiaodan Wang and Eric Martin for COMP9021

import sys
from random import seed, randint


dim = 10
grid = [[None] * dim for _ in range(dim)]

def display_grid():
    for i in range(dim):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

# Possibly define other functions
def homogenous_region(i, j, flag):
    # base case 1
    # lowest of list
    if i == 9 and j <= 8:
        if grid[i][j] != 2:
            if grid[i][j] == flag:
                grid[i][j] = 2
                return 1 + homogenous_region(i, j+1, flag)
            else:
                grid[i][j] = 2
                return int(0)
        return int(0)

    # base case 1
    # rightest of list
    if j == 9 and i <= 8:
        if grid[i][j] != 2:
            if grid[i][j] == flag:
                grid[i][j] = 2
                return 1 + homogenous_region(i+1, j, flag)
            else:
                grid[i][j] = 2
                return int(0)
        return int(0)
    # base case 3
    # rl conner
    if i == 9 and j == 9:
        if grid[i][j] != 2:
            if grid[i][j] == flag:
                grid[i][j] = 2
                return int(1)
            else:
                grid[i][j] = 2
                return int(0)
        return int(0)
    # recursion
    if i<9 and j<9:
        if grid[i][j] != 2:
            if grid[i][j] == flag:
                grid[i][j] = 2
                return 1 + homogenous_region(i, j+1, flag) + homogenous_region(i+1, j, flag)
            else:
                grid[i][j] = 2
                return int(0)
        return int(0)


try:
    arg_for_seed, density = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density = int(arg_for_seed), int(density)
    if arg_for_seed < 0 or density < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
# We fill the grid with randomly generated 0s and 1s,
# with for every cell, a probability of 1/(density + 1) to generate a 0.
for i in range(dim):
    for j in range(dim):
        grid[i][j] = int(randint(0, density) != 0)
print('Here is the grid that has been generated:')
display_grid()

size_of_largest_homogenous_region_from_top_left_corner  = 0
# Replace this comment with your code
size_of_largest_homogenous_region_from_top_left_corner = homogenous_region(0,0,grid[0][0])

print('The size_of the largest homogenous region from the top left corner is '
      f'{size_of_largest_homogenous_region_from_top_left_corner}.'
     )

max_size_of_region_with_checkers_structure = 0
# Replace this comment with your code
print('The size of the largest area with a checkers structure is '
      f'{max_size_of_region_with_checkers_structure}.'
     )



