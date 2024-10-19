#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from bashmap import BashMap


# TODO swap arg1 and arg2 for most of these tests.
class BashMapTest(unittest.TestCase):

    def test_utility_only(self):
        cmd = 'curl'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap['utility'])
    
    def test_utility_and_arg_only(self):
        cmd = 'curl -s'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap['utility'])
        self.assertEqual([()], bashmap['-s'])

    def test_combined_shortoptions(self):
        cmd = 'curl -sSP8084 someurl' 
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap['utility'])
        self.assertEqual([()], bashmap['-s'])
        self.assertEqual([()], bashmap['-S'])
        self.assertEqual([('8084',)], bashmap['-P'])
        self.assertEqual([('someurl',)], bashmap['operands'])

    def test_combined_shortoptions_with_quoted_optionarg(self):
        cmd = '''curl -sSP"8084" someurl'''
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap['utility'])
        self.assertEqual([()], bashmap['-s'])
        self.assertEqual([()], bashmap['-S'])
        self.assertEqual([('8084',)], bashmap['-P'])
        self.assertEqual([('someurl',)], bashmap['operands'])
    
    def test_multiple_short_options(self):
        cmd = 'curl -s -S -P 8084 someurl'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap['utility'])
        self.assertEqual([()], bashmap['-s'])
        self.assertEqual([()], bashmap['-S'])
        self.assertEqual([('8084',)], bashmap['-P'])
        self.assertEqual([('someurl',)], bashmap['operands'])
    
    def test_multiple_longoptions(self):
        cmd = 'curl --ftp-port 8084 --url someurl --data "num=5&id=6"'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(bashmap['utility'], [('curl',)])
        self.assertEqual(bashmap['--ftp-port'], [('8084',)])
        self.assertEqual(bashmap['--url'], [('someurl',)])
        self.assertEqual(bashmap['--data'], [('num=5&id=6',)])

    def test_multiple_duplicate_options(self):
        cmd = 'curl --data "num=5" --url someurl1 --data "id=6" --url someurl2'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(bashmap['utility'], [('curl',)])
        self.assertEqual(bashmap['--data'], [('num=5',), ('id=6',)])
        self.assertEqual(bashmap['--url'], [('someurl1',), ('someurl2',)])

    def test_operand_first(self):
        cmd = 'curl someurl -s -SP 8084'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(bashmap['utility'], [('curl',)])
        self.assertEqual(bashmap['-s'], [()])
        self.assertEqual(bashmap['-S'], [()])
        self.assertEqual(bashmap['-P'], [('8084',)])
        self.assertEqual(bashmap['operands'], [('someurl',)])
    
    def test_multiple_operands(self):
        cmd = 'curl www.github.com www.pypi.org -P 8080'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(bashmap['utility'], [('curl',)])
        self.assertEqual(bashmap['operands'], [('www.github.com',), ('www.pypi.org',)])
        self.assertEqual(bashmap['-P'], [('8080',)])
    
    def test_limitoverride_equals_option_args(self):
        cmd = 'sips -s format jpeg infile --out outfile'
        limitOverrides = {'-s': 2}
        bashmap = BashMap.fromcmd(cmd, limitoverrides=limitOverrides)
        self.assertEqual(bashmap['utility'], [('sips',)])
        self.assertEqual(bashmap['-s'], [('format','jpeg')])
        self.assertEqual(bashmap['operands'], [('infile',)])
        self.assertEqual(bashmap['--out'], [('outfile',)])

    def test_limitoverride_exceeds_optionargs(self):
        cmd = 'sips infile -s format jpeg --out outfile'
        limitOverrides = {'-s': 3}
        bashmap = BashMap.fromcmd(cmd, limitoverrides=limitOverrides)
        self.assertEqual(bashmap['utility'], [('sips',)])
        self.assertEqual(bashmap['-s'], [('format','jpeg',)])
        self.assertEqual(bashmap['operands'], [('infile',)])
        self.assertEqual(bashmap['--out'], [('outfile',)])
    
    def test_infinite_limitoverride(self):
        cmd = 'sips infile -s format jpeg --out outfile'
        limitOverrides = {'-s': None}
        bashmap = BashMap.fromcmd(cmd, limitoverrides=limitOverrides)
        self.assertEqual(bashmap['utility'], [('sips',)])
        self.assertEqual(bashmap['-s'], [('format','jpeg',)])
        self.assertEqual(bashmap['operands'], [('infile',)])
        self.assertEqual(bashmap['--out'], [('outfile',)])
    
    def test_shortoption_and_longoption_combined_exception(self):
        cmd = 'curl -s--basic'
        self.assertRaises(ValueError, BashMap.fromcmd, cmd)

    def test_longoption_and_optionarg_combined_exception(self):
        cmd = 'curl --ftp-port8084'
        self.assertRaises(ValueError, BashMap.fromcmd, cmd)

    def test_two_explicit_shortoptions_combined_exception(self):
        cmd = 'curl -s-S someurl'
        self.assertRaises(ValueError, BashMap.fromcmd, cmd)
    
    def test_utility(self):
        cmd = 'curl www.github.com www.pypi.org -P 8080'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('curl',)], bashmap.utility)
    
    def test_operands(self):
        cmd = 'curl www.github.com www.pypi.org -P 8080'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('www.github.com',), ('www.pypi.org',)], bashmap.operands)
    
    def test_load_simpleoptions(self):
        cmd = 'curl -s -P 8080 -S'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(['-s', '-P', '-S'], bashmap.load_simpleoptions())
    
    def test_vals(self):
        cmd = 'curl -s -P 8080 --url www.github.com --url www.pypi.org'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual([('8080',)], bashmap.vals('-P'))
        self.assertEqual([('www.github.com',), ('www.pypi.org',)], bashmap.vals('--url'))
        self.assertEqual([()], bashmap.vals('-s'))

    def test_simpleutility(self):
        cmd = 'curl -P 8080 www.github.com'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual('curl', bashmap.simpleutility)
    
    def test_load_simpleoperands(self):
        cmd = 'curl -s -P 8080 www.github.com www.pypi.org'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(['www.github.com', 'www.pypi.org'], bashmap.load_simpleoperands())

    def test_allsimpleoptionargs(self):
        cmd = 'curl -s -P 8080 --url www.github.com --url www.pypi.org'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(['8080', 'www.github.com', 'www.pypi.org'], bashmap.allsimpleoptionargs)
    
    def test_simpleoptionargs(self):
        cmd = 'curl -s -P 8080 --url www.github.com --url www.pypi.org'
        bashmap = BashMap.fromcmd(cmd)
        self.assertEqual(['8080'], bashmap.simpleoptionargs('-P'))
        self.assertEqual(['www.github.com', 'www.pypi.org'], bashmap.simpleoptionargs('--url'))
        self.assertEqual([], bashmap.simpleoptionargs('-s'))
        self.assertEqual([], bashmap.simpleoptionargs('-A'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

