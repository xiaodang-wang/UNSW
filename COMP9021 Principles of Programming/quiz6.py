# Defines two classes, Point() and Triangle().
# An object for the second class is created by passing named arguments,
# point_1, point_2 and point_3, to its constructor.
# Such an object can be modified by changing one point, two or three points
# thanks to the method change_point_or_points().
# At any stage, the object maintains correct values
# for perimeter and area.
#
# Written by Xiaodan Wang and Eric Martin for COMP9021


from math import sqrt


class PointError(Exception):
    def __init__(self, message):
        self.message = message


class Point():
    def __init__(self, x = None, y = None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is None or y is None:
            raise PointError('Need two coordinates, point not created.')
        else:
            self.x = x
            self.y = y
            
    # Possibly define other methods


class TriangleError(Exception):
    def __init__(self, message):
        self.message = message


class Triangle:
    def __init__(self, *, point_1, point_2, point_3):
        
        # Replace pass above with your code
        a = sqrt((point_1.x - point_2.x)**2 + (point_1.y - point_2.y)**2)
        b = sqrt((point_1.x - point_3.x)**2 + (point_1.y - point_3.y)**2)
        c = sqrt((point_3.x - point_2.x)**2 + (point_3.y - point_2.y)**2)
        s = (a + b + c)/2
        A = sqrt(s * (s - a) * (s - b) * (s - c))

        if A <= 0:
            raise TriangleError('Incorrect input, triangle not created.')

        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        self.area = A
        self.perimeter = a + b + c
       
    def change_point_or_points(self, *, point_1 = None,point_2 = None, point_3 = None):
        
        # Replace pass above with your code
        if point_1 == None:
            point_1 = self.point_1
        if point_2 == None:
            point_2 = self.point_2
        if point_3 == None:
            point_3 = self.point_3

        a = sqrt((point_1.x - point_2.x)**2 + (point_1.y - point_2.y)**2)
        b = sqrt((point_1.x - point_3.x)**2 + (point_1.y - point_3.y)**2)
        c = sqrt((point_3.x - point_2.x)**2 + (point_3.y - point_2.y)**2)
        s = (a + b + c)/2
        A = sqrt(s * (s - a) * (s - b) * (s - c))

        if A <= 0:
            return print('Incorrect input, triangle not modified.')

        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        self.area = A
        self.perimeter = a + b + c

    # Possibly define other methods

        

            
            
