#!/usr/bin/env python3

from ChessValidator import ChessValidator
from contextlib import contextmanager
import sys, os

# --------------------
# For suppressing the output of the functions which are tested
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
# ------------------

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

def testing_chess_validator_move_generic():
    """
    Testing generic stuff such as inputting same position or same team.
    """
    result = ['>> Testing Generic']
    chess_validator = ChessValidator()
    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a1'
    to_string = 'a1'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Same position and same team'))

    # -----

    from_string = 'a1'
    to_string = 'a2'
    active_player = 0
    
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Same team'))

    # -----

    from_string = 'a1'
    to_string = 'a3'
    active_player = 1
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Different team'))

    # -----
    
    result.append('> Finished')
    return result


def testing_chess_validator_move_rook():
    result = ['>> Testing Move Rook']
    chess_validator = ChessValidator()
    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a1'
    to_string = 'a3'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing across near pawn'))

    # ------

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': ['r', ' ', ' ', 'p', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a1'
    to_string = 'a5'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing across 3 step away pawn'))
        
    # -----

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': ['r', ' ', ' ', 'p', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a1'
    to_string = 'a3'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing two steps',
            False))
        
    # -----

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': ['r', 'p', ' ', 'P', ' ', ' ', ' ', 'R'],
    }
    
    from_string = 'a8'
    to_string = 'a5'
    active_player = 1

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing two steps (black team)',
            False))
        
    # -----

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': [' ', 'p', ' ', 'r', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a4'
    to_string = 'g4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways',
            False))
        
    # -----

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', ' ', ' ', 'p', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': [' ', 'p', ' ', 'r', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a4'
    to_string = 'g4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways across pawn'))
        
    # -----

    board = {
        'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        'g': ['n', 'p', ' ', 'p', ' ', ' ', 'P', 'N'],
        'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
        'd': ['k', ' ', ' ', ' ', ' ', ' ', 'P', 'K'],
        'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
        'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
        'a': [' ', 'p', ' ', 'r', ' ', ' ', 'P', 'R'],
    }
    
    from_string = 'a4'
    to_string = 'f4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways in front of pawn',
            False))
        
    # -----

    result.append('> Finished')
    return result

def test_result(result, out_message, success_on_false=True):
    """
    The result of the testing function should be put into the result
    argument, the message which describes this test to out_message
    and if the test fails if the bool is true also specify
    success_on_false to be False.
    Returns the message with success or failed.
    """
    if not success_on_false:
        result = not result
    if not result:
        return ('+ ' + out_message)
    return ('- FAILED - ' + out_message)
    

def run_test(testing_function):
    """
    Run a test and print its results
    """
    result = testing_function()
    for r in result:
        print(r)
    print('')    

if __name__ == '__main__':
    run_test(testing_chess_validator_move_generic)
    run_test(testing_chess_validator_move_rook)