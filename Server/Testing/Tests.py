#!/usr/bin/env python3

import importlib
import os
import pkgutil
import sys
from inspect import getmembers, isfunction

from .. import Testing
from ..Chess.ChessValidator import ChessValidator

"""
# ---------
# How To
# ---------
1. Copy everything out of the TEST CASE TEMPLATE comment (the TEST CASE TEMPLATE comment itself isn't necessary...)
2. Create a new file inside of this folder and name it to something meaningful. The function should have the same name.
   !!! It has to start with testing_ . Otherwise it won't be noticed as a test.
   (The name will be used in the ouput)
3. Customize the test (you can look for reference in the other test files)
   3.1 Normally the board is adjusted for a specific move
   3.2 Then the to and from draws are customized for this test
   3.3 The description should be meaningful. If the test fails this will be helpful.
   3.4 The team is either 0 (white) or 1 (black)
   3.5 If the test should fail (e.g. the move should'nt work) its Expect.False and vice versa
   3.6 You can create custom helper functions inside of the files just don't let them start with testing_
4. Run the file and see whether the test has passed

Notes:
- The testing suppresses all printing to console of the actual functions
"""

'''
# TEST CASE TEMPLATE
from .Helper import *
from ..Chess.ChessValidator import ChessValidator

def testing_chess_validator_template():
    result = []
    chess_validator = ChessValidator()

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    for from_string, to_string, description, active_player, expect in (
            ['a1', 'a1', 'Same position and same team', 0, Expect.FALSE],
            ['a1', 'a2', 'Same team', 0, Expect.FALSE],
            ['a1', 'a3', 'Different team ', 1, Expect.FALSE],
            ['a7', 'a9', 'Row out of board', 1, Expect.FALSE],
            ['h1', 'g1', 'Col out of board', 0, Expect.FALSE],
            ):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player, description, expect))

    # ------

    result.append('> Finished')
    return result
'''

"""
REMINDER
  _______________
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
 |_______________|
  a b c d e f g h
"""

class Test():
    def __init__(self, shorten=True):
        self.shorten = True
        self.test_counter = 0
        self.failed_tests = []

    def run(self, shorten=True):
        """
        Looks trough all submodules inside this module.
        Then it looks for all files starting with testing_
        and imports their function and then runs their test.
        """

        # Check all submodules for testing_... files and call their testing_... function
        submodules = self.import_submodules(Testing)
        for name in submodules.keys():
            # Only import it if 
            if '.testing_' in name:
                functions_list = [f for f in getmembers(submodules[name]) if isfunction(f[1])]
                
                test_function = None
                # If there is more than one function only call the function with testing_ in front
                if len(functions_list):
                    for function in functions_list:
                        name, _ = function
                        if 'testing_' in name:
                            _, test_function = function
                            break
                else:
                    _, test_function = functions_list[0]
                
                # Then run this function as a test
                self.run_test(test_function, self.shorten)

        # Then make a summary
        print('\n----- Summary -----')
        print(f'Ran {self.test_counter} tests')
        
        # If there failed some tests list the
        if len(self.failed_tests):
            print(f'    {len(self.failed_tests)} failed')
            for result, f in self.failed_tests:
                print(f'    -> {result.replace("- FAILED - ", f"In {f}, ")}')
        else:
            print('All tests succeeded')
        
    def run_test(self, testing_function, shorten):
        """
        Run a single test and print its results.
        """
        # Title capitalizes the first letter of each word
        test_name = '>> ' + testing_function.__name__.replace('_', ' ').title()
        print(test_name)

        # Get the result of the testing function and print it according to arguments
        result = testing_function()
        for r in result:
            if shorten:
                if '+' in r:
                    print('+ ', end='')
                else:
                    print('\n' + r)
            else:
                print(r)

            # If the test failed add it to the list of failed tests
            if 'FAILED' in r:
                self.failed_tests.append((r, testing_function.__name__,))
        print('')

        self.test_counter += len(result) - 1 # Minus the > Finished

    def import_submodules(self, package, recursive=True):
        """
        (Copied from stackoverflow)
        Import all submodules of a module, recursively, including subpackages.
        The package should be an imported package.
        In this case its this packages parent.
        It returns a dict of {name: module}.
        """
        if isinstance(package, str):
            package = importlib.import_module(package)
        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(import_submodules(full_name))
        return results
