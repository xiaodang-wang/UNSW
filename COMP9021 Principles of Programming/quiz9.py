# Randomly generates a binary search tree whose number of nodes
# is determined by user input, with labels ranging between 0 and 999,999,
# displays it, and outputs the maximum difference between consecutive leaves.
#
# Written by *** and Eric Martin for COMP9021

import sys
from random import seed, randrange
from binary_tree_adt import *

# Possibly define some functions
def in_order(tree):
    if tree.left_node.value is None and tree.right_node.value is None:
        return [tree.value]
    if tree.left_node.value is None and tree.right_node.value is not None:
        return in_order(tree.right_node)        
    if tree.left_node.value is not None and tree.right_node.value is None:
        return in_order(tree.left_node)
    values = in_order(tree.left_node)
    values.extend(in_order(tree.right_node))
    return values

def max_diff_in_consecutive_leaves(tree):
    max_diff = 0
    list_of_consecutive_leaves = in_order(tree)
    for i in range(len(list_of_consecutive_leaves)-1):
        if (list_of_consecutive_leaves[i+1] - list_of_consecutive_leaves[i]) > max_diff:
            max_diff = list_of_consecutive_leaves[i+1] - list_of_consecutive_leaves[i]
    return max_diff
        
    

##provided_input = input('Enter two integers, the second one being positive: ')
##try:
##    arg_for_seed, nb_of_nodes = provided_input.split()
##except ValueError:
##    print('Incorrect input, giving up.')
##    sys.exit()
##try:
##    arg_for_seed, nb_of_nodes = int(arg_for_seed), int(nb_of_nodes)
##    if nb_of_nodes < 0:
##        raise ValueError
##except ValueError:
##    print('Incorrect input, giving up.')
##    sys.exit()
##seed(arg_for_seed)
##tree = BinaryTree()
##for _ in range(nb_of_nodes):
##    datum = randrange(1000000)
##    tree.insert_in_bst(datum)

tree = BinaryTree()

print('Here is the tree that has been generated:')
tree.print_binary_tree()
print('The maximum difference between consecutive leaves is: ', end = '')
print(max_diff_in_consecutive_leaves(tree))

