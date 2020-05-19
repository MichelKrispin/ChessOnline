#!/usr/bin/env python3

import inspect
import os
import sys
from contextlib import contextmanager
from enum import Enum

from ..Chess.ChessValidator import ChessValidator


"""
# How To
1. Scroll down to the commented test_..._template method
2. Copy it and rename it to a meaningful name.
   (The name will be used in the ouput)
3. Fill out the chess board to the testing values
4. Set new from and to values
5. Change the text inside the function call to something helpful
6. Set the Expect value to Expect.TRUE if the function call should return true
   or to Expect.FALSE if you expect the move to be invalid.
7. Call the new method from the main at the bottom of this file.
8. Run the file and see whether the test has passed
"""

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
# Enum class for making the test function easier
class Expect():
    FALSE = False
    TRUE = True
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
    result = []
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
    
    for from_string, to_string, description, active_player, expect in (
            ['a1', 'a1', 'Same position and same team', 0, Expect.FALSE],
            ['a1', 'a2', 'Same team', 0, Expect.FALSE],
            ['a1', 'a3', 'Different team ', 1, Expect.FALSE],
            ):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player, description, expect))

    result.append('> Finished')
    return result

# ---------------------------
# Testing the rook
# ---------------------------
def testing_chess_validator_move_rook():
    result = []
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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing across near pawn',
        Expect.FALSE))

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

    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing across 3 step away pawn',
        Expect.FALSE))
        
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
    
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing two steps',
        Expect.TRUE))
        
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

    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing two steps (black team)',
        Expect.TRUE))
        
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

    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing sideways',
        Expect.TRUE))
        
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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing sideways across pawn',
        Expect.FALSE))
        
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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing sideways in front of pawn',
        Expect.TRUE))
        
    # -----

    result.append('> Finished')
    return result

# ---------------------------
# Testing the knight
# ---------------------------
def testing_chess_validator_move_knight():
    result = []
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
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing knight c3 to {to_string} ({count})',
            Expect.TRUE))
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
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing knight (invalid) c3 to {to_string} ({count})',
            Expect.FALSE))
        count += 1

    # ------

    result.append('> Finished')
    return result

# ---------------------------
# Testing the bishop
# ---------------------------
def testing_chess_validator_move_bishop():
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
    
    from_string = 'c1'
    to_string = 'c5'
    active_player = 0
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing straight',
        Expect.FALSE))
        
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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing left diagonal',
        Expect.TRUE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing right diagonal',
        Expect.TRUE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing down left diagonal',
        Expect.TRUE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing down right diagonal (black team)',
        Expect.TRUE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing up right across pawn (black team)',
        Expect.FALSE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing down right across paw',
        Expect.FALSE))

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
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing somewhere',
        Expect.FALSE))

    # ------

    result.append('> Finished')
    return result

# --------------------
# Queen
# --------------------
def testing_chess_validator_move_queen():
    result = []
    chess_validator = ChessValidator()

    # ------
    # First check valid moves

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|      q        |
4|               |
3|               |
2|p p p p p p p p|
1|r n b   k b n r|
""")
    
    from_string = 'd5'
    active_player = 0
    to_strings = ['d6', 'd7', 'f7', 'h5', 'a5', 'b7', 'd3', 'f3']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing queen (invalid) d5 to {to_string} ({count})',
            Expect.TRUE))
        count += 1

    # ------
    # Then invalid moves
    
    to_strings = ['d8', 'e7', 'c3', 'h4', 'g8', 'b6', 'a4', 'd1']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing queen (invalid) e5 to {to_string} ({count})',
            Expect.FALSE))
        count += 1

    # ------

    result.append('> Finished')
    return result

# --------------------
# Testing the king
# --------------------
def testing_chess_validator_move_king():
    result = []
    chess_validator = ChessValidator()

    # ------
    # First check valid moves

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|        k      |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q   b n r|
""")
    
    from_string = 'e5'
    active_player = 0
    to_strings = ['e6', 'd6', 'd5', 'd4', 'e4', 'f4', 'f5', 'f6']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing king e5 to {to_string} ({count})',
            Expect.TRUE))
        count += 1

    # ------
    # Then invalid moves
    
    to_strings = ['d8', 'e7', 'f7', 'e1', 'c5', 'a3', 'd7', 'g6']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing king (invalid) e5 to {to_string} ({count})',
            Expect.FALSE))
        count += 1

    # ------
    # Then drawing next to the other king (valid)
    
    board = generate_board_from_string("""
8|R N B Q   B N R|
7|P P P P P P P P|
6|               |
5|    K     k    |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q   b n r|
""")
    
    from_string = 'f5'
    to_strings = ['e5', 'e6', 'e4']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing king one step away from enemy king e5 to {to_string} ({count})',
            Expect.TRUE))
        count += 1

    # ------
    # Then drawing next to the other king (invalid)
    
    board = generate_board_from_string("""
8|R N B Q   B N R|
7|P P P P P P P P|
6|               |
5|    K   k      |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q   b n r|
""")

    from_string = 'e5'
    to_strings = ['d5', 'd6', 'd4']
    count = 1
    for to_string in to_strings:
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player,
            f'Drawing king (invalid) next to enemy king e5 to {to_string} ({count})',
            Expect.FALSE))
        count += 1

    # ------

    result.append('> Finished')
    return result

# --------------------
# Pawn
# --------------------
def testing_chess_validator_move_pawn():
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
    
    from_strings = ['a2', 'a2']
    to_strings = ['a3', 'a4']
    active_player = 0
    count = 1
    for i in range(len(from_strings)):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_strings[i], to_strings[i], active_player,
            f'Drawing pawn {from_strings[i]} to {to_strings[i]} ({count})',
            Expect.TRUE))
        count += 1

    # ------

    from_strings = ['a7', 'a7']
    to_strings = ['a6', 'a5']
    active_player = 1
    count = 1
    for i in range(len(from_strings)):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_strings[i], to_strings[i], active_player,
            f'Drawing pawn {from_strings[i]} to {to_strings[i]} ({count}) (black team)',
            Expect.TRUE))
        count += 1

    # ------

    from_strings = ['a2', 'a2', 'a2']
    to_strings = ['a5', 'b3', 'b5']
    descriptions = ['Drawing pawn too far', 'Drawing pawn diagonal without enemy', 'Drawing pawn somewhere']
    active_player = 0
    count = 1
    for i in range(len(from_strings)):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_strings[i], to_strings[i], active_player,
            descriptions[i] + f'({from_strings[i]} to {to_strings[i]} - {count})',
            Expect.FALSE))
        count += 1

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P   P P P|
6|               |
5|        P      |
4|      p        |
3|               |
2|p p p   p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'd4'
    to_string = 'e5'
    active_player = 0
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn onto enemy',
        Expect.TRUE))

    # ------

    to_string = 'c5'
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn diagonal without enemy',
        Expect.FALSE))

    # ------

    from_string = 'e5'
    to_string = 'd4'
    active_player = 1
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn diagonal onto enemy (black team)',
        Expect.TRUE))

    # ------

    to_string = 'e6'
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn backwards (black team)',
        Expect.FALSE))

    # ------

    to_string = 'e7'
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn two steps backwards (black team)',
        Expect.FALSE))

    # ------

    to_string = 'd3'
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn backwards',
        Expect.FALSE))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P   P P P|
6|               |
5|               |
4|      p P      |
3|               |
2|p p p   p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'd4'
    to_string = 'e5'
    active_player = 0
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn onto enemy one step sideways (same row)',
        Expect.FALSE))

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P   P P P P|
6|               |
5|      P        |
4|      p        |
3|               |
2|p p p   p p p p|
1|r n b q k b n r|
""")
    
    from_string = 'd4'
    to_string = 'd5'
    active_player = 0
    result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
        board, from_string, to_string, active_player,
        'Drawing pawn onto enemy in front',
        Expect.FALSE))

    # ------

    result.append('> Finished')
    return result

# ---------------------------
# Testing for check moves
# ---------------------------
def testing_chess_validator_check_moves():
    result = []
    chess_validator = ChessValidator()

    # ------

    board = generate_board_from_string("""
8|  N B   K B N  |
7|P P P P P P P P|
6|        Q      |
5|        n      |
4|R   b   k p   R|
3|               |
2|p p p p p   p p|
1|r n   q   b   r|
""")

    from_strings = ['f4', 'c4', 'c4', 'e5']
    to_strings = ['f5', 'd5', 'a6', 'c6']
    active_player = 0
    count = 1
    for i in range(len(from_strings)):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_strings[i], to_strings[i], active_player,
            f'Drawing figure {from_strings[i]} to {to_strings[i]} ({count}) and exposing attack of own king',
            Expect.FALSE))
        count += 1

    # ------

    result.append('> Finished')
    return result

# ---------------------------
# Testing for check for check
# ---------------------------
def testing_chess_validator_check():
    result = []
    chess_validator = ChessValidator()

    # ------

    # Fake the board a little
    chess_validator.board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")

    for activate_player in [0, 1]:
        chess_validator.active_player = activate_player
        with suppress_stdout():
            result.append(test_result(
                chess_validator.check_for_check(),
                f'Default board (Player {activate_player})',
                line_number(),
                Expect.FALSE))

    # ------
    # Attack from behind other player

    chess_validator.board = generate_board_from_string("""
8|  N B   K   N  |
7|P P P P Q P P P|
6|               |
5|        b      |
4|R   n   k p   R|
3|               |
2|p p p p p p p p|
1|r n b q     n B|
""")

    chess_validator.active_player = 0
    with suppress_stdout():
        result.append(test_result(
            chess_validator.check_for_check(),
            f'Attack from behind other player',
            line_number(),
            Expect.FALSE))

    # ------
    # Check for a lot of Rook attacks

    boards = []
    boards.append(generate_board_from_string("""
8|  N B Q   B N R|
7|P P P P P P P P|
6|               |
5|        K     r|
4|R     k        |
3|               |
2|p p p p p p p p|
1|r n b q   b n  |
""")) # 0
    boards.append(generate_board_from_string("""
8|  N B Q   B N R|
7|P P P P P P P P|
6|               |
5|r       K      |
4|      k       R|
3|               |
2|p p p p p p p p|
1|r n b q   b n  |
""")) # 1
    boards.append(generate_board_from_string("""
8|  N B Q   B N R|
7|P P P P P P P P|
6|        r      |
5|        K      |
4|      k        |
3|      R        |
2|p p p p p p p p|
1|r n b q   b n  |
""")) # 2
    boards.append(generate_board_from_string("""
8|  N B Q   B N R|
7|P P P P P P P P|
6|      R        |
5|        K      |
4|      k        |
3|        r      |
2|p p p p p p p p|
1|r n b q   b n  |
""")) # 3
    boards.append(generate_board_from_string("""
8|  N B Q   B N  |
7|P P P P P P P P|
6|      R r      |
5|  r     K     r|
4|  R   k     R  |
3|      R r      |
2|p p p p p p p p|
1|  n b q   b n  |
""")) # 4
    boards.append(generate_board_from_string("""
8|R N B     B N R|
7|P P P P P P P P|
6|               |
5|        K     q|
4|      k     Q  |
3|               |
2|p p p p p p p p|
1|r n b q   b n r|
""")) # 4

    board_count = 0
    for board in boards:
        chess_validator.board = board
        for activate_player in [0, 1]:
            chess_validator.active_player = activate_player
            with suppress_stdout():
                result.append(test_result(
                    chess_validator.check_for_check(),
                    f'Attacked by rook/queen (Player {activate_player} - Board {board_count})',
                    line_number(),
                    Expect.TRUE))
                
        board_count += 1

    # ------
    # Checking the Queen and the Bishop
    boards = []
    boards.append(generate_board_from_string("""
8|R N B     B N R|
7|P P P P P P P P|
6|  Q     K      |
5|               |
4|      k     q  |
3|               |
2|p p p p p p p p|
1|r n b     b n r|
""")) # 0
    boards.append(generate_board_from_string("""
8|R N B     B N R|
7|P P P P P P P P|
6|        K      |
5|               |
4|      k        |
3|  q     Q      |
2|p p p p p p p p|
1|r n b     b n r|
""")) # 1
    boards.append(generate_board_from_string("""
8|R N   Q   B N R|
7|P P P P P P P P|
6|  B     K      |
5|               |
4|      k     b  |
3|               |
2|p p p p p p p p|
1|r n b q     n r|
""")) # 2

    board_count = 0
    for board in boards:
        chess_validator.board = board
        for activate_player in [0, 1]:
            chess_validator.active_player = activate_player
            with suppress_stdout():
                result.append(test_result(
                    chess_validator.check_for_check(),
                    f'Attacked by bishop/queen (Player {activate_player} - Board {board_count})',
                    line_number(),
                    Expect.TRUE))
                
        board_count += 1
    # ------


    result.append('> Finished')
    return result

# ---------------------------
# Testing for king can be saved
# ---------------------------
def testing_chess_validator_king_can_be_saved():
    result = []
    chess_validator = ChessValidator()

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N  |
7|P P P P P P P P|
6|               |
5|        k     R|
4|               |
3|               |
2|p p p p p p p p|
1|r n b q   b n r|
""")
    
    chess_validator.to_col = 'a'
    chess_validator.to_row = 3
    chess_validator.from_col = 'a'
    chess_validator.from_row = 2
    chess_validator.board = board
    chess_validator.active_player = 0
    chess_validator.attackers = [['h', 4]]
    with suppress_stdout():
        result.append(test_result( chess_validator.validate_king_can_be_saved(),
            f'Attacked by one Rook',
            line_number(),
            Expect.TRUE))

    # Check the to and from spots 
    with suppress_stdout():
        result.append(test_result(
            (chess_validator.to_col == 'a' and chess_validator.to_row == 3 and
            chess_validator.from_col == 'a' and chess_validator.from_row == 2 and
            chess_validator.attackers == [['h', 4]]),
            f'Correctly restoring the old spots',
            line_number(),
            Expect.TRUE))

    # ------
    # Now check for when he can't escape 

    board = generate_board_from_string("""
8|  N B       N  |
7|P P P P P P P P|
6|R              |
5|    Q   k     R|
4|               |
3|      B K      |
2|p p p p p p p p|
1|r n b q   b n r|
""")

    chess_validator.board = board
    chess_validator.attackers = [['h', 4], ['c', 4]]
    with suppress_stdout():
        result.append(test_result(
            chess_validator.validate_king_can_be_saved(),
            'Check mate by R,Q,B,K',
            line_number(),
            Expect.FALSE))

    # ------
    # And at the end test for special cases

    boards = []
    boards.append(generate_board_from_string("""
8|R N B   K B N R|
7|P P P P P P P P|
6|               |
5|        Q      |
4|               |
3|               |
2|p p p p   p p p|
1|r n b q k b n r|
""")) # 0
    boards.append(generate_board_from_string("""
8|R N B   K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|               |
2|p p p p Q p p p|
1|r n b q k b n r|
""")) # 1
    boards.append(generate_board_from_string("""
8|R N B   K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|              Q|
3|               |
2|p p p p     p p|
1|r n b q k b n r|
""")) # 2

    attackers = [[['e', 4]], [['e', 1]], [['h', 3]]]
    count = 0
    for board in boards:
        chess_validator.board = board
        chess_validator.attackers = attackers[count]
        with suppress_stdout():
            result.append(test_result(
                chess_validator.validate_king_can_be_saved(),
                f'King can be saved (board {count})',
                line_number(),
                Expect.TRUE))
        count += 1

    # ------

    result.append('> Finished')
    return result

'''
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

def run_individiual_chess_validate(line, validate, board, from_string, to_string, player, msg, expect):
    """
    This is just a wrapper function so the tests get shorter and
    hopefully a little bit more readable.
    It suppresses the standard out for the validate function so there won't be 
    anything printed by the validation function.
    """
    result = ''
    with suppress_stdout():
        try:
            result = test_result(
                validate(
                board, from_string, to_string, player),
                msg,
                line,
                expect)
        except Exception as e:
            result = f'- Test ({msg}) at line {line} threw {str(e)}'
    return result

def test_result(result, out_message, line_number, expect):
    """
    The result of the testing function should be put into the result
    argument, the message which describes this test to out_message
    and if the test fails if the bool is true also specify
    success_on_false to be False.
    Returns the message with success or failed.
    """
    if expect == Expect.TRUE:
        result = not result
    if not result:
        return ('+ ' + out_message)
    option_msg = ' (expected True)' if expect else ' (expected False)'
    return ('- FAILED - ' + str(line_number) + ' - ' + out_message + option_msg)
    

def run_test(testing_function, shorten):
    """
    Run a test and print its results.
    """
    # Title capitalizes the first letter of each word
    test_name = '>> ' + testing_function.__name__.replace('_', ' ').title()
    print(test_name)

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
    global test_counter 
    test_counter += len(r) - 1 # Minus the > Finished

def run_all_tests(shorten=True):
    global test_counter
    test_counter = 0

    run_test(testing_chess_validator_move_generic, shorten)
    run_test(testing_chess_validator_move_rook, shorten)
    run_test(testing_chess_validator_move_knight, shorten)
    run_test(testing_chess_validator_move_bishop, shorten)
    run_test(testing_chess_validator_move_queen, shorten)
    run_test(testing_chess_validator_move_king, shorten)
    run_test(testing_chess_validator_move_pawn, shorten)
    run_test(testing_chess_validator_check, shorten)
    run_test(testing_chess_validator_check_moves, shorten)
    run_test(testing_chess_validator_king_can_be_saved, shorten)

    print(f'Ran {test_counter} tests')
    