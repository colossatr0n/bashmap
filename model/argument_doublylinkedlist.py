"""ArgumentLinkedList - A linked list of ArgumentNodes.
"""
from model.argumentnode import ArgumentNode


class ArgumentDoublyLinkedList:
    """A doubly linked list of ArgumentNodes.
    """    
    def __init__(self):
        self.head = None
        self.tail = None
    
    @staticmethod
    def from_cmd(args):
        """Converts a list of strings into a doubly linked list of ArgumentNodes. 
        
        Arguments:
            args {list of strings} -- The Bash arguments.
        
        Returns:
            [ArgumentLinkedList] -- The doubly linked list of ArgumentNodes.
        """        
        llist = ArgumentDoublyLinkedList()
        llist.head = ArgumentNode(value=args[0])

        prev = None
        for arg in args:
            if not prev:
                prev = llist.head
                continue
            prev.next = ArgumentNode(value=arg)
            prev.next.prev = prev
            prev = prev.next
        llist.tail = prev
        return llist
