from ChessValidator import ChessValidator
from enum import Enum


class ChessMove(Enum):
    """
    Simple enum to determine the result of a move.
    """
    INVALID_MOVE = -1
    PASSED = 0
    CHECK_MATE = 1
    STALE_MATE = 2


class ChessBoard():
    """
    The class that holds the actual information of the board.
    Where is which figure etc.
    The game is only using letters so the default board looks like
      _______________
    8|R N B Q K B N R|
    7|P P P P P P P P|
    6|               |
    5|               |
    4|               |
    3|               |
    2|p p p p p p p p|
    1|r n b q k b n r|
     |_______________|
      a b c d e f g h

    Capital letters is the black team.
    Small the white team.
    """
    def __init__(self):
        # The board is defined as 8 rows but mirrored here
        self.board = {
            'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
            'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
            'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
            'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
            'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
            'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
            'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
            'a': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        }
        self.chess_validator = ChessValidator()

    def make_move(self, from_string, to_string, active_player):
        """
        Making a move. This method expects valid from and to strings.
        They have to be in the form a1 to h8.
        """
        # Validate move
        if not self.chess_validator.validate_move(
                self.board, from_string, to_string, active_player):
            return ChessMove.INVALID_MOVE

        if self.chess_validator.check_mate():
            return ChessMove.CHECK_MATE
        elif self.chess_validator.stale_mate():
            return ChessMove.STALE_MATE

        # If everything passed make the move (chess indices start from 1)
        figure = self.board[from_string[0]][int(from_string[1])-1]
        self.board[from_string[0]][int(from_string[1])-1] = ' '
        self.board[to_string[0]][int(to_string[1])-1] = figure
        return ChessMove.PASSED

    def render_to_byte_text(self):
        """
        Renders all board information to a byte string which can be send.
        The string has all information separated by commmas and a dot for line break.
        The default board would be send as:
        R,N,B,Q,K,B,N,R.P,P,P,P,P,P,P,P. , , , , , , , . , , , , , , , . , , , , , , , . , , , , , , , .p,p,p,p,p,p,p,p.r,n,b,q,k,b,n,r.
        """
        result = ''
        for index in [7, 6, 5, 4, 3, 2, 1, 0]:
            for char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                if char != 'a':
                    result += ','
                result += self.board[char][index]
            result += '.'

        return result.encode()

