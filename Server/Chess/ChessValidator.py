from copy import deepcopy

class ChessValidator():
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.columns = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        self.check_mate = False

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
            if self.verbose: print('validate_figure_from_active_team failed')
            return False

        # - If there is already a figure of the from team
        if not self.validate_from_same_team_or_enemy_king():
            if self.verbose: print('validate_from_same_team_or_enemy_king failed')
            return False

        # - Check whether this teams king is in check
        #   If so different rules apply
        if self.check_for_check():
            # If the king is in danger check if it can be saved
            # If the king can't be saved this team looses - Check mate
            if not self.validate_king_can_be_saved():
                # Return that this is a valid move but ChessBoard (caller) now checks the check_mate attribute  
                self.check_mate = True
                return True

        # If it can be saved set the current move, check again for check and 
        # if it is still check this move won't save the king. Hence this move is invalid
        error = self.validate_figure_type_in_range()
        if error:
            if self.verbose: print(f'Figure is not allowed to go there: {error}')
            return False

        # If there is no error apply the current move to self.board and check_for_check.
        # If is returns true its invalid
        self.make_move()
        if self.check_for_check():
            self.make_move(undo=True) # Needs to be here as the make move alters the board reference
            return False
        self.make_move(undo=True)
        # If the move won't get the active team in a check its alright
        if self.verbose: print("Validator -> Valid move")
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

    def check_for_check(self):
        """
        Checks whether the active player is currently in check.
        This would mean the moves he can do aren't the same as if the king
        wouldn't be in danger.
        """
        # Get the position of the king (use default position first)
        active_king = 'K' if self.active_player else 'k'
        king_col = 'e'
        king_row = 7 if self.active_player else 1
        if self.board[king_col][king_row] != active_king:
            for col in self.columns:
                for row in range(8):
                    if self.board[col][row] == active_king:
                        king_col = col
                        king_row = row
        
        # Then check all positions from where the King could be attacked whether he is in danger
        # Set attackers and create an empty list to save them
        row_col_attacker = ['q', 'r'] if self.active_player else ['Q', 'R']
        diagonal_attacker = ['q', 'b'] if self.active_player else ['Q', 'B']
        knight_attacker = 'n' if self.active_player else 'N'
        pawn_attacker = 'p' if self.active_player else 'P'
        attackers = [] # A list of [col, row] with attackers

        # This loop is trying to do as much as possible without a lot of code repition.
        # It is checking all rows and columns and diagonal parts from the perspective of the king.
        # So its first going steps right, and down, ..., then diagonally top right, ... and always checks
        # whether there is an attacker (one of the attackers) at that spot. If there is any other
        # figure it continues with the next row, column, diagonal etc..
        # The loop is built up like this:
        # attacker - The enemy which could attack the king from that position
        # direction - Right=1, Left=-1, Top=-1, Up=1 (going up is position while down means subtracting)
        # col_multiplier - If iterating trough a column this is 1, if not 0
        # row_multiplier - If iterating trough a row this is 1, if not 0
        for attacker, direction, col_multiplier, row_multiplier in ([
            (row_col_attacker, 1, 1, 0), # right straight
            (row_col_attacker, 1, 0, 1), # down straight
            (row_col_attacker, -1, 1, 0), # left straight
            (row_col_attacker, -1, 0, 1), # up straight
            (diagonal_attacker, 1, 1, 1), # right up
            (diagonal_attacker, 1, 1, -1), # right down
            (diagonal_attacker, 1, -1, 1), # left up
            (diagonal_attacker, -1, 1, 1), # left down
            ]):
            # Initializing the variables
            i = direction # Starting position
            new_col = king_col
            new_row = king_row
            inside_board = True
            # As long as we are inside the board (checks happen directly after updating new values)
            while inside_board: 
                # New columns are the kings column + (either 0 if not moving OR iteratorcount)
                new_col = chr(ord(king_col) + (i * col_multiplier))
                new_row = king_row + (i * row_multiplier)
                if (new_col > 'h' or new_col < 'a' or
                    new_row > 7 or new_row < 0):
                   inside_board = False
                   continue
            
                # Now check first whether its an enemy
                if self.board[new_col][new_row] in attacker:
                    # This is where the attacker is saved
                    attackers.append([new_col, new_row])
                    inside_board = False
                    continue

                # If there is anything else in between the rest isn't important
                if self.board[new_col][new_row] != ' ':
                    inside_board = False
                    continue

                i += direction

        # - Knight
        for i in range(8):
            knight_indices = [-2, -1, 1, 2, 2, 1, -1, -2]
            try:
                if self.board[
                    chr(ord(king_col) + knight_indices[i])][
                    king_row + knight_indices[(i+2)%8]] == knight_attacker:
                        attacker.append(
                            [ord(king_col) + knight_indices[i], king_row + knight_indices[(i+2)%8]]
                        )
                        print('Attacked by a knight')
            except IndexError: # Ignore because its outide of the board
                pass

        # - Pawn
        pawn_col = chr(ord(king_col) - 1) if active_king else king_col + 1
        try: # Right side
            if self.board[pawn_col][king_row + 1] == pawn_attacker:
                    attacker.append([pawn_col, king_row + 1])
                    print('Attacked by a knight')
        except IndexError: # Ignore because its outide of the board
            pass

        try: # Left side
            if self.board[pawn_col][king_row - 1] == pawn_attacker:
                    attacker.append([pawn_col, king_row - 1])
                    print('Attacked by a knight')
        except IndexError: # Ignore because its outide of the board
            pass

        # If there are any attacker then its check
        if len(attackers) > 0:
            # If there are attacker then save them for the validate_king_can_be_saved function
            self.attackers = attackers
            return True
        return False

    def validate_king_can_be_saved(self):
        """
        Checks whether the king can be saved. It returns False if it will die.
        Or True if there is still some hope.
        It checks for three main possibilities:
        1. Check whether the king is able to make a move and get out of check
        If there are more than 1 attacker and this can't happen he is dead...
            If there is only one attacker 
            2. Check for any own figure which can put itself inside the attack line
            3. Check for any own figure which can attack the one attacker
        """
        # First check whether to king can reposition itself and check for check again
        # TODO: Check king repositioning
        # Get the position of the king (use default position first)
        active_king, enemy_king = ('K', 'k') if self.active_player else ('k', 'K')
        king_col = 'e'
        king_row = 7 if self.active_player else 1
        if self.board[king_col][king_row] != active_king:
            for col in self.columns:
                for row in range(8):
                    if self.board[col][row] == active_king:
                        king_col = col
                        king_row = row

        # And the limits for spotting an enemy
        lower_limit, upper_limit = ('a', 'z') if self.active_player else ('A', 'Z')
        for col_iterator in [-1, 0, 1]:
            for row_iterator in [-1, 0, 1]:
                # So we can look on each position next to the king.
                # If there is an enemy or an empty spot try to move the king and check for check again
                try:
                    new_spot = self.board[
                        chr(ord(king_col) + col_iterator)][
                            king_row + row_iterator]
                    
                    if ((new_spot >= lower_limit and new_spot <= upper_limit) or 
                        new_spot == ' '):
                            # Replace the King
                            # Careful to save everything which will be changed
                            # DO
                            tmp_from_col = self.from_col
                            tmp_from_row = self.from_row
                            tmp_to_col = self.to_col
                            tmp_to_row = self.to_row

                            self.from_col = king_col
                            self.from_row = king_row
                            self.to_col = chr(ord(king_col) + col_iterator) 
                            self.to_row = king_row + col_iterator 

                            # DO
                            self.make_move()

                            result = True
                            # Now check first whether the enemy king is in range 
                            for inner_col_iterator in [-1, 0, 1]:
                                for inner_row_iterator in [-1, 0, 1]:
                                    try:
                                        if self.board[
                                            chr(ord(self.from_col) + inner_col_iterator)][
                                                self.from_row + inner_row_iterator] == enemy_king:
                                                result = False
                                                break
                                    except IndexError:
                                        pass

                            # Only if the move was valid go into further checking
                            if result:
                                # DO
                                attackers_copy = deepcopy(self.attackers)

                                # Then check for the new check and if it returns False
                                # the king can be saved
                                result = not self.check_for_check()

                                # UNDO
                                self.attackers = attackers_copy


                            # UNDO
                            self.make_move(undo=True)

                            # UNDO
                            self.from_col = tmp_from_col
                            self.from_row = tmp_from_row 
                            self.to_col = tmp_to_col 
                            self.to_row = tmp_to_row 
                            
                            # If the result was True we found a way to save the king
                            if result:
                                return True

                # If we except an IndexError ignore
                except IndexError:
                    pass

        # If that didn't work check whether there is more than one attacker
        if len(self.attackers) == 1:
            # TODO: 2nd and 3rd Test
            # Then try to move any figure inside the attack line

            # If that didn't work try to attack the attacker
            pass

        # If all checks fail... Check mate
        return False
    
    def validate_figure_type_in_range(self):
        """
        Validates whether the figure is allowed to go to that position.
        E.g. a King is only allowed to go one step away from his position.
        The function returns either a string indicating why the figure
        could not go there or None.
        """
        figure = self.board[self.from_col][self.from_row]
        # There are two types of figures unique ones and generic ones
        # First the generic ones are validated
        # These are r/R, b/B, n/N, q/Q, k/K

        if figure in ['r', 'R']: # Rook
            # Rook is allowed to go along the column and rows
            # So either the columns or the rows must be the same
            if (self.from_col != self.to_col and
                self.from_row != self.to_row):
                return 'Rook - only allowed to go straight'
            
            # Then there can't be something in between
            # So go trough the whole row and check whether there is something in between
            if self.from_col == self.to_col:
                smaller, greater = self.max_out_of_two(self.from_row, self.to_row)
                # Go trough all but the latest as this one could be a figure
                for i in range(1, greater - smaller):
                    if self.board[self.from_col][smaller + i] != ' ':
                        return 'Rook - Someone in between (column)'

            # Otherwise go trough the whole column
            elif self.from_row == self.to_row:
                smaller, greater = self.max_out_of_two(self.from_col, self.to_col)
                # Go trough all but the latest as this one could be a figure
                for i in range(1, ord(greater) - ord(smaller)):
                    if self.board[chr(ord(smaller) + i)][self.from_row] != ' ':
                        return 'Rook - Someone in between (row)'

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
                return 'Knight - Not going two steps then sideways'

        elif figure in ['b', 'B']: # Bishop
            # The difference between the columns and the rows has to be the same
            # because the Bishop is allowed to walk in diagonal lines
            if (abs(ord(self.from_col) - ord(self.to_col)) !=
                abs(self.from_row - self.to_row)):
                return 'Bishop - Only allowed to go diagonal'

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
                    return 'Bishop - Someone in between'

                # Then update the indices
                if row_difference > 0: row_difference -= 1
                else: row_difference += 1
                if col_difference > 0: col_difference -= 1
                else: col_difference += 1

        elif figure in ['q', 'Q']: # Queen
            # The queen is a combination of the rook and the bishop so everything is just
            # split up into two geater ifs and then the source of the rook and the bishop
            # is copied down there
            # If the columns and destinations aren't the same its a bishop move (or invalid)
            if (self.from_col != self.to_col and
                self.from_row != self.to_row):
                # Check whether it is actually a bishop move - if not mark as invalid
                if (abs(ord(self.from_col) - ord(self.to_col)) !=
                    abs(self.from_row - self.to_row)):
                    return 'Queen - Only allowed to go straight or diagonal'

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
                        return 'Queen - Someone in between (diagonal)'

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
                            return 'Queen - Someone in between (column)'

                elif self.from_row == self.to_row:
                    smaller, greater = self.max_out_of_two(self.from_col, self.to_col)
                    # Go trough all but the latest as this one could be a figure
                    for i in range(1, ord(greater) - ord(smaller)):
                        if self.board[chr(ord(smaller) + i)][self.from_row] != ' ':
                            return 'Queen - Someone in between (row)'

        elif figure in ['k', 'K']: # King
            # The king is only allowed to do one step.
            # So the differences from new to old columns can only
            # be 1 or 0. Otherwise the turn is invalid.
            col_difference = abs(ord(self.to_col) - ord(self.from_col))
            row_difference = abs(self.to_row - self.from_row)
            if col_difference > 1 or row_difference > 1:
                return 'King - Only allowed to go one step'
            
            enemy_king = 'k' if figure == 'K' else 'K'
            # If the king is stepping towards the enemy king the move is invalid
            for col_iterator in [-1, 0, 1]:
                for row_iterator in [-1, 0, 1]:
                    # We can look all places as we are just looking for the enemy king
                    try:
                        if self.board[
                            chr(ord(self.to_col) + col_iterator)][
                                self.to_row + row_iterator] == enemy_king:
                                return 'King - Next to new position is the enemy king'
                    # If we except an IndexError ignore as we would then ask
                    # for a spot outside of the board
                    except IndexError:
                        pass

        # The unique one is p/P because it has unique
        # patterns for each team i.e. going downwards/upwards
        elif figure in ['p', 'P']: # White Pawn
            start_row = 1 if figure == 'p' else 6 # Default start row
            multiplier = 1 if figure == 'p' else (-1) # Going up or down

            col_difference = abs(ord(self.to_col) - ord(self.from_col))
            row_difference = self.to_row - self.from_row

            # Move is sideways
            if col_difference > 0:
                if col_difference > 1: # too far
                    return 'Pawn - Going too far sideways'
                # Using multiplier as white team goes up (1) and black team goes down (-1)
                if multiplier * row_difference != 1: # too far off
                    return 'Pawn - Only allowed to go one step diagonal'
                
                # Then the move is one step diagonal (only allowed if enemy is there)
                if self.board[self.to_col][self.to_row] == ' ':
                    return 'Pawn - Only allowed to step diagonal if there is an enemy'
            
            # Otherwise its just on the row
            else:
                # If going more than one step
                if multiplier * row_difference > 1:
                    if multiplier * row_difference > 2: # too far
                        return 'Pawn - Stepping too far'
                    elif self.from_row != start_row: # two steps only from start
                        return 'Pawn - Two steps are only allowed from the start row'
                # Backwards is not allowed
                elif multiplier * row_difference < 0: 
                    return 'Pawn - Not allowed to step backwards'
                # Attacking an enemy in front of the pawn is not allowed
                elif self.board[self.to_col][self.to_row] != ' ':
                    return 'Pawn - Not allowed to attack enemy in front'

        return None

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

    def make_move(self, undo=False):
        """
        A helper function for making a move which updates self.board.
        It uses the self.to_col etc. attributes to make the move.
        If undo is True it uses the self.to_col as the source and the from as the destination
        to undo a move.
        """
        if not undo:
            # Save the old destination figure for the undo operation
            self.old_destination_figure = self.board[self.to_col][self.to_row]
            figure = self.board[self.from_col][self.from_row]
            self.board[self.from_col][self.from_row] = ' '
            self.board[self.to_col][self.to_row] = figure

        else:
            try:
                figure = self.board[self.to_col][self.to_row]
                self.board[self.to_col][self.to_row] = self.old_destination_figure
                self.board[self.from_col][self.from_row] = figure
            except:
                print('Error undoing a move inside the ChessValidator')
            

