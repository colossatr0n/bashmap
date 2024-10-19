"""bashparse - Parses an ArgumentDoublyLinkedList of Bash command arguments and returns the result as an argument dictionary.

This module allows for parsing an ArgumentLinkedList of Bash command arguments. The parsed arguments are then stored and
returned in an argument dictionary.
"""
# TODO: This file is finished.

def parse(linkedlist, limitoverrides):
    """Parses a linked list of Bash arguments and returns the argument dictionary.
    
    Arguments:
        linkedlist {ArgumentDoublyLinkedList} -- The linked list of ArgumentNodes representing the Bash command.
        limitoverrides {dict} -- The limits override dictionary indicating how many option-arguments an option can receive.
    
    Returns:
        dict -- The argument dictionary.
    """
    argdict = dict()
    # Stores first argument as the utility
    _store_utility(linkedlist.head, argdict)
    # Begins parsing arguments
    _parse_arguments(linkedlist.head.next, argdict, limitoverrides)
    return argdict


def _parse_arguments(argnode, argdict, limitoverrides):
    """Parses an ArgumentNode and stores it in the argument dictionary as either an option, option-argument, or operand.
    
    Arguments:
        argnode {ArgumentNode} -- An argument from the Bash command.
        argdict {dict} -- The argument dictionary containing the mapping for the Bash command.
        limitoverrides {dict} -- The limits override dictionary indicating how many option-arguments an option can receive.
    """    
    if argnode is None:
        return
    # If argument is an option
    if _is_option(argnode):
        # Store the option
        _store_option(argnode, argdict)
        # If the option has potential option-arguments, parse them
        if _has_next(argnode):
            argnode = _parse_optionarguments(argnode, argnode.next, argdict, limitoverrides.get(argnode.value, 1))
        else:
            return argnode
    # Othwerwise, argument is an operand
    else:
        _store_operand(argnode, argdict)

    # Move onto next argument
    _parse_arguments(argnode.next, argdict, limitoverrides)


def _parse_optionarguments(option_node, argnode, argdict, n):
    """Parses and stores for the option up to (n-1) argument nodes that follow the current argument node.
    
    Arguments:
        option_node {ArgumentNode} -- The option node.
        argnode {ArgumentNode} -- The argument node.
        argdict {dict} -- The argument dictionary containing the mapping for the Bash command.
        n {int} -- The number of argument nodes to check, including the current argument node.

    Returns:
        ArgumentNode -- The last node that was parsed.
    """
    # If the argument following the option is an option-argument  
    if _is_optionargument(argnode):
        # Store it in the option-argument group
        _upsert_optionargument_group(option_node, argnode, -1, argdict)
        # If n is finite
        if _is_finite(n):
            n -= 1
            if n <= 0:
                return argnode
    else:
        return argnode.prev
    return _parse_optionarguments(option_node, argnode.next, argdict, n)


def _store_operand(operand_node, argdict):
    """Stores operand in argument dictionary.    
    
    Arguments:
        operand_node {ArgumentNode} -- The operand node.
        argdict {dict} -- The argument dictionary containing the mapping for the Bash command.
    """    
    # If an operand exists, append operand
    if 'operands' in argdict:
        argdict['operands'].append(_init_optionargument_group(operand_node.value))
    # Otherwise, create new operand key value pair
    else:
        argdict['operands'] = [_init_optionargument_group(operand_node.value)]


def _store_utility(utility_node, argdict):
    """Stores utility in argument dictionary.
    
    Arguments:
        utility_node {[type]} -- [description]
        argdict {[type]} -- [description]
    """    
    argdict['utility'] = [_init_optionargument_group(utility_node.value)]


def _store_option(option_node, argdict):
    """Stores option in argument dictionary.
    
    Arguments:
        option_node {ArgumentNode} -- The option node.
        argdict {dict} -- The argument dictionary containing the mapping for the Bash command.
    """    
    argdict.setdefault(option_node.value, []).append(_init_optionargument_group())


def _upsert_optionargument_group(option_node, optionarg, index, argdict):
    """Updates or inserts the option-argument group at the given index in the list.
    
    Arguments:
        option_node {ArgumentNode} -- The option node.
        optionarg {ArgumentNode} -- The option-argument node to create the group from or to add to the option-argument group.
        index {int} -- The index of the new or already existing option-argument group in the list.
        argdict {dict} -- The argument dictionary containing the mapping for the Bash command.

    """    
    if option_node.value not in argdict:
        argdict[option_node.value] = [_init_optionargument_group(optionarg.value)]
    else:
        argdict[option_node.value][index] = _append_optionargument_group(argdict[option_node.value][index], optionarg.value)


def _init_optionargument_group(value=None):
    """Initializes an empty or valued option-argument group.
    
    Keyword Arguments:
        value {string} -- The value to insert into the option-argument group (default: {None})
    
    Returns:
        tuple -- The option-argument group.
    """    
    if value is None:
        return ()
    else:
        return (value,)


def _append_optionargument_group(group, value):
    """Appends the value to the option-argument group.
    
    Arguments:
        group {tuple} -- The option-argument group to append to.
        value {string} -- The value to append to the option-argument group.
    
    Returns:
        tuple -- The new option-argument group.
    """    
    return (*group, value)


def _is_option(argnode):
    """Checks whether the ArgumentNode is an option.
    
    Arguments:
        argnode {ArgumentNode} -- The argument node to check.
    
    Returns:
        bool -- True if ArgumentNode is an option, False otherwise
    """    
    return argnode.value[0] == '-'


def _is_optionargument(argnode):
    """Checks whether the ArgumentNode is an option-argument.
    
    Arguments:
        argnode {ArgumentNode} -- The argument node to check.
    
    Returns:
        bool -- True if ArgumentNode is an option-argument, False otherwise
    """    
    return argnode.value[0] != '-'


def _is_finite(limit):
    """Checks whether the limit is finite.
    
    Arguments:
        limit {int} -- The option-argument limit.
    
    Returns:
        bool -- True if limit is finite, False otherwise (infinite).
    """    
    return limit is not None


def _has_next(option_node):
    """Checks whether the ArgumentNode has a following ArgumentNode.
    
    Arguments:
        option_node {ArgumentNode} -- The ArgumentNode to check for a following ArgumentNode.
    
    Returns:
        bool -- True if ArgumentNode has a following ArgumentNode, False otherwise.
    """    
    return option_node.next is not None
