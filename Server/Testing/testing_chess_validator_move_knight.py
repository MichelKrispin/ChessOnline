from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
