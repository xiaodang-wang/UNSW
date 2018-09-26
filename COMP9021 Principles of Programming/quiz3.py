# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for a given direction being
# one of N, E, S or W (for North, East, South or West) and for a given size greater than 1,
# the number of triangles pointing in that direction, and of that size.
#
# Triangles pointing North:
# - of size 2:
#   1
# 1 1 1
# - of size 3:
#     1
#   1 1 1
# 1 1 1 1 1
#
# Triangles pointing East:
# - of size 2:
# 1
# 1 1
# 1
# - of size 3:
# 1
# 1 1
# 1 1 1 
# 1 1
# 1
#
# Triangles pointing South:
# - of size 2:
# 1 1 1
#   1
# - of size 3:
# 1 1 1 1 1
#   1 1 1
#     1
#
# Triangles pointing West:
# - of size 2:
#   1
# 1 1
#   1
# - of size 3:
#     1
#   1 1
# 1 1 1 
#   1 1
#     1
#
# The output lists, for every direction and for every size, the number of triangles
# pointing in that direction and of that size, provided there is at least one such triangle.
# For a given direction, the possble sizes are listed from largest to smallest.
#
# We do not count triangles that are truncations of larger triangles, that is, obtained
# from the latter by ignoring at least one layer, starting from the base.
#
# Written by Xiaodan Wang and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def triangles_in_grid():
#North_grid
    N_grid = [[0]*(dim+2) for _ in range (dim+2)]
    for i in range (1, dim+1):
        for j in range (1, dim+1):
            if grid[i-1][j-1] !=0:
                N_grid[i][j] = 1

#West_grid    
    new_grid = N_grid.copy()
    new_grid.reverse()
    W_grid = [[0]*(dim+2) for _ in range (dim+2)]
    for i in range (dim+2):
        for j in range (dim+2):
            W_grid[i][j] = new_grid[j][i]

#South_grid    
    new_grid = W_grid.copy()
    new_grid.reverse()
    S_grid = [[0]*(dim+2) for _ in range (dim+2)]
    for i in range (dim+2):
        for j in range (dim+2):
            S_grid[i][j] = new_grid[j][i]

#East_grid    
    new_grid = S_grid.copy()
    new_grid.reverse()
    E_grid = [[0]*(dim+2) for _ in range (dim+2)]
    for i in range (dim+2):
        for j in range (dim+2):
            E_grid[i][j] = new_grid[j][i]
            
    N = triangles_on_one_direction(N_grid)
    S = triangles_on_one_direction(S_grid)
    W = triangles_on_one_direction(W_grid)
    E = triangles_on_one_direction(E_grid)
    
    dictionary = {}
    if N is not None:
        dictionary['N'] = N
    if S is not None:
        dictionary['S'] = S
    if W is not None:
        dictionary['W'] = W
    if E is not None:
        dictionary['E'] = E
    return dictionary
    # Replace return {} above with your code


def triangles_on_one_direction(new_grid):
    size = 1
    size_and_number = []
    
    for i in range (1, dim + 1):
        for j in range(1, dim + 1):
            
            if new_grid[i][j] == 1:
                
                while 0 not in new_grid[i+size][j-size:j+1+size]:
                    size = size + 1
                
                if size != 1:
                    size_and_number.append(size)
                    size = 1


    L = []
    if len(size_and_number) != 0:
        for i in range(max(size_and_number),1,-1):
            L.append((i,size_and_number.count(i))) 
        return L
    else:
        return


# Possibly define other functions

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are amongst 'N', 'E', 'S' and 'W',
# and whose values are pairs of the form (size, number_of_triangles_of_that_size),
# ordered from largest to smallest size.
triangles = triangles_in_grid()
for direction in sorted(triangles, key = lambda x: 'NESW'.index(x)):
    print(f'\nFor triangles pointing {direction}, we have:')
    for size, nb_of_triangles in triangles[direction]:
        triangle_or_triangles = 'triangle' if nb_of_triangles == 1 else 'triangles'
        print(f'     {nb_of_triangles} {triangle_or_triangles} of size {size}')

