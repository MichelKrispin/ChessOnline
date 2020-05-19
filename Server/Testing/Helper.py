import inspect
import os
import sys
from contextlib import contextmanager
from enum import Enum


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
