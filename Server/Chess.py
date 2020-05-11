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

        # Start the game loop
        self.game_loop()

    def game_loop(self):
        """
        The game loop.
        """
        # Initialize by sending active player to the active player
        self.player_connections[self.active_player].send(b'+')

        while True:
            unique_count = 0
            valid_request = False
            while not valid_request:
                request_data = self.player_connections[self.active_player].recv(1024)
                if self.validate_request_data(request_data):
                    valid_request = True
                else:
                    if self.verbose: print(f'{request_data} was invalid input')
                    response = (b'Invalid input + Input row column to row column (e.g. a1 to h8)'
                        + str(unique_count).encode())
                    self.player_connections[self.active_player].sendall(response)
                unique_count += 1
            if self.verbose: print(f"Requested: {request_data.decode('utf-8')}")

            # Send data to active player
            active_response = b'-'
            self.player_connections[self.active_player].sendall(active_response)

            # Send data to opponent player
            inactive_response = b'+'
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
        if data[0] < 96 or data[0] > 105:
            return False
        # If second character isn't between 1 and 8
        if data[1] < 49 or data[1] > 57:
            return False

        if data[-2] < 96 or data[-2] > 105:
            return False
        if data[-1] < 49 or data[-1] > 57:
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

