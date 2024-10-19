#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import itertools
from splitter.bashsplit import split


class BashSplitTest(unittest.TestCase):

    def test_single_shortoption_without_optionargument(self):
        permutables = ["-s"]
        self._test_permutations("curl", permutables)

    def test_single_shortoption_with_optionargument(self):
        permutables = [ "-P 8080"]
        self._test_permutations("curl", permutables)

    def test_multiple_shortoptions_without_optionarguments(self):
        permutables = ["-s", "-S", "-#"]
        self._test_permutations("curl", permutables)
    
    def test_multiple_shortoptions_with_optionarguments(self):
        cmd = "curl -P 8080 -d somedata -X POST"
        args = split(cmd)
        self.assertEqual(["curl", "-P", "8080", "-d", "somedata", "-X", "POST"], args)

        permutables = ["-P 8080", "-d somedata", "-X POST"]
        self._test_permutations("curl", permutables)

    def test_single_longoption_without_optionargument(self):
        permutables = ["--silent"]
        self._test_permutations("curl", permutables)

    def test_single_longoption_with_optionargument(self):
        permutables = ["--url www.github.com"]
        self._test_permutations("curl", permutables)

    def test_multiple_longoptions_without_optionarguments(self):
        permutables = ["--silent", "--show-error", "--use-ascii"]
        self._test_permutations("curl", permutables)

    def test_multiple_longoptions_with_optionarguments(self):
        permutables = ["--url www.github.com", "--limit-rate 10", "--data somedata"]
        self._test_permutations("curl", permutables)

    def test_singleoperand(self):
        permutables = ["www.github.com"]
        self._test_permutations("curl", permutables)

    def test_multipleoperands(self):
        permutables = ["-s", "-S", "-P 8080", "www.github.com"]
        self._test_permutations("curl", permutables)
    
    def test_all_arguments(self):
        permutables = ["www.github.com", "-s", "-P 8080", "--data somedata", "--show-error"]
        self._test_permutations("curl", permutables)

    def test_combined_shortoptions_with_an_optionargument(self):
        cmd = "curl -sSP8080 www.github.com"
        args = split(cmd)
        self.assertEqual(["curl", "-s", "-S", "-P", "8080", "www.github.com"], args)
    
    def _test_permutations(self, utility, permutables, expected=None):
        for permutationTuple in itertools.permutations(permutables):
            expected = [utility]
            for i in permutationTuple:
                expected.extend(i.split(" "))
            self.assertEqual(expected, split(" ".join(expected)))
    

if __name__ == '__main__':
    unittest.main(verbosity=2)

