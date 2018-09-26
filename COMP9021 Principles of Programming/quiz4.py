# Uses National Data on the relative frequency of given names in the population of U.S. births,
# stored in a directory "names", in files named "yobxxxx.txt with xxxx being the year of birth.
#
# Prompts the user for a first name, and finds out the first year
# when this name was most popular in terms of frequency of names being given,
# as a female name and as a male name.
# 
# Written by Xiaodan Wang and Eric Martin for COMP9021


import os


first_name = input('Enter a first name: ')
directory = 'names'
min_male_frequency = 0
male_first_year = None
min_female_frequency = 0
female_first_year = None

# Replace this comment with your code

for filename in sorted(os.listdir(directory),reverse = True):
    if not filename.endswith('.txt'):
        continue
    
    # new file
    # initial
    total_female = 0
    total_male = 0
    name_count_female = {}
    name_count_male = {}
    
    # open files
    with open(directory + '/' + filename) as data:
        #read line
        for line in data:
            name, gender, count = line.split(',')
            # distinguished by gender
            # {name: count}, total_count
            if gender == 'F':
                name_count_female[name] = int(count)
                total_female = total_female + int(count)
            else:
                name_count_male[name] = int(count)
                total_male = total_male + int(count)
    # max earliest frequence
    if first_name in name_count_female:
        if int(name_count_female.get(first_name)) / total_female * 100 > min_female_frequency:
            min_female_frequency = int(name_count_female.get(first_name)) / total_female * 100
            female_first_year = int(filename[3:7])
    
    if first_name in name_count_male:
        if int(name_count_male.get(first_name)) / total_male * 100 > min_male_frequency:
            min_male_frequency = int(name_count_male.get(first_name)) / total_male * 100
            male_first_year = int(filename[3:7])
            
            
if not female_first_year:
    print(f'In all years, {first_name} was never given as a female name.')
else:
    print(f'In terms of frequency, {first_name} was the most popular '
          f'as a female name first in the year {female_first_year}.\n'
          f'  It then accounted for {min_female_frequency:.2f}% of all female names.'
         )
if not male_first_year:
    print(f'In all years, {first_name} was never given as a male name.')
else:
    print(f'In terms of frequency, {first_name} was the most popular '
          f'as a male name first in the year {male_first_year}.\n'
          f'  It then accounted for {min_male_frequency:.2f}% of all male names.'
         )
