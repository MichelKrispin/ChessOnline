from .Helper import *
from ..Chess.ChessValidator import ChessValidator

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
            'Check mate by R,Q,B,K (King cannot be saved)',
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
    boards.append(generate_board_from_string("""
8|R N B     B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|        K      |
2|p p p   Q   p p|
1|r n b q k b n r|
""")) # 3
    boards.append(generate_board_from_string("""
8|R N B Q K B   R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|          N    |
2|p p p p p p p p|
1|r n b q k b n r|
""")) # 4
    boards.append(generate_board_from_string("""
8|R N B Q K B N  |
7|P P P P P P P P|
6|               |
5|        R      |
4|r              |
3|      p   p    |
2|p p   p k p   p|
1|  n b q   b n r|
""")) # 5

    attackers = [
        [['e', 4]],
        [['e', 1]],
        [['h', 3]],
        [['e', 1]],
        [['f', 2]],
        [['e', 4]],
    ]
    descriptions = [
        "Other figure stepping in between",
        "King attacks attacker himself",
        "King stepps away",
        "Bishop or knight attacks attacker (king can't move)",
        "Someone attacks knight (king can't move)",
        "Rook steps in (king can't move)",
    ]
    count = 0
    for board in boards:
        chess_validator.board = board
        chess_validator.attackers = attackers[count]
        with suppress_stdout():
            result.append(test_result(
                chess_validator.validate_king_can_be_saved(),
                descriptions[count] + f' (board {count})',
                line_number(),
                Expect.TRUE))
        count += 1

    # ------

    result.append('> Finished')
    return result