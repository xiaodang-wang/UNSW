# Written by Xiaodan Wang for COMP9021 Assignment_2

import os
import re
import numpy
import copy

class FileNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class FriezeError(Exception):
    def __init__(self, message):
        self.message = message

class Frieze:
    def __init__(self, filename = None):
        self.filename = filename        
        # FileNotFoundError
        if self.filename not in os.listdir('.'):
            raise FileNotFoundError('')       
        # open file & read file into data[][]
        with open(self.filename) as file:
            data = []
            line_data = []
            data_set = set()
            length = None
            for line in file:
                # FriezeError: Incorrect input.
                # case1 not ' 'or num type
                wrong_input = re.findall('[^ \d\n]',line)
                if wrong_input != []:
                    raise FriezeError('Incorrect input.')
                for num in line.split():
                    line_data.append(num)
                if line_data != []:
                    # case 2 length equality
                    if length is not None and length != len(line_data):
                        raise FriezeError('Incorrect input.')
                    length = len(line_data)
                    data.append(line_data)
                    data_set.update(set(line_data))
                    line_data = []
        data_numpy = numpy.array(data)
        self.data = data_numpy.astype(numpy.int32)
        (height,length) = self.data.shape
        self.height = height
        self.length = length
        # for special case change the last line into first line
        first_col = numpy.array(self.data[:,0])[:,numpy.newaxis]
        self.changed_data = self.data[:,:-1]
        self.changed_data = numpy.c_[self.changed_data,first_col]
        # FriezeError: Incorrect input.
        # case3 beyound {0-15}
        if (self.data > 15).any():
            raise FriezeError('Incorrect input.')            
        # case4 height&length
        if height < 3 or height > 17:
            raise FriezeError('Incorrect input.')
        if length < 5 or length > 51:
            raise FriezeError('Incorrect input.')       
        # FriezeError: Input does not represent a frieze.
        # case1 topline
        top_line = self.data[0][:-1]
        for i in set(top_line):
            if i not in {4,12}:
                raise FriezeError('Input does not represent a frieze.')
        end_of_top_line = self.data[0][-1]
        if end_of_top_line != 0:
            raise FriezeError('Input does not represent a frieze.')
        # case2 bottomline
        bottom_line = self.data[-1][:-1]
        for i in set(bottom_line):
            if i not in {4,5,6,7}:
                raise FriezeError('Input does not represent a frieze.')
        end_of_bottom_line = self.data[-1][-1]
        if end_of_bottom_line not in {0,1}:
            raise FriezeError('Input does not represent a frieze.')
        self.N = set()
        self.NE = set()
        self.E = set()
        self.SE = set()
        self.classify()
        self.classify_display()
        # case3 crossing
        if not self.no_crossing():
            raise FriezeError('Input does not represent a frieze.')
        # case4 left should equal to right border
        if 0 not in self.dis_n:
            if length - 1 in self.dis_n:
                raise FriezeError('Input does not represent a frieze.')
        else:
            if length - 1 not in self.dis_n:
                raise FriezeError('Input does not represent a frieze.')
            else:
                if self.dis_n[0] != self.dis_n[length - 1]:
                    raise FriezeError('Input does not represent a frieze.')
        # case5
        right_border_set = set(self.data[:,-1])
        for e in right_border_set:
            if e not in {0,1}:
                raise FriezeError('Input does not represent a frieze.')
        # case6 periods
        find_period = False
        for i in range(1,int(length/2)+1):
            if (self.data[:,:1] == self.data[:,i:i+1]).all() and (length - 1) % i == 0:
                period = i
                for n in range(period):
                    for m in range(n, length-1, period):
                        if (self.data[:,m:m+1] != self.data[:,n:n+1]).any():
                            break
                    else:
                        continue
                    break
                if m == length - 2 and n == period - 1:
                    find_period = True
                    break
                else:
                    continue
        if not find_period:
            raise FriezeError('Input does not represent a frieze.')
        if period < 2 or period * 2 > length - 1:
            raise FriezeError('Input does not represent a frieze.')
        self.period = period
        
    def display(self):
        with open(f'{self.filename[:-4]}.tex','w') as latex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage{tikz}\n'
                  '\\usepackage[margin=0cm]{geometry}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\vspace*{\\fill}\n'
                  '\\begin{center}\n'
                  '\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]', file = latex_file
                )
            # N
            print('% North to South lines', file = latex_file)
            n_list = self.display_list(self.dis_n)
            for e in sorted(n_list.keys()):
                for (x,y) in n_list[e]:
                    print(f'    \\draw ({e},{x}) -- ({e},{y});', file = latex_file)
            # SE
            print('% North-West to South-East lines', file = latex_file)
            se_list = self.display_list(self.dis_se)
            se_list_p = []
            for e in se_list:
                for (x,y) in se_list[e]:
                    se_list_p.append((x-e+1,x+1,y-e+1,y+1))
            for e in sorted(se_list_p, key = lambda x:(x[1],x[0])):
                print(f'    \\draw ({e[0]},{e[1]}) -- ({e[2]},{e[3]});', file=latex_file)
            # E
            print('% West to East lines', file = latex_file)
            e_list = self.display_list(self.dis_e)
            for e in sorted(e_list.keys()):
                for (x,y) in e_list[e]:
                    print(f'    \\draw ({x+1},{e}) -- ({y+1},{e});', file = latex_file)
            # NE
            print('% South-West to North-East lines', file = latex_file)
            ne_list_p = []
            ne_list = self.display_list(self.dis_ne)
            for e in ne_list:
                for (x,y) in ne_list[e]:
                    ne_list_p.append((e-y,y,e-x,x))
            for e in sorted(ne_list_p, key = lambda x:(x[1],x[0])):
                print(f'    \\draw ({e[0]},{e[1]}) -- ({e[2]},{e[3]});', file = latex_file)            
            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n'
                  '\n'
                  '\\end{document}', file = latex_file
                 )
    # turn dict{set()} into ordered list dict{list[]}
    def display_list(self,origin_dict):
        d = {}
        for x in sorted(origin_dict.keys()):
            x_list = self.combine(origin_dict[x])
            d[x] = x_list
        return d
    
    # combine consective elements
    def combine(self, origin_set):
        L = [(sorted(origin_set)[0]-1,sorted(origin_set)[0])]
        for e in sorted(origin_set)[1:]:
            if e-1 == L[-1][1]:
                L[-1] = (L[-1][0],e)
            else:
                L.append((e-1,e))
        return L
                
    # classify dict N NE E SE       
    def classify_display(self):
        # N  {1,3,5,7,9,11,13,15}
        self.dis_n = {}
        for [x,y] in numpy.argwhere((self.data == 1)|(self.data == 3)|\
                                    (self.data == 5)|(self.data == 7)|\
                                    (self.data == 9)|(self.data == 11)|\
                                    (self.data == 13)|(self.data == 15)):
            if y in self.dis_n:
                self.dis_n[y].add(x)
            else:
                self.dis_n[y] = {x}            
        # NE {2,3,6,7,10,11,14,15}
        self.dis_ne = {}
        for [x,y] in numpy.argwhere((self.data == 2)|(self.data == 3)|\
                                    (self.data == 6)|(self.data == 7)|\
                                    (self.data == 10)|(self.data == 11)|\
                                    (self.data == 14)|(self.data == 15)):
            if (x+y) in self.dis_ne:
                self.dis_ne[x + y].add(x)
            else:
                self.dis_ne[x + y] = {x} 
        # E  {4,5,6,7,12,13,14,15}
        self.dis_e = {}
        for [x,y] in numpy.argwhere((self.data == 4)|(self.data == 5)|\
                                    (self.data == 6)|(self.data == 7)|\
                                    (self.data == 12)|(self.data == 13)|\
                                    (self.data == 14)|(self.data == 15)):
            if x in self.dis_e:
                self.dis_e[x].add(y)
            else:
                self.dis_e[x] = {y} 
        # SE {8,9,10,11,12,13,14,15}
        self.dis_se = {}
        for [x,y] in numpy.argwhere((self.data == 8)|(self.data == 9)|\
                                    (self.data == 10)|(self.data == 11)|\
                                    (self.data == 12)|(self.data == 13)|\
                                    (self.data == 14)|(self.data == 15)):
            if (x-y) in self.dis_se:
                self.dis_se[x - y].add(x)
            else:
                self.dis_se[x - y] = {x}

    def no_crossing(self):
        for (x,y) in self.NE:
            if (x-1,y) in self.SE:
                return False
        return True
    
    # classify dict N NE E SE       
    def classify(self):
        # N  {1,3,5,7,9,11,13,15}
        for [x,y] in numpy.argwhere((self.changed_data == 1)|(self.changed_data == 3)|\
                                    (self.changed_data == 5)|(self.changed_data == 7)|\
                                    (self.changed_data == 9)|(self.changed_data == 11)|\
                                    (self.changed_data == 13)|(self.changed_data == 15)):
            self.N.add((x,y))
        # NE {2,3,6,7,10,11,14,15}
        for [x,y] in numpy.argwhere((self.changed_data == 2)|(self.changed_data == 3)|\
                                    (self.changed_data == 6)|(self.changed_data == 7)|\
                                    (self.changed_data == 10)|(self.changed_data == 11)|\
                                    (self.changed_data == 14)|(self.changed_data == 15)):
            self.NE.add((x,y))
        # E  {4,5,6,7,12,13,14,15}
        for [x,y] in numpy.argwhere((self.changed_data == 4)|(self.changed_data == 5)|\
                                    (self.changed_data == 6)|(self.changed_data == 7)|\
                                    (self.changed_data == 12)|(self.changed_data == 13)|\
                                    (self.changed_data == 14)|(self.changed_data == 15)):
            self.E.add((x,y))
        # SE {8,9,10,11,12,13,14,15}
        for [x,y] in numpy.argwhere((self.changed_data == 8)|(self.changed_data == 9)|\
                                    (self.changed_data == 10)|(self.changed_data == 11)|\
                                    (self.changed_data == 12)|(self.changed_data == 13)|\
                                    (self.changed_data == 14)|(self.changed_data == 15)):
            self.SE.add((x,y))

    def analyse(self):
        horizontal = self.horizontal()
        vertical = self.vertical()
        glided_horizontal = self.glided_horizontal()
        rotation = self.rotation()
        if not horizontal and not vertical and not glided_horizontal and not rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation only.')
        if not horizontal and vertical and not glided_horizontal and not rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and vertical reflection only.')
        if horizontal and not vertical and not glided_horizontal and not rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and horizontal reflection only.')
        if not horizontal and not vertical and glided_horizontal and not rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and glided horizontal reflection only.')
        if not horizontal and not vertical and not glided_horizontal and rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and rotation only.')
        if not horizontal and vertical and glided_horizontal and rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        glided horizontal and vertical reflections, and rotation only.')
        if horizontal and vertical and not glided_horizontal and rotation:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        horizontal and vertical reflections, and rotation only.')

    def rotation(self):        
        for move in range(self.period):
            if self.height % 2 == 0:
                # rotation for even s.height
                # with point on the point
                if self.rotation_odd_height_even(move):
                    return True
                # with point on the interval
                if self.rotation_odd_height_odd(move):
                    return True
            else:
                if self.rotation_even_height_even(move):
                    return True
                if self.rotation_even_height_odd(move):
                    return True                
        return False


    def vertical(self):
        for move in range(self.period):
            if self.vertical_even(move):
                return True
            if self.vertical_odd(move):
                return True
        return False

    def glided_horizontal(self):
        if self.period % 2 == 0:
            if self.height % 2 == 0:
                return self.glided_horizontal_even()
            else:
                return self.glided_horizontal_odd()
        else:
            return False

    def horizontal(self):
        if self.height % 2 == 0:
            return self.horizontal_even()
        else:
            return self.horizontal_odd()

    def horizontal_odd(self):
        lower_N = set()
        changed_N = set()
        changed_NE = set()
        lower_SE = set()
        changed_E = set()
        lower_E = set()
        changed_SE = set()
        lower_NE = set()
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2+1) and y in range(self.period):
                changed_N.add(((x + (self.height//2 - x) *2 +1),y))
            elif x in range(self.height//2+1, self.height) and y in range(self.period):
                lower_N.add((x, y))
        if changed_N ^ lower_N:
            return False
        # NE -- SE
        for (x,y) in self.NE:
            if x in range(1, self.height//2+1) and y in range(self.period):
                changed_NE.add(((x + (self.height//2 - x) *2),y))
            elif x in range(self.height//2 + 1, self.height) and y in range(self.period):
                lower_NE.add((x, y))
        for (x,y) in self.SE:
            if x in range(self.height//2, self.height - 1) and y in range(self.period):
                lower_SE.add((x, y))
            elif x in range(self.height//2) and y in range(self.period):
                changed_SE.add(((x + (self.height//2 - x)*2),y))
        if changed_NE ^ lower_SE:
            return False
        if changed_SE ^ lower_NE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1, self.height//2) and y in range(self.period):
                changed_E.add(((x + (self.height//2 - x) *2),y))
            elif x in range(self.height//2+1, self.height - 1) and y in range(self.period):
                lower_E.add((x, y))               
        if changed_E ^ lower_E:
            return False
        return True

    def horizontal_even(self):
        changed_NE = set()
        lower_SE = set()
        lower_NE = set()
        changed_SE = set()
        changed_N = set()
        lower_N = set()
        changed_E = set()
        lower_E = set()
        # NE
        for (x,y) in self.NE:
            if x == self.height//2:
                return False
            elif x in range(1, self.height//2) and y in range(self.period):
                changed_NE.add((x+(self.height//2-x)*2-1,y))
            elif x in range(self.height//2+1, self.height) and y in range(self.period):
                lower_NE.add((x,y))       
        # SE
        for (x,y) in self.SE:
            if x == self.height//2 - 1:
                return False
            elif x in range(self.height//2, self.height - 1) and y in range(self.period):
                lower_SE.add((x,y))
            elif x in range(self.height//2-1) and y in range(self.period):
                changed_SE.add((x+(self.height//2-x)*2-1,y))
        if changed_NE ^ lower_SE:
            return False
        if changed_SE ^ lower_NE:
            return False       
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2) and y in range(self.period):
                changed_N.add((x+(self.height//2-x)*2,y))
            elif x in range(self.height//2 + 1,self.height) and y in range(self.period):
                lower_N.add((x,y))
        if changed_N ^ lower_N:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1,self.height//2) and y in range(self.period):
                changed_E.add((x+(self.height//2-x)*2-1,y))
            elif x in range(self.height//2,self.height-1) and y in range(self.period):
                lower_E.add((x,y))
        if changed_E ^ lower_E:
            return False
        return True

    def vertical_even(self, move):
        changed_N = set()
        right_N = set()
        changed_NE = set()
        right_SE = set()
        changed_E = set()
        right_E = set()
        changed_SE = set()
        right_NE = set()
        # axis
        if self.period % 2 == 1:
            period = self.period +1
        else:
            period = self.period        
        # N
        for (x,y) in self.N:
            if x in range(1, self.height) and y in range(move+1, period//2 + move):
                changed_N.add((x,y+(period//2-y+move)*2))
            elif x in range(1, self.height) and y in range(period//2+move+1, move+period):
                right_N.add((x, y))
        if changed_N ^ right_N:
            return False
        # NE
        for (x,y) in self.NE:
            if x in range(1, self.height) and y in range(move, period//2 + move):
                changed_NE.add((x-1,y+(period//2-y+move)*2-1))
            elif x in range(1, self.height) and y in range(period//2+move, move+period):
                right_NE.add((x, y))
        # SE
        for (x,y) in self.SE:
            if x in range(self.height - 1) and y in range(period//2+move, move+period):
                right_SE.add((x, y))
            elif x in range(self.height - 1) and y in range(move, period//2 + move):
                changed_SE.add((x+1,y+(period//2-y+move)*2-1))
        if changed_NE ^ right_SE:
            return False
        if changed_SE ^ right_NE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1, self.height - 1) and y in range(move, move+period//2):
                changed_E.add((x,y+(period//2-y+move)*2-1))
            elif x in range(1, self.height - 1) and y in range(move+period//2, move+period):
                right_E.add((x, y))               
        if changed_E ^ right_E:
            return False
        return True

    def vertical_odd(self,move):
        changed_NE = set()
        right_SE = set()
        right_NE = set()
        changed_SE = set()
        changed_N = set()
        right_N = set()
        changed_E = set()
        right_E = set()
        # axis
        if self.period % 2 == 1:
            period = self.period + 1
        else:
            period = self.period       
        # NE
        for (x,y) in self.NE:
            if y == period//2 + move:
                return False
            elif x in range(1, self.height) and y in range(move, period//2 + move):
                changed_NE.add((x-1,y+(period//2-y+move)*2))
            elif x in range(1, self.height) and y in range(period//2+move+1, move+period):
                right_NE.add((x,y))       
        # SE
        for (x,y) in self.SE:
            if y == self.period//2 + move:
                return False
            elif x in range(self.height - 1) and y in range(period//2+move+1, move+period+1):
                right_SE.add((x,y))
            elif x in range(self.height - 1) and y in range(move, period//2 + move):
                changed_SE.add((x+1,y+(period//2-y+move)*2))               
        if changed_NE ^ right_SE:
            return False
        if changed_SE ^ right_NE:
            return False
        # N
        for (x,y) in self.N:
            if x in range(1, self.height) and y in range(move+1, period//2 + move+1):
                changed_N.add((x,y+(period//2-y+move)*2+1))
            elif x in range(1, self.height) and y in range(period//2+move+1, move+period+1):
                right_N.add((x,y))               
        if changed_N ^ right_N:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1, self.height-1) and y in range(move, period//2 + move):
                changed_E.add((x,y+(period//2-y+move)*2))
            elif x in range(1, self.height-1) and y in range(period//2+move+1, move+period+1):
                right_E.add((x,y))
        if changed_E ^ right_E:
            return False
        return True

    def glided_horizontal_odd(self):
        changed_N = set()
        lower_N = set()
        changed_NE = set()
        lower_SE = set()
        changed_E = set()
        lower_E = set()
        changed_SE = set()
        lower_NE = set()
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2+1) and y in range(self.period):
                changed_N.add(((x + (self.height//2 - x) *2 +1),y+self.period//2))
            elif x in range(self.height//2+1, self.height) and y in range(self.period//2,self.period+self.period//2):
                lower_N.add((x, y))
        if changed_N ^ lower_N:
            return False
        # NE -- SE
        for (x,y) in self.NE:
            if x in range(1, self.height//2+1) and y in range(self.period):
                changed_NE.add(((x + (self.height//2 - x) *2),y+self.period//2))
            elif x in range(self.height//2 + 1, self.height) and y in range(self.period//2,self.period//2+self.period):
                lower_NE.add((x, y))
        for (x,y) in self.SE:
            if x in range(self.height//2, self.height - 1) and y in range(self.period//2,self.period//2+self.period):
                lower_SE.add((x, y))
            elif x in range(self.height//2) and y in range(self.period):
                changed_SE.add(((x + (self.height//2 - x)*2),y+self.period//2))
        if changed_NE ^ lower_SE:
            return False
        if changed_SE ^ lower_NE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1, self.height//2) and y in range(self.period):
                changed_E.add(((x + (self.height//2 - x) *2),y+self.period//2))
            elif x in range(self.height//2+1, self.height - 1) and y in range(self.period//2,self.period//2+self.period):
                lower_E.add((x, y))               
        if changed_E ^ lower_E:
            return False
        return True

    def glided_horizontal_even(self):
        changed_NE = set()
        lower_SE = set()
        lower_NE = set()
        changed_SE = set()
        changed_N = set()
        lower_N = set()
        changed_E = set()
        lower_E = set()
        # NE
        for (x,y) in self.NE:
            if x == self.height//2:
                return False
            elif x in range(1, self.height//2) and y in range(self.period):
                changed_NE.add((x+(self.height//2-x)*2-1,y+self.period//2))
            elif x in range(self.height//2+1, self.height) and y in range(self.period//2,self.period//2+self.period):
                lower_NE.add((x,y))       
        # SE
        for (x,y) in self.SE:
            if x == self.height//2 - 1:
                return False
            elif x in range(self.height//2, self.height - 1) and y in range(self.period//2,self.period//2+self.period):
                lower_SE.add((x,y))
            elif x in range(self.height//2-1) and y in range(self.period):
                changed_SE.add((x+(self.height//2-x)*2-1,y+self.period//2))
        if changed_NE ^ lower_SE:
            return False
        if changed_SE ^ lower_NE:
            return False       
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2) and y in range(self.period):
                changed_N.add((x+(self.height//2-x)*2,y+self.period//2))
            elif x in range(self.height//2 + 1,self.height) and y in range(self.period//2,self.period//2+self.period):
                lower_N.add((x,y))
        if changed_N ^ lower_N:
            return False
        # E
        for (x,y) in self.E:
            if x in range(1,self.height//2) and y in range(self.period):
                changed_E.add((x+(self.height//2-x)*2-1,y+self.period//2))
            elif x in range(self.height//2,self.height-1) and y in range(self.period//2,self.period//2+self.period):
                lower_E.add((x,y))
        if changed_E ^ lower_E:
            return False
        return True

    def rotation_even_height_even(self, move):
        changed_lu_N = set()
        right_lower_N = set()
        changed_ll_N = set()
        right_upper_N = set()
        changed_lu_NE = set()
        right_lower_NE = set()
        changed_ll_NE = set()
        right_upper_NE = set()
        changed_lu_SE = set()
        right_lower_SE = set()
        changed_ll_SE = set()
        right_upper_SE = set()
        changed_lu_E = set()
        right_lower_E = set()
        changed_ll_E = set()
        right_upper_E = set()
        # axis
        if self.period % 2 == 1:
            period = self.period + 1
        else:
            period = self.period
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2+1):
                if y in range(move, period//2 + move+1):
                    changed_lu_N.add((x+(self.height//2-x)*2+1,y+(period//2-y+move)*2))
                elif y in range(period//2+move, move+period+1):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(period//2+move, move+period+1):
                    right_lower_N.add((x, y))
                elif y in range(move, period//2 + move+1):
                    changed_ll_N.add((x-(x-self.height//2)*2+1,y+(period//2-y+move)*2))
        if changed_lu_N ^ right_lower_N:
            return False
        if changed_ll_N ^ right_upper_N:
            return False
        # NE
        for (x,y) in self.NE:
            if x in range(1, self.height//2+1):
                if y in range(move, period//2 + move):
                    changed_lu_NE.add((x+(self.height//2-x)*2+1,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move, move+period):
                    right_upper_NE.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(period//2+move, move+period):
                    right_lower_NE.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_NE.add((x-(x-self.height//2)*2+1,y+(period//2-y+move)*2-1))
        if changed_lu_NE ^ right_lower_NE:
            return False
        if changed_ll_NE ^ right_upper_NE:
            return False
        # SE
        for (x,y) in self.SE:
            if x in range(self.height//2):
                if y in range(move, period//2 + move):
                    changed_lu_SE.add((x+(self.height//2-x)*2-1,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move, move+period):
                    right_upper_SE.add((x, y)) 
            elif x in range(self.height//2, self.height-1):
                if y in range(period//2+move, move+period):
                    right_lower_SE.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_SE.add((x-(x-self.height//2)*2-1,y+(period//2-y+move)*2-1))
        if changed_lu_SE ^ right_lower_SE:
            return False
        if changed_ll_SE ^ right_upper_SE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(self.height//2+1):
                if y in range(move, period//2 + move):
                    changed_lu_N.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move, move+period):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2, self.height+1):
                if y in range(period//2+move, move+period):
                    right_lower_N.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_N.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2-1))
        if changed_lu_E ^ right_lower_E:
            return False
        if changed_ll_E ^ right_upper_E:
            return False
        return True

    def rotation_even_height_odd(self,move):
        changed_lu_N = set()
        right_lower_N = set()
        changed_ll_N = set()
        right_upper_N = set()
        changed_lu_NE = set()
        right_lower_NE = set()
        changed_ll_NE = set()
        right_upper_NE = set()
        changed_lu_SE = set()
        right_lower_SE = set()
        changed_ll_SE = set()
        right_upper_SE = set()
        changed_lu_E = set()
        right_lower_E = set()
        changed_ll_E = set()
        right_upper_E = set()
        # axis
        if self.period % 2 == 1:
            period = self.period + 1
        else:
            period = self.period
        # N
        for (x,y) in self.N:
            if x in range(1, self.height//2+1):
                if y in range(move, period//2 + move+1):
                    changed_lu_N.add((x+(self.height//2-x)*2+1,y+(period//2-y+move)*2+1))
                elif y in range(period//2+move, move+period+1):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(period//2+move, move+period+1):
                    right_lower_N.add((x, y))
                elif y in range(move, period//2 + move+1):
                    changed_ll_N.add((x-(x-self.height//2)*2+1,y+(period//2-y+move)*2+1))       
        if changed_lu_N ^ right_lower_N:
            return False
        if changed_ll_N ^ right_upper_N:
            return False
        # NE
        for (x,y) in self.NE:
            if x in range(1,self.height//2+1):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2+1,y) not in self.NE:
                        return False
                elif y in range(move, period//2 + move):
                    changed_lu_NE.add((x+(self.height//2-x)*2+1,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1, move+period+1):
                    right_upper_NE.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(period//2+move+1, move+period+1):
                    right_lower_NE.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_NE.add((x-(x-self.height//2)*2+1,y+(period//2-y+move)*2))
        if changed_lu_NE ^ right_lower_NE:
            return False
        if changed_ll_NE ^ right_upper_NE:
            return False
        # SE
        for (x,y) in self.SE:
            if x in range(self.height//2):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2-1,y) not in self.SE:
                        return False
                elif y in range(move, period//2 + move):
                    changed_lu_SE.add((x+(self.height//2-x)*2-1,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1, move+period+1):
                    right_upper_SE.add((x, y))
            elif x in range(self.height//2, self.height-1):
                if y in range(period//2+move+1, move+period+1):
                    right_lower_SE.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_SE.add((x-(x-self.height//2)*2-1,y+(period//2-y+move)*2))
        if changed_lu_SE ^ right_lower_SE:
            return False
        if changed_ll_SE ^ right_upper_SE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(self.height//2+1):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2,y) not in self.E:
                        return False
                elif y in range(move, period//2 + move):
                    changed_lu_N.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1, move+period+1):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2, self.height+1):
                if y in range(period//2+move+1, move+period+1):
                    right_lower_N.add((x, y))
                elif y in range(move, period//2 + move):
                    changed_ll_N.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2))
        if changed_lu_E ^ right_lower_E:
            return False
        if changed_ll_E ^ right_upper_E:
            return False
        return True       

    def rotation_odd_height_odd(self,move):
        changed_lu_N = set()
        right_lower_N = set()
        changed_ll_N = set()
        right_upper_N = set()
        changed_lu_NE = set()
        right_lower_NE = set()
        changed_ll_NE = set()
        right_upper_NE = set()
        changed_lu_SE = set()
        right_lower_SE = set()
        changed_ll_SE = set()
        right_upper_SE = set()
        changed_lu_E = set()
        right_lower_E = set()
        changed_ll_E = set()
        right_upper_E = set()
        # axis
        if self.period % 2 == 1:
            period = self.period + 1
        else:
            period = self.period
        # N
        for (x,y) in self.N:
            if x == self.height//2:
                if y in range(period//2+1+move):
                    if (x,y+(period//2-y+move)*2+1) not in self.N:
                        return False
            elif x in range(1, self.height//2):
                if y in range(move, period//2 + move+1):
                    changed_lu_N.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2+1))
                elif y in range(period//2+move+1, move+period+2):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(period//2+move+1, move+period+2):
                    right_lower_N.add((x, y))
                elif y in range(move, period//2 + move+1):
                    changed_ll_N.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2+1))
        if changed_lu_N ^ right_lower_N:
            return False
        if changed_ll_N ^ right_upper_N:
            return False
        # NE
        for (x,y) in self.NE:
            if x == self.height//2:
                if y in range(period//2+move):
                    if (x,y+(period//2-y+move)*2) not in self.NE:
                        return False
            elif x in range(1,self.height//2):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2, y) not in self.NE:
                        return False
                elif y in range(move,period//2+move):
                    changed_lu_NE.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_upper_NE.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(move,period//2+move):
                    changed_ll_NE.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_lower_NE.add((x, y))
        if changed_lu_NE ^ right_lower_NE:
            return False
        if changed_ll_NE ^ right_upper_NE:
            return False
        # SE
        for (x,y) in self.SE:
            if x == self.height//2-1:
                if y in range(period//2+move):
                    if (x,y+(period//2-y+move)*2) not in self.SE:
                        return False
            elif x in range(self.height//2-1):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2-2, y) not in self.SE:
                        return False
                elif y in range(move,period//2+move):
                    changed_lu_SE.add((x+(self.height//2-x)*2-2,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_upper_SE.add((x, y))
            elif x in range(self.height//2, self.height-1):
                if y in range(move,period//2+move):
                    changed_ll_SE.add((x-(x-self.height//2)*2-2,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_lower_SE.add((x, y))
        if changed_lu_SE ^ right_lower_SE:
            return False
        if changed_ll_SE ^ right_upper_SE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(self.height//2):
                if y == move + period//2:
                    if (x+(self.height//2-x)*2-1, y) not in self.E:
                        return False
                elif y in range(move,period//2+move):
                    changed_lu_E.add((x+(self.height//2-x)*2-1,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_upper_E.add((x, y))
            elif x in range(self.height//2, self.height):
                if y in range(move,period//2+move):
                    changed_ll_E.add((x-(x-self.height//2)*2-1,y+(period//2-y+move)*2))
                elif y in range(period//2+move+1,move+period+1):
                    right_lower_E.add((x, y))
        if changed_lu_E ^ right_lower_E:
            return False
        if changed_ll_E ^ right_upper_E:
            return False
        return True

    def rotation_odd_height_even(self,move):
        changed_lu_N = set()
        right_lower_N = set()
        changed_ll_N = set()
        right_upper_N = set()
        changed_lu_NE = set()
        right_lower_NE = set()
        changed_ll_NE = set()
        right_upper_NE = set()
        changed_lu_SE = set()
        right_lower_SE = set()
        changed_ll_SE = set()
        right_upper_SE = set()
        changed_lu_E = set()
        right_lower_E = set()
        changed_ll_E = set()
        right_upper_E = set()
        # axis
        if self.period % 2 == 1:
            period = self.period + 1
        else:
            period = self.period
        # N
        for (x,y) in self.N:
            if x == self.height//2:
                if y in range(move+period//2):
                    if (x+(self.height//2-x)*2-1,y) not in self.N:
                        return False
            elif x in range(1,self.height//2):
                if y in range(move,period//2+move+1):
                    changed_lu_N.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2))
                elif y in range(period//2+move,move+period+1):
                    right_upper_N.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(move,period//2+move+1):
                    changed_ll_N.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2))
                elif y in range(period//2+move,move+period+1):
                    right_lower_N.add((x, y))
        if changed_lu_N ^ right_lower_N:
            return False
        if changed_ll_N ^ right_upper_N:
            return False
        # NE
        for (x,y) in self.NE:
            if x == self.height//2:
                if y in range(period//2+move):
                    if (x,y+(period//2-y+move)*2-1) not in self.NE:
                        return False
            elif x in range(1,self.height//2):
                if y in range(move,period//2+move):
                    changed_lu_NE.add((x+(self.height//2-x)*2,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_upper_NE.add((x, y))
            elif x in range(self.height//2+1, self.height):
                if y in range(move,period//2+move):
                    changed_ll_NE.add((x-(x-self.height//2)*2,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_lower_NE.add((x, y))
        if changed_lu_NE ^ right_lower_NE:
            return False
        if changed_ll_NE ^ right_upper_NE:
            return False
        # SE
        for (x,y) in self.SE:
            if x == self.height//2-1:
                if y in range(period//2+move):
                    if (x,y+(period//2-y+move)*2-1) not in self.SE:
                        return False
            elif x in range(self.height//2-1):
                if y in range(move,period//2+move):
                    changed_lu_SE.add((x+(self.height//2-x)*2-2,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_upper_SE.add((x, y))
            elif x in range(self.height//2, self.height-1):
                if y in range(move,period//2+move):
                    changed_ll_SE.add((x-(x-self.height//2)*2-2,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_lower_SE.add((x, y))
        if changed_lu_SE ^ right_lower_SE:
            return False
        if changed_ll_SE ^ right_upper_SE:
            return False
        # E
        for (x,y) in self.E:
            if x in range(self.height//2):
                if y in range(move,period//2+move):
                    changed_lu_E.add((x+(self.height//2-x)*2-1,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_upper_E.add((x, y))
            elif x in range(self.height//2, self.height):
                if y in range(move,period//2+move):
                    changed_ll_E.add((x-(x-self.height//2)*2-1,y+(period//2-y+move)*2-1))
                elif y in range(period//2+move,move+period):
                    right_lower_E.add((x, y))
        if changed_lu_E ^ right_lower_E:
            return False
        if changed_ll_E ^ right_upper_E:
            return False
        return True
    
