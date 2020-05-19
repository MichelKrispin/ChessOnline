from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
