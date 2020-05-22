import sys

from .ChessMove import ChessMove
from .ChessBoard import ChessBoard


class ChessGame():
    """
    The class which handles all of the chess logic and
    sends the computed data then back to the client.
    """
    player = { 'white': 0, 'black': 1 } # Helper dictionary
    player_string = { 0: 'white', 1: 'black' }

    def __init__(self, verbose=True):
        """ Creates a new chess game. """
        # Initialize all variables
        self.active_player = self.player['white']
        self.inactive_player = self.player['black']

        # Only for showing more information
        self.verbose = verbose

        # Create a chess board
        self.chess_board = ChessBoard()

    def make_move(self, from_col, from_row, to_col, to_row):
        """
        Make a move in the chess game.
        This method returns one element of the ChessMove Enum which can be compared against.
        Expects str for the columns and int as rows.
        These should also be between 'a'-'h' and 1-8 (inclusive). Otherwise it will be an invalid turn.
        """
        # If the input data is invald return invalid move
        if not self.validate_move_input(from_col, from_row, to_col, to_row):
            return ChessMove.INVALID_MOVE

        # Concatenate the input for the chess board
        move = self.chess_board.make_move(
            from_col + str(from_row), to_col + str(to_row), self.active_player)

        # If the move was invalid return it
        if move == ChessMove.INVALID_MOVE:
            return move

        # Otherwise switch the players and return the move value then
        self.switch_player()
        return move

    def switch_player(self):
        """ Switch to one or the other player after a round. """
        if self.active_player:
            self.active_player = self.player['white']
            self.inactive_player = self.player['black']
        else:
            self.active_player = self.player['black']
            self.inactive_player = self.player['white']

    def validate_move_input(self, from_col, from_row, to_col, to_row):
        """
        Check whether the data is a string which start with
        two characters such as a1 and ends with them.
        Allowed are characters from a-h and numbers from 1-8
        In ASCII the valid range is
         a    1  -   h   8
        (97)(49) - (104)(56)
        """
        # First check whether the types are correct
        if (type(from_col) != str or type(to_col) != str or
            type(from_row) != int or type(to_row) != int):
            return False

        # If first character isn't between a and h
        # If row character isn't between 1 and 8
        if ('a' <= from_col <= 'h' and
            1 <= from_row <= 8 and
            'a' <= to_col <= 'h' and
            1 <= to_row <= 8):
            return True
        
        return False # If its not in that range its invalid

    @property
    def board(self):
        """ Returns the chess board as a string to be send to a client. """
        return self.chess_board.render_to_text()

    @property
    def board_as_bytes(self):
        """ Returns the chess board as a byte string to be send to a client. """
        return self.chess_board.render_to_text().encode()

    @property
    def state(self):
        """
        Returns the current state of the chess board.
        This is string containing each field from the top left to the bottom right
        as a string. If a field is empty this is indicated by a space.
        E.g. RNBQKBNR PP PPPP  ... and so on
        """
        return self.chess_board.render_to_state()
