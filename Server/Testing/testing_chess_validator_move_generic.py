from .Helper import *
from ..Chess.ChessValidator import ChessValidator

def testing_chess_validator_move_generic():
    """
    Testing generic stuff such as inputting same position or same team.
    """
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
    
    for from_string, to_string, description, active_player, expect in (
            ['a1', 'a1', 'Same position and same team', 0, Expect.FALSE],
            ['a1', 'a2', 'Same team', 0, Expect.FALSE],
            ['a1', 'a3', 'Different team ', 1, Expect.FALSE],
            ):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player, description, expect))

    result.append('> Finished')
    return result
