# Written by *** and Eric Martin for COMP9021


'''
Prompts the user for two strictly positive integers, numerator and denominator.

Determines whether the decimal expansion of numerator / denominator is finite or infinite.

Then computes integral_part, sigma and tau such that numerator / denominator is of the form
integral_part . sigma tau tau tau ...
where integral_part in an integer, sigma and tau are (possibly empty) strings of digits,
and sigma and tau are as short as possible.
'''


import sys
from math import gcd


try:
    numerator, denominator = input('Enter two strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    numerator, denominator = int(numerator), int(denominator)
    if numerator <= 0 or denominator <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


has_finite_expansion = False
integral_part = 0
sigma = ''
tau = ''

# Replace this comment with your code
sigma_list = []
remainder_set = set()
remainder_list = []

integral_part = numerator // denominator
remainder =  numerator % denominator

i = 0
tau_flag = False

while remainder != 0:   
    if remainder in remainder_set:
        tau_flag = True
        break
    remainder_set.add(remainder)
    sigma_list.append(remainder * 10 // denominator)
    remainder = remainder * 10 % denominator
    i += 1

if not tau_flag:
    #has finite expansion
    has_finite_expansion = True   
    sigma = ''.join('%s'%id for id in sigma_list)
else:
    #has no finite expansion
    remainder_1 = numerator % denominator
    #use while not for 
    #j == tau_begin_at
    for j in range (i):
        remainder_list.append(remainder_1)
        remainder_1 = remainder_1 * 10 % denominator
        
        if remainder == remainder_list[j]:
            sigma = ''.join('%s'%id for id in sigma_list[0:j])
            tau = ''.join('%s'%id for id in sigma_list[j:i])
            break

if has_finite_expansion:
    print(f'\n{numerator} / {denominator} has a finite expansion')
else:
    print(f'\n{numerator} / {denominator} has no finite expansion')
if not tau:
    if not sigma:
        print(f'{numerator} / {denominator} = {integral_part}')
    else:
        print(f'{numerator} / {denominator} = {integral_part}.{sigma}')
else:
    print(f'{numerator} / {denominator} = {integral_part}.{sigma}({tau})*')


