from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
