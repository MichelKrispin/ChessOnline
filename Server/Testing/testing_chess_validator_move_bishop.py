from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
