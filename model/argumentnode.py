"""ArgumentNode - Node for an argument that contains a value, next, and previous.
"""


class ArgumentNode:
    """Node for an argument that contains a value, next, and previous.
    """    
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None
