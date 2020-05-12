class ChessValidator():

    def validate_move(self, board, from_string, to_string, active_player):
        """
        Validates whether the move is valid.
        The board is a dictionary with lists such as
        board = {
            'h': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
            'g': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
            'f': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
            'e': ['q', 'p', ' ', ' ', ' ', ' ', 'P', 'Q'],
            'd': ['k', 'p', ' ', ' ', ' ', ' ', 'P', 'K'],
            'c': ['b', 'p', ' ', ' ', ' ', ' ', 'P', 'B'],
            'b': ['n', 'p', ' ', ' ', ' ', ' ', 'P', 'N'],
            'a': ['r', 'p', ' ', ' ', ' ', ' ', 'P', 'R'],
        }
        # It is mirrored as the letter is usually used first
        # With this convention any field can be addresses using
        # board['a'][1]
        from_string = 'a1'
        to_string = 'b2'

        The from_string and to_string always contain a character
        at the front raning from a lower 'a' to a lower 'h'.
        The second character is an integer (encoded as a character)
        ranging from '1' to '8'.

        active_player = 0 or 1
        0 means white team, 1 means black team
        """
        # Update all parameters of the class
        self.board = board
        self.from_row = int(from_string[1]) - 1
        self.from_col = from_string[0] 
        self.to_row = int(to_string[1]) - 1
        self.to_col = to_string[0] 
        self.active_player = active_player

        # Rules
        # -----
        
        # TODO: Maybe add special rules before?

        # - If there is no figure of the own team on the source spot
        if not self.validate_figure_from_active_team():
            return False

        # - If there is already a figure of the from team
        if not self.validate_from_same_team_or_enemy_king():
            return False

        # - If the destination is allowed by the figure type
        if not self.validate_figure_type_in_range():
            return False

        print("Validator -> Valid move")
        return True

    def validate_figure_from_active_team(self):
        """
        Validates whether the figure on the source spot actually belongs
        to the active players team.
        """
        # TODO: Validate whether the figure is from active team
        valid_range = ord('a') # White team is between a-z (ord gets ascii value)
        if self.active_player:
            valid_range = ord('A')

        source_figure = self.board[self.from_col][self.from_row]
        print(
            f"Validator -> source_figure at {ord(source_figure)} in range {valid_range} to {valid_range+26}"
        )
        # If not in the range of a/A to z/Z return False
        if ord(source_figure) < valid_range or ord(source_figure) > valid_range + 26:
            return False

        return True

    def validate_from_same_team_or_enemy_king(self):
        """
        Validates whether the source and destination is from the same team
        or if the source is the enemy king. Both would be invalid.
        Otherwise True will be returned.
        """
        # TODO: Validate from same team
        return True
    
    def validate_figure_type_in_range(self):
        """
        Validates whether the figure is allowed to go to that position.
        E.g. a King is only allowed to go one step away from his position.
        """
        # TODO: Validate if figure type goes to the correct destination
        return True

    def check_mate(self):
        """
        Checks whether there is a checkmate
        """
        # TODO: Check for checkmate
        return False

    def stale_mate(self):
        """
        Checks whether there is a stalemate
        """
        # TODO: Check for stalemate
        return False

