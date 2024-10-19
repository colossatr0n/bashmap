# BashMap

BashMap converts a shell command into an argument dictionary: 

```python
>>> from bashmap import BashMap
>>> BashMap.from_cmd('curl -s -SP8080 www.github.com www.pypi.org --basic --retry 5')
{
    {'utility': [('curl',)],
    '-s': [()],
    '-S': [()],
    '-P': [('8080',)],
    'operands': [('www.github.com',), ('www.pypi.org',)],
    '--basic': [()],
    '--retry': [('5',)]
}
```

and can also be called from the command line:
```bash
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
```
BashMap recognizes general patterns to form its argument dictionaries. Not all shell commands follow the same standards, so there will be commands that get categorized incorrectly. To help overcome this, see [Limit Override Dictionary](#limit-override-dictionary).

# Table of Contents
- [BashMap](#bashmap)
- [Table of Contents](#table-of-contents)
- [Terminology Legend](#terminology-legend)
- [Raw Representation](#raw-representation)
  - [Utility](#utility)
  - [Operands](#operands)
  - [Option without Option-Arguments](#option-without-option-arguments)
  - [Option with Option-Arguments](#option-with-option-arguments)
- [Simple Representation](#simple-representation)
  - [Simple Utility](#simple-utility)
  - [Simple Operands](#simple-operands)
  - [Simple Options](#simple-options)
  - [Simple Option Arguments](#simple-option-arguments)
- [Limit Override Dictionary](#limit-override-dictionary)
  - [When to Use](#when-to-use)
  - [Finite Limits](#finite-limits)
    - [*Limit an option to zero option-arguments*](#limit-an-option-to-zero-option-arguments)
    - [*Allow an option to accept up to N option-arguments at a time*](#allow-an-option-to-accept-up-to-n-option-arguments-at-a-time)
  - [Infinite Limits](#infinite-limits)
    - [*Allow an option to accept infinite numbers of option-arguments at a time*](#allow-an-option-to-accept-infinite-numbers-of-option-arguments-at-a-time)

# Terminology Legend
Terminology is derived from [The Open Group Base Specifications Issue 7, 2018 edition
IEEE Std 1003.1-2017](https://pubs.opengroup.org/onlinepubs/9699919799.2018edition/basedefs/V1_chap12.html#tag_12_01).


| Term              | Definition                                                                                   | Example                          |
| ----------------- | -------------------------------------------------------------------------------------------- | -------------------------------- |
| `command`         | The command.                                                                                 | `curl -P 8080 www.github.com`    |
| `utility`         | The name of the command.                                                                     | `curl`                           |
| `option`          | An option of the command.                                                                    | `-P`                             |
| `option-argument` | An argument of the option.                                                                   | `8080`                           |
| `operand`         | An argument that doesn't belong to an option.                                                | `www.github.com`                 |
| `argument-group`  | A group of arguments. In the example, `arg1` and `arg2` belong to a single `argument-group`. | `--multipleOptionArgs arg1 arg2` |

# Raw Representation

For an actual representation of a BashMap dictionary, see the [BashMap usage example](#bashmap). For terminology examples, see [Terminology Legend](#terminology-legend).

## Utility
The `utility` can be accessed through the `utility` key or property:

```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap['utility']
[('curl',)]

>>> bashmap.utility
[('curl',)]
```

## Operands
The `operands` can be accessed through the `operands` key or property:

```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap['operands']
[('www.github.com',), ('www.pypi.org',)]

>>> bashmap.operands
[('www.github.com',), ('www.pypi.org',)]
```

## Option without Option-Arguments
This type of `option's` value is list with an empty `argument-group` (tuple):

```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap['-s']
[()]
```

## Option with Option-Arguments
This type of `option's` value is a list of `arguments-groups` (tuple) containing the `option-arguments`:

```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap['-P']
[('8080',)]
```
Each `argument-group` (tuple) represents the `option-arguments` for each `option` call. See this [example](#allow-an-option-to-accept-up-to-n-option-arguments-at-a-time). 

# Simple Representation
BashMap has lazy properties and convenience functions that provide a simple representation of its raw data. They contain less context about the command, but can be more convenient to use. The simple representations are essentially the raw representations without the `argument-groups`.

## Simple Utility
```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap.simpleutility
'curl'
```

## Simple Operands
```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap.simpleoperands
['www.github.com', 'www.pypi.org']
```

## Simple Options
```python
>>> bashmap = BashMap.from_cmd('curl -s -P 8080 www.github.com www.pypi.org')
>>> bashmap.simpleoptions
['-s', '-P']
```

## Simple Option Arguments
```python
>>> bashmap = BashMap.from_cmd('curl -X GET -P 8080 www.github.com www.pypi.org')
>>> bashmap.simpleoptionargs('-P')
['8080']
>>>
>>> bashmap.load_all_simpleoptionargs()
['GET', '8080']
```

# Limit Override Dictionary
The limit override dictionary is an optional dictionary that can be passed to BashMap to override the amount of `option-arguments` an `option` can receive.

The value can either be a non-negative integer to denote a finite limit or `None` if the limit is infinite.

## When to Use
There are two scenarios in which the limit override dictionary is useful:

- An `option` should take zero `option-arguments` but is immediately followed by an `operand`. 
  - See [example](#limit-an-option-to-zero-option-arguments).
- An `option` can take more than one `option-argument` at a time. 
  - See [finite example](#allow-an-option-to-accept-up-to-n-option-arguments-in-a-single-call) and [infinite example](#allow-an-option-to-accept-infinite-numbers-of-option-arguments-at-a-time).

## Finite Limits

### *Limit an option to zero option-arguments*

```python
>>> bashmap('curl -s www.github.com', limit_overrides={'-s': 0})
{
    'utility': [('curl',)],
    '-s': [()],
    'operands': [('www.github.com',)]
}

```

This should be used when an `operand` (`www.github.com`) is immediately preceded by an `option` (`-s`) that doesn't take an `option-argument`. Unless otherwise defined, BashMap will pair the `option` (`-s`) with the `non-option` (`www.github.com`):

```python
# Not using limit override
>>> bashmap('curl -s www.github.com')
# results in incorrect output
{
    'utility': [('curl',)],
    '-s': [('www.github.com',)]
}
```

### *Allow an option to accept up to N option-arguments at a time*

```python
>>> bashmap('sips --setProperty format jpeg --setProperty quality best --out outfile infile', limit_overrides={'--setProperty': 2})
{ 
    'utility': [('sips',)],
    '--setProperty': [('format', 'jpeg'), ('quality', 'best')],
    '--out': [('outfile',)],
    'operands': [('infile',)]
}
```

The scenario in which this should be used is if a `utility` allows multiple `option-arguments` to be received by a single `option` call. In the example above, there's one call to `--setProperty` with `format jpeg` and a second call with `quality best`. `format jpeg` comprises one `argument-group` and `quality best` comprises the second `argument-group`.

Though this isn't commonplace for an `option` to receive multiple `option-arguments` in a single call, it does occasionally happen. 

Unless otherwise defined, BashMap associates an `option` call with a single `option-argument`:

```python
# Not using limit override
>>> bashmap('sips --setProperty format jpeg infile --out outfile')
# results in incorrect output, since `jpeg` gets lumped in with the operands
{ 
    'utility': [('sips',)],
    '--setProperty': [('format',)],
    '--out': [('outfile',)],
    'operands': [('jpeg,'), ('infile',)]
}
```

## Infinite Limits

### *Allow an option to accept infinite numbers of option-arguments at a time*

```python
>>> bashmap('some_utility --infiniteOptArgs optArg1 optArg2 optArg3 --out outfile.txt infile.txt ', limit_overrides={'--infiniteOptArgs': None})
# results in
{
    'utility': [('some_utility',)],
    '--infiniteOptArgs': [('optArg1', 'optArg2', 'optArg3')],
    '--out': [('file.txt',)],
    'operands': [('infile.txt',)]
}
```

Though it is uncommon for an `option` to take an infinite number of `option-arguments`, `None` is used as the `option's` value to denote this behavior.