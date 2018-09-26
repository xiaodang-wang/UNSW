# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        # find the min node
        min_node = self.head
        check_node = self.head.next_node

        while check_node:
            if min_node.value > check_node.value:
                min_node = check_node
            check_node = check_node.next_node

        # circle and count len
        node = self.head
        length = 0
        while node.next_node:
            length = length + 1
            node = node.next_node
        node.next_node = self.head
#        print(length)

        # find the begin node
        begin_node = self.head
        while begin_node.next_node.value != min_node.value:
            begin_node = begin_node.next_node

##        node = self.head
##        while node:
##            print(node.value)
##            node = node.next_node

        #
        self.head = begin_node
        even_node = begin_node
        odd_node = begin_node.next_node
        

        onode = self.head
        self.head = onode.next_node
        enode = self.head
        for _ in range(int((length+1)/2)-1):
##            print('for',onode.value,enode.value)
##            print(onode.next_node.value,onode.next_node.next_node.next_node.value)
##            print(enode.next_node.value,onode.value)
            
            onode1 = enode.next_node 
            onode.next_node = onode.next_node.next_node.next_node
            enode.next_node = onode

            onode = onode1
            enode = onode.next_node

        onode.next_node = None
        enode.next_node = onode

##        node = self.head
##        while node:
##            print(node.value)
##            node = node.next_node

            

            
        




















            
