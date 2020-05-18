from ChessBoard import ChessBoard, ChessMove
import sys

class ChessGame():
    """
    The class which handles all of the chess logic and
    sends the computed data then back to the client.
    """
    player = { 'white': 0, 'black': 1 } # Helper dictionary
    player_string = { 0: 'white', 1: 'black' }

    def __init__(self, white_player_connection, black_player_connection, verbose=True):
        """
        Needs the connections for both players so it can send data to them.
        """
        # Initialize all variables
        self.player_connections = []
        self.player_connections.append(white_player_connection)
        self.player_connections.append(black_player_connection)

        self.active_player = self.player['white']
        self.inactive_player = self.player['black']

        # Only for showing more information
        self.verbose = verbose

        # Create a chess board
        self.chess_board = ChessBoard()

        # Start the game loop
        self.game_loop()

    def game_loop(self):
        """
        The game loop.
        The data send to the clients is prepended by a + or - to indicate
        the active player. After that the board data will be send.
        All in all it looks like
        +R,N,B,Q,K,B,N,R.P,P,P,P,P,P,P. and so on
        The dot indicates a line break.
        """
        # Initialize by sending the board to active in inactive player
        rendered_board = self.chess_board.render_to_byte_text()
        active_response = b'+' + rendered_board
        self.player_connections[self.active_player].sendall(active_response)

        inactive_response = b'-' + rendered_board
        self.player_connections[self.inactive_player].sendall(inactive_response)

        while True:
            # Check for a valid input for as long as it is needed
            unique_count = 0
            while True:
                request_data = self.player_connections[self.active_player].recv(1024)

                # Check if the input is valid (a1 to h8 etc.)
                if self.validate_request_data(request_data):
                    # If the input is valid make the move
                    move = self.chess_board.make_move(
                        request_data[:2].decode('utf-8'),
                        request_data[-2:].decode('utf-8'),
                        self.active_player
                    )

                    # If the move was invalid ask again for input
                    if move == ChessMove.INVALID_MOVE:
                        if self.verbose: print("Validator failed")
                        response = (b'++Invalid move ' + str(unique_count).encode())
                        self.player_connections[self.active_player].sendall(response)

                    # Otherwise go more into detail of what happened and toggle the player
                    else:
                        if move == ChessMove.CHECK_MATE:
                            if self.verbose: print("Check mate")
                        elif move == ChessMove.STALE_MATE:
                            if self.verbose: print("Stale mate")
                        else:
                            if self.verbose: print("Valid move")
                        break

                # If the input was invalid ask for input again and notify player
                else:
                    if self.verbose: print(f'{request_data} was invalid input')
                    response = (
                            b'++Invalid input (except row col to row col e.g. a1 to h8) '
                        + str(unique_count).encode())
                    try:
                        self.player_connections[self.active_player].sendall(response)
                    except BrokenPipeError:
                        print('At least one client closed the connection')
                        sys.exit(1)
                unique_count += 1
            if self.verbose: print(f"Requested: {request_data.decode('utf-8')}")

            # Send data to active player
            rendered_board = self.chess_board.render_to_byte_text()
            active_response = b'-' + rendered_board
            self.player_connections[self.active_player].sendall(active_response)

            # Send data to opponent player
            inactive_response = b'+' + rendered_board
            self.player_connections[self.inactive_player].sendall(inactive_response)

            self.switch_player()

    def validate_request_data(self, data):
        """
        Check whether the data is a string which start with
        two characters such as a1 and ends with them.
        Allowed are characters from a-h and numbers from 1-8
        In ASCII the valid range is
         a    1  -   h   8
        (97)(49) - (104)(56)
        """
        if len(data) < 4:
            return False

        # If first character isn't between a and h
        if data[0] < ord('a') or data[0] > ord('h'):
            return False
        # If second character isn't between 1 and 8
        if data[1] < ord('1') or data[1] > ord('8'):
            return False

        if data[-2] < ord('a') or data[-2] > ord('h'):
            return False
        if data[-1] < ord('1') or data[-1] > ord('8'):
            return False
        
        return True # If passed it is valid


    def switch_player(self):
        """ Switch to one or the other player after a round. """
        if self.active_player:
            self.active_player = self.player['white']
            self.inactive_player = self.player['black']
        else:
            self.active_player = self.player['black']
            self.inactive_player = self.player['white']

