#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bashmap - Converts a Bash command into an argument dictionary

Converts a Bash command into an argument dictionary. Can be imported as a module or
run from the command line.

Example - Imported as Module:
    >>> from bashmap import BashMap
    >>> BashMap.fromcmd('curl -s -SP8080 www.github.com www.pypi.org --basic --retry 5')
    {
        'utility': [('curl',)],
        '-s': [()],
        '-S': [()],
        '-P': [('8080',)],
        'operands': [('www.github.com',), ('www.pypi.org',)],
        '--basic': [()],
        '--retry': [('5',)]
    }

Example - Command Line:
    $ bashmap "curl -P 8080 www.github.com"
    {
        'utility': [('curl',)],
        '-s': [()],
        '-S': [()],
        '-P': [('8080',)],
        'operands': [('www.github.com',), ('www.pypi.org',)],
        '--basic': [()],
        '--retry': [('5',)]
    }
"""
import argparse
import ast
import json
from pprint import pprint

from model.argument_doublylinkedlist import ArgumentDoublyLinkedList
from splitter import bashsplit
from parser import bashparse
from utils.cachedproperty import cached_property


class BashMap(dict):

    def __init__(self, *args, **kwargs):
        super(BashMap, self).__init__(*args, **kwargs)
    
    @classmethod
    def fromcmd(cls, cmd, limitoverrides=None):
        """Converts a Bash cmd into an argument dictionary. Accepts a limit overrides dictionary
        that allows for setting the upper limit of how many `option-arguments` an `option` can
        receive in a single call.
        
        Example:
            >>> BashMap.fromcmd('curl -s -SP8080 www.github.com www.pypi.org --basic --retry 5')
            {
                'utility': [('curl',)],
                '-s': [()],
                '-S': [()],
                '-P': [('8080',)],
                'operands': [('www.github.com',), ('www.pypi.org',)],
                '--basic': [()],
                '--retry': [('5',)]
            }
        
        Arguments:
            cmd {string} -- The Bash cmd.
        
        Keyword Arguments:
            limitOverrides {dict} -- The limits override dictionary indicating how many option-arguments an option can receive. (default: {dict()})

        Returns:
            [dict] -- The resulting argument dictionary.
        """
        if limitoverrides is None:
            limitoverrides = {}
        # Split the Bash cmd into a list of string arguments.
        args = bashsplit.split(cmd)
        # Convert args into linked list
        arglinkedlist = ArgumentDoublyLinkedList.from_cmd(args)
        # Parse the arguments in the linked list
        return cls(bashparse.parse(arglinkedlist, limitoverrides))

    @property
    def utility(self):
        """A property that returns the utility as a tuple within a list.
        
        Returns:
            Tuple list -- A list with a single tuple containing the utility name.  
        """        
        return self['utility']

    @cached_property
    def simpleutility(self):
        """A cached property that returns the utility as a string.
        
        Returns:
            str -- The utility name.
        """        
        return self.utility[0][0]

    @property
    def operands(self):
        """A property that returns the operands in a list of tuples.
        
        Returns:
            Tuple list -- A list of tuples containing the operands.
        """        
        return self['operands']
    
    @cached_property
    def simpleoperands(self):
        """A cached property that returns the operands as a list of strings.
        
        Returns:
            str list -- The operands.
        """        
        return self.load_simpleoperands()

    def load_simpleoperands(self):
        """Loads the operands as a list of strings.
        
        Returns:
            str list -- The operands.
        """        
        return list(operand for operandtuple in self.operands for operand in operandtuple)
    
    @cached_property
    def simpleoptions(self):
        """A cached property that returns the options as a list of strings.
        
        Returns:
            str list -- The options.
        """        
        return self.load_simpleoptions()
    
    def load_simpleoptions(self):
        """Loads the options as a list of strings.
        
        Returns:
            str list -- The options
        """        
        return list(arg for arg in self.keys() if arg[0] == '-')

    @cached_property
    def allsimpleoptionargs(self):
        """A cached property that returns all of the options in the dictionary as a list of strings.
        
        Returns:
            str list -- Every option in the dictionary.
        """        
        return self.loadall_simpleoptionargs()

    def loadall_simpleoptionargs(self):
        """Loads all option-arguments in the dictionary as a list of strings.
        
        Returns:
            str list -- Every option-argument in the dictionary.
        """        
        return list(optionarg for option in self.simpleoptions for optionarg_tuple in self[option] for optionarg in optionarg_tuple)

    def simpleoptionargs(self, *options):
        """Loads the option-arguments for the option(s) as a list of strings.
        
        Arguments:
            option {str} -- The option's name.
        
        Returns:
            str list -- The option-arguments for the option(s). Empty list if option(s) DNE or option(s) have no option-arguments.
        """        
        return list(optionarg for optionarg_tuple in self.vals(*options) for optionarg in optionarg_tuple)

    def vals(self, *keys):
        """Returns the values for the key(s) if they exist. Otherwise returns an empty list.

        Arguments:
            option {str} -- The option name.
        
        Returns:
            Tuple list -- The values for the key(s). Empty list if the key(s) DNE or doesn't have value.
        """        
        arg_groups = []
        for key in keys:
            if key in self:
                arg_groups.extend(self[key])
        return arg_groups


def _set_up_argumentparser():
    epilog = """
Example:

    $ bashmap "curl -s -P 8080 www.github.com www.pypi.org"
    {
        'utility': [('curl',)],
        '-s': [()],
        '-P': [('8080',)],
        'operands': [('www.github.com'), ('www.pypi.org')]
    }
    """
    parser = argparse.ArgumentParser(
        description="Converts a Bash command into an argument dictionary.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', help="The Bash command to convert into an argument dictionary.")
    parser.add_argument('-l', '--limit-overrides', help="The limits override dictionary indicating how many option-arguments an option can receive.")
    parser.add_argument('-j', '--json', action='store_true', help="Prints the argument dictionary in JSON.")
    parser.add_argument('-p', '--pretty', action='store_true', help="Pretty prints the argument dictionary.")
    return parser    


def main():
    args = _set_up_argumentparser().parse_args()

    limit_overrides = ast.literal_eval(args.limit_overrides) if args.limit_overrides else dict()
    bashmap = BashMap.fromcmd(args.command, limitoverrides=limit_overrides)

    if args.json:
        if args.pretty:
            print(json.dumps(bashmap, indent=2))
        else:
            print(json.dumps(bashmap))
    else:
        if args.pretty:
            pprint(bashmap, width=1)
        else:
            print(bashmap)


if __name__ == "__main__":
    main()
