from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
