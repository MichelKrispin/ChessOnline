from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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