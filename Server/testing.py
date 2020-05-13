#!/usr/bin/env python3

from ChessValidator import ChessValidator
from contextlib import contextmanager
import sys, os
import inspect
import argparse

# --------------------
# For suppressing the output of the functions which are tested
# (copied from stackoverflow)
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

# ------------------
# The line number to show where something failed
def line_number():
    """Returns the current line number."""
    return inspect.currentframe().f_back.f_lineno
# ------------------

# ------------------
# A helper function
def generate_board_from_string(string):
    """
    A helper function to generate a board from a
    string so there is no need to always state the
    mirrored dictionary.
    The string should be given as:
    8|R N B Q K B N R|
    7|P P P P P P P P|
    6|               |
    5|               |
    4|               |
    3|               |
    2|p p p p p p p p|
    1|r n b q k b n r|

    -> Linue numbers for readability
    -> | to indicate start and end
    -> Spaces in between
    -> Spaces for empty spots
    """
    board = {
        'a': ['', '', '', '', '', '', '', ''],
        'b': ['', '', '', '', '', '', '', ''],
        'c': ['', '', '', '', '', '', '', ''],
        'd': ['', '', '', '', '', '', '', ''],
        'e': ['', '', '', '', '', '', '', ''],
        'f': ['', '', '', '', '', '', '', ''],
        'g': ['', '', '', '', '', '', '', ''],
        'h': ['', '', '', '', '', '', '', ''],
    }
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    col_index = 0
    row_index = 7
    i = 0
    while i < len(string):
        if string[i] not in ['r', 'R', 'n', 'N', 'b', 'B', 'q', 'Q', 'k', 'K', 'p', 'P', ' ']:
            i += 1
            continue

        try:
            board[columns[col_index]][row_index] = string[i]
            i += 1
        except IndexError:
            print(f'Index error using col_index: {col_index} and row_index: {row_index}')
            return
        # Skip next element and go on
        i += 1

        col_index += 1
        if col_index > 7:
            col_index = 0
            row_index -= 1
        if row_index < 0:
            break

    return board
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

# ---------------------------
# Testing generic moves 
# ---------------------------
def testing_chess_validator_move_generic():
    """
    Testing generic stuff such as inputting same position or same team.
    """
    result = ['>> Testing Generic']
    chess_validator = ChessValidator()
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
    
    from_string = 'a1'
    to_string = 'a1'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Same position and same team',
            line_number()))

    # -----

    from_string = 'a1'
    to_string = 'a2'
    active_player = 0
    
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Same team',
            line_number()))

    # -----

    from_string = 'a1'
    to_string = 'a3'
    active_player = 1
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Different team',
            line_number()))

    # -----
    
    result.append('> Finished')
    return result

# ---------------------------
# Testing the rook
# ---------------------------
def testing_chess_validator_move_rook():
    result = ['>> Testing Move Rook']
    chess_validator = ChessValidator()
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
    
    from_string = 'a1'
    to_string = 'a3'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing across near pawn',
            line_number()))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|p              |
3|               |
2|  p p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'a1'
    to_string = 'a5'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing across 3 step away pawn',
            line_number()))
        
    # -----

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|p              |
3|               |
2|  p p p p p p p|
1|r n b q k b n r|
""")
    from_string = 'a1'
    to_string = 'a3'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing two steps',
            line_number(),
            False))
        
    # -----

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|  P P P P P P P|
6|               |
5|               |
4|P              |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'a8'
    to_string = 'a5'
    active_player = 1

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing two steps (black team)',
            line_number(),
            False))
        
    # -----

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|r              |
3|               |
2|p p p p p p p p|
1|  n b q k b n r|
""")
    
    from_string = 'a4'
    to_string = 'g4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways',
            line_number(),
            False))
        
    # -----

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|r     p        |
3|               |
2|p p p   p p p p|
1|  n b q k b n r|
""")
    
    from_string = 'a4'
    to_string = 'g4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways across pawn',
            line_number()))
        
    # -----

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|r             p|
3|               |
2|p p p p p p p  |
1|  n b q k b n r|
""")
    
    from_string = 'a4'
    to_string = 'f4'
    active_player = 0

    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing sideways in front of pawn',
            line_number(),
            False))
        
    # -----

    result.append('> Finished')
    return result

# ---------------------------
# Testing the knight
# ---------------------------
def testing_chess_validator_move_knight():
    result = ['>> Testing Move Knight']
    chess_validator = ChessValidator()

    # ------
    # Check all possible moves

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|p   n   p     q|
2|  p p p   p p p|
1|r   b   k b n r|
""")
    
    from_string = 'c3'
    active_player = 0

    to_strings = ['d1', 'b1', 'a2', 'a4', 'b5', 'd5', 'e4', 'e2']
    count = 1
    for to_string in to_strings:
        with suppress_stdout():
            result.append(test_result(
                chess_validator.validate_move(
                board, from_string, to_string, active_player),
                (f'Drawing knight c3 to {to_string} ({count})'),
                line_number(),
                False))
        count += 1

    # ------
    # Test moves that shouldn't work

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|     N         |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'd5'
    active_player = 0

    to_strings = ['d6', 'e5', 'c5', 'd4', 'h1', 'a5', 'h3', 'f1']
    count = 1
    for to_string in to_strings:
        with suppress_stdout():
            result.append(test_result(
                chess_validator.validate_move(
                board, from_string, to_string, active_player),
                (f'Drawing knight (invalid) c3 to {to_string} ({count})'),
                line_number()))
        count += 1

    # ------

    result.append('> Finished')
    return result

# ---------------------------
# Testing the bishop
# ---------------------------
def testing_chess_validator_move_bishop():
    result = ['>> Testing Move Bishop']
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
    
    from_string = 'c1'
    to_string = 'c5'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing straight',
            line_number()))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|  p            |
2|p   p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'c1'
    to_string = 'a3'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing left diagonal',
            line_number(),
            False))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|        b      |
2|p p p p p p p p|
1|r n   q k b n r|
""")
    
    from_string = 'e3'
    to_string = 'h6'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing right diagonal',
            line_number(),
            False))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|          b    |
5|               |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k   n r|
""")
    
    from_string = 'f6'
    to_string = 'c3'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing down left diagonal',
            line_number(),
            False))

    # ------

    board = generate_board_from_string("""
8|R N B Q K   N R|
7|P P P P P P P P|
6|               |
5|    B          |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'c5'
    to_string = 'e3'
    active_player = 1
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing down right diagonal (black team)',
            line_number(),
            False))

    # ------

    board = generate_board_from_string("""
8|R N B Q K   N R|
7|P P P P P P P P|
6|               |
5|    B          |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'c5'
    to_string = 'f8'
    active_player = 1
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing up right across pawn (black team)',
            line_number()))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|    b          |
4|      p        |
3|               |
2|p p p p p p p p|
1|r n b q k   n r|
""")
    
    from_string = 'c5'
    to_string = 'e3'
    active_player = 1
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing down right across pawn',
            line_number()))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|        b      |
2|p p p p p p p p|
1|r n   q k b n r|
""")
    
    from_string = 'e3'
    to_string = 'b8'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing somewhere',
            line_number()))

    # ------

    result.append('> Finished')
    return result

'''
def testing_chess_validator_template():
    result = ['>> Testing Move Rook']
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
    
    from_string = 'a1'
    to_string = 'a3'
    active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_move(
            board, from_string, to_string, active_player),
            'Drawing across near pawn',
            line_number()))

    # ------

    result.append('> Finished')
    return result
'''

def test_result(result, out_message, line_number, success_on_false=True):
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
    return ('- FAILED - ' + str(line_number) + ' - ' + out_message)
    

def run_test(testing_function, shorten):
    """
    Run a test and print its results.
    """
    result = testing_function()
    for r in result:
        if shorten:
            if '+' in r:
                print('+ ', end='')
            else:
                print('\n' + r)
        else:
            print(r)
    print('')    

def parse_arguments():
    """
    Parse the command line arguments if there are any.
    """
    parser = argparse.ArgumentParser(description='Test all existing test cases.')
    # Add the shorten argument
    parser.add_argument(
            'shorten',
            help='Shorten the output to print only the details of failed tests.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    shorten = True if args.shorten else False
    run_test(testing_chess_validator_move_generic, shorten)
    run_test(testing_chess_validator_move_rook, shorten)
    run_test(testing_chess_validator_move_knight, shorten)
    run_test(testing_chess_validator_move_bishop, shorten)

