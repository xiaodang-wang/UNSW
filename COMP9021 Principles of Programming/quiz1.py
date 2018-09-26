# Written by Xiaodan Wang and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers at most equal to a given upper bound,
of a given length, all controlled by user input.

Outputs four lists:
- elements_to_keep, consisting of L's smallest element, L's third smallest element,
  L's fifth smallest element, ...
  Hint: use sorted(), list slices, and set()
- L_1, consisting of all members of L which are part of elements_to_keep, preserving
  the original order
- L_2, consisting of the leftmost occurrences of the members of L which are part of
  elements_to_keep, preserving the original order
- L_3, consisting of the LONGEST, and in case there are more than one candidate, the
  LEFTMOST LONGEST sequence of CONSECUTIVE members of L that reduced to a set,
  is a set of integers without gaps.
'''


import sys
from random import seed, randint


try:
    arg_for_seed, upper_bound, length = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, upper_bound, length = int(arg_for_seed), int(upper_bound), int(length)
    if arg_for_seed < 0 or upper_bound < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, upper_bound) for _ in range(length)]
print('\nThe generated list L is:')
print('  ', L)

L_1 = []
L_2 = []
L_3 = []
elements_to_keep = []

# Replace this comment with your code
# elements_to_keep
M = []
M = sorted(set(L))
elements_to_keep = M[::2]
# or:
# keep 1st 3rd 5th... smallest num
# keep M[0] M[2] M[4]...
#for i in range(len(M)):
#    if i%2 == 0:
#        elements_to_keep.append(M[i])

# L_1
# compare L and elements_to_keep one by one
for m in range(len(L)):
    for n in range(len(elements_to_keep)):
        if L[m] == elements_to_keep[n]:
            L_1.append(L[m])
            
# L_2
# compare L_1 with L_2(EMPTY) to fill L_2
for j in range(len(L_1)):
    if not L_1[j] in L_2:
        L_2.append(L_1[j])
        
# L_3
# use slices get M1 to judge whether M1 is consecutive 
# in length order from longest to shortest(2 numbers)
def determine_L3(L):
    exit_flag = 1
    for x in range(len(L)):
        if x < len(L)-1:
            for y in range(x+1):
                M1 = L[y:len(L)-x+y]

            # judge M1
                M2 = []
                M2 = sorted(set(M1))
                if M2[-1] - M2[0] == len(M2)-1:
                    return M1
                    #L_3 = M1
                # out of loops with flag
                # or use return
                    exit_flag = 0
                    break
            if exit_flag == 0:
                break
    #incase there is no consecutive numbers
        else:
            L_3 = 'no consecutive numbers'

L_3 = determine_L3(L)
    
print('\nThe elements to keep in L_1 and L_2 are:')
print('  ', elements_to_keep)
print('\nHere is L_1:')
print('  ', L_1)
print('\nHere is L_2:')
print('  ', L_2)
print('\nHere is L_3:')
print('  ', L_3)
