# Written by *** for COMP9021


from binary_tree_adt import *
from math import log


class PriorityQueue(BinaryTree):
    def __init__(self):
        super().__init__()

    def insert(self, value):
        # Replace pass above with your code
        if self.value is None:
            self.value = value
            self.left_node = PriorityQueue()
            self.right_node = PriorityQueue()
            return
        # insert num
        insertion = self
        height = int(log(self.size()+1,2))
        numbers = 2 ** height
        fn = numbers
        self.nodes = [insertion]
        for _ in range(height - 1):
            numbers = numbers // 2
            if self.size() + 1 < numbers + fn:
                insertion = insertion.left_node
            else:
                fn = fn + numbers
                insertion = insertion.right_node
            self.nodes.append(insertion)
        if self.size() + 1 == fn:
            insertion.left_node.insert(value)
            parent = insertion.left_node
        else:
            insertion.right_node.insert(value)
            parent = insertion.right_node
        self.bubble_up(parent)
        
    def bubble_up(self, i):
        for e in self.nodes[::-1]:
            if i.value < e.value:
                i.value, e.value = e.value, i.value

##    def bubble_up(self, i):
##        for e in o_nodes:
            

