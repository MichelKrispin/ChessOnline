from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
