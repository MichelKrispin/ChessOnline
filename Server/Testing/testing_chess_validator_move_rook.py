from .Helper import *
from ..Chess.ChessValidator import ChessValidator


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