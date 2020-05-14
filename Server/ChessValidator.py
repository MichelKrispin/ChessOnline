class ChessValidator():
    def __init__(self):
        self.columns = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

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
            print('validate_figure_from_active_team failed')
            return False

        # - If there is already a figure of the from team
        if not self.validate_from_same_team_or_enemy_king():
            print('validate_from_same_team_or_enemy_king failed')
            return False

        # - If the destination is allowed by the figure type
        if not self.validate_figure_type_in_range():
            print('validate_figure_type_in_range failed')
            return False

        print("Validator -> Valid move")
        return True

    def validate_figure_from_active_team(self):
        """
        Validates whether the figure on the source spot actually belongs
        to the active players team.
        """
        valid_range = ord('a') # White team is between a-z (ord gets ascii value)
        if self.active_player:
            valid_range = ord('A')

        source_figure = self.board[self.from_col][self.from_row]
        # If not in the range of a/A to z/Z return False
        if ord(source_figure) < valid_range or ord(source_figure) > valid_range + 26:
            return False

        return True

    def validate_from_same_team_or_enemy_king(self):
        """
        Validates whether the source and destination is from the same team
        or if the destination is the enemy king. Both would be invalid.
        Otherwise True will be returned.
        """
        source_figure = self.board[self.from_col][self.from_row]
        destination_figure = self.board[self.to_col][self.to_row]

        # If there is no figure on the source spot it failed
        if source_figure == ' ':
            return False

        # If there is no figure on the destination spot we don't care
        if destination_figure == ' ':
            return True

        # If destination figure is a King it failed
        if destination_figure == ord('k') or destination_figure == ord('K'):
            return False

        # If both figures are in the same range it failed
        if ord(source_figure) - ord('a') - 1 > 0: # Source is team white (small letters)
            # If destination figure is also white its invalid
            if ord(destination_figure) - ord('a') > 0:
                return False
        else: # If negative it is team black (capital letters)
            # If destination figure is also black its invalid
            if ord(destination_figure) - ord('a') < 0:
                return False

        return True
    
    def validate_figure_type_in_range(self):
        """
        Validates whether the figure is allowed to go to that position.
        E.g. a King is only allowed to go one step away from his position.
        """
        # TODO: Validate if figure type goes to the correct destination

        figure = self.board[self.from_col][self.from_row]
        # There are two types of figures unique ones and generic ones
        # First the generic ones are validated
        # These are r/R, b/B, n/N, q/Q, k/K

        if figure in ['r', 'R']: # Rook
            # Rook is allowed to go along the column and rows
            # So either the columns or the rows must be the same
            print('Figure is r/R')
            if (self.from_col != self.to_col and
                self.from_row != self.to_row):
                return False
            
            # Then there can't be something in between
            # So go trough the whole row and check whether there is something in between
            if self.from_col == self.to_col:
                smaller, greater = self.max_out_of_two(self.from_row, self.to_row)
                # Go trough all but the latest as this one could be a figure
                for i in range(1, greater - smaller):
                    if self.board[self.from_col][smaller + i] != ' ':
                        return False

            # Otherwise go trough the whole column
            elif self.from_row == self.to_row:
                smaller, greater = self.max_out_of_two(self.from_col, self.to_col)
                # Go trough all but the latest as this one could be a figure
                for i in range(1, ord(greater) - ord(smaller)):
                    if self.board[chr(ord(smaller) + i)][self.from_row] != ' ':
                        return False

        elif figure in ['n', 'N']: # White Knight
            print('Figure is n')
            # The knight can go two steps in one direction and one step
            # in the perpendicular direction
            # This means the difference between source and destination column
            # has to be 1 or 2. Same for the rows.
            # If the column difference is 1 the row difference has to be 2.
            # So the addition of the absolute difference has to be 3. Always.
            # Otherwise its not a valid move.
            col_difference = abs(ord(self.to_col) - ord(self.from_col))
            row_difference = abs(self.to_row - self.from_row)
            if col_difference + row_difference != 3:
                return False

        elif figure in ['b', 'B']: # Bishop
            # The difference between the columns and the rows has to be the same
            # because the Bishop is allowed to walk in diagonal lines
            print('Figure is b/B')
            if (abs(ord(self.from_col) - ord(self.to_col)) !=
                abs(self.from_row - self.to_row)):
                return False

            # Then the only thing to check is whether there is some figure in between
            # as the destination spot can't be a king or any same team figure etc.
            col_difference = ord(self.to_col) - ord(self.from_col)
            row_difference = self.to_row - self.from_row

            # Decrement them once so the destincation spot is skipped
            if row_difference > 0: row_difference -= 1
            else: row_difference += 1
            if col_difference > 0: col_difference -= 1
            else: col_difference += 1
            # As row and column difference grow equally this could also be col_difference
            while row_difference != 0:
                if self.board[
                        chr(ord(self.from_col) + col_difference)][
                                self.from_row + row_difference] != ' ':
                    return False

                # Then update the indices
                if row_difference > 0: row_difference -= 1
                else: row_difference += 1
                if col_difference > 0: col_difference -= 1
                else: col_difference += 1

        elif figure in ['q', 'Q']: # Queen
            # TODO: Validate Queen
            # The queen is a combination of the rook and the bishop so everything is just
            # split up into two geater ifs and then the source of the rook and the bishop
            # is copied down there
            print('Figure is q/Q')
            # If the columns and destinations aren't the same its a bishop move (or invalid)
            if (self.from_col != self.to_col and
                self.from_row != self.to_row):
                # Check whether it is actually a rook move - if not mark as invalid
                if (abs(ord(self.from_col) - ord(self.to_col)) !=
                    abs(self.from_row - self.to_row)):
                    return False

                col_difference = ord(self.to_col) - ord(self.from_col)
                row_difference = self.to_row - self.from_row

                if row_difference > 0: row_difference -= 1
                else: row_difference += 1
                if col_difference > 0: col_difference -= 1
                else: col_difference += 1

                while row_difference != 0:
                    if self.board[
                            chr(ord(self.from_col) + col_difference)][
                                    self.from_row + row_difference] != ' ':
                        return False

                    if row_difference > 0: row_difference -= 1
                    else: row_difference += 1
                    if col_difference > 0: col_difference -= 1
                    else: col_difference += 1
            
            # Otherwise its a rook move
            else:
                if self.from_col == self.to_col:
                    smaller, greater = self.max_out_of_two(self.from_row, self.to_row)
                    for i in range(1, greater - smaller):
                        if self.board[self.from_col][smaller + i] != ' ':
                            return False

                elif self.from_row == self.to_row:
                    smaller, greater = self.max_out_of_two(self.from_col, self.to_col)
                    # Go trough all but the latest as this one could be a figure
                    for i in range(1, ord(greater) - ord(smaller)):
                        if self.board[chr(ord(smaller) + i)][self.from_row] != ' ':
                            return False

        elif figure in ['k', 'K']: # King
            # The king is only allowed to do one step.
            # So the differences from new to old columns can only
            # be 1 or 0. Otherwise the turn is invalid.
            print('Figure is k/K')
            col_difference = abs(ord(self.to_col) - ord(self.from_col))
            row_difference = abs(self.to_row - self.from_row)
            if col_difference > 1 or row_difference > 1:
                return False

        # The unique one is p/P because it has unique
        # patterns for each team i.e. going downwards/upwards
        elif figure in ['p', 'P']: # White Pawn
            # TODO: Validate white team pawn
            print('Figure is p/P')
            start_row = 1 if figure == 'p' else 6 # Default start row
            multiplier = 1 if figure == 'p' else (-1) # Going up or down

            col_difference = abs(ord(self.to_col) - ord(self.from_col))
            row_difference = self.to_row - self.from_row

            # Move is sideways
            if col_difference > 0:
                if col_difference > 1: # too far
                    return False
                # Using multiplier as white team goes up (1) and black team goes down (-1)
                if multiplier * row_difference != 1: # too far off
                    return False
                
                # Then the move is one step diagonal (only allowed if enemy is there)
                if self.board[self.to_col][self.to_row] == ' ':
                    return False
            
            # Otherwise its just on the row
            else:
                # If going more than one step
                if multiplier * row_difference > 1:
                    if multiplier * row_difference > 2: # too far
                        return False
                    elif self.from_row != start_row: # two steps only from start
                        return False
                # Backwards is not allowed
                elif multiplier * row_difference < 0: 
                    return False

        return True

    def check_mate(self):
        """
        Checks whether there is a checkmate.
        """
        # TODO: Check for checkmate
        return False

    def stale_mate(self):
        """
        Checks whether there is a stalemate
        """
        # TODO: Check for stalemate
        return False

    def max_out_of_two(self, first, second):
        """
        A helper function which returns two ordered elements as a tuple.
        """
        if first < second:
            return first, second
        return second, first
