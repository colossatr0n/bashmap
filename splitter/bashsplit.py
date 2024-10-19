"""bashsplit - Splits a Bash command string into its separate arguments.

Example:
    >>> split('curl -s -SP 8080')
    ['curl', '-s', '-S' '-P', '8080']
"""
import shlex
import re


def split(command):
    """Splits a Bash command string into its separate arguments.
    
    Example:
        >>> split('curl -s -SP 8080')
        ['curl', '-s', '-S' '-P', '8080']

    Arguments:
        command {string} -- The Bash command.
    
    Returns:
        [list of strings] -- The list of Bash arguments.
    """    
    # Creates list of arguments found in the command
    args = []

    # Splits the command into its individual parts
    for arg in shlex.split(command):
        # Checks for subset of illegal syntaxes
        _check_syntax(arg)
        # If arg starts with a single dash but is concatenated with other arguments
        if arg[0] == '-' and arg[1] != '-' and len(arg) > 2:
            # Stores the initial option 
            args.append(arg[0:2])
            # Parses the rest of argument for options and option-arguments
            for i,option in enumerate(arg[2:]):
                # Stores value if number
                if str.isdigit(option):
                    args.append(arg[2 + i:])
                    break
                # Stores option
                else:
                    args.append('-' + option)   
        else:
            args.append(arg)
    return args


def _check_syntax(arg):
    """Checks for a subset of invalid Bash command syntax.
    
    Arguments:
        arg {string} -- The argument to check for valid syntax.
    
    Raises:
        ValueError: The argument contains invalid syntax.
    """    
    error = False
    # Checks for two explicit options without a space between them.
    if re.match(r'^-\w-', arg):
        error = True
    # Checks for long option and option-argument without a space between them.
    if re.match(r'--\w+-\w+\d', arg):
        error = True
    if error:
        raise ValueError('Argument \"{}\" is invalid syntax.'.format(arg))
