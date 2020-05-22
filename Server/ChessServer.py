import signal
import socket
import sys

from .Chess.Chess import ChessGame
from .Chess.ChessMove import ChessMove


class ChessServer():
    def __init__(self, host='127.0.0.1', port=30123, verbose=True):
        """ Initializes the chess server. """
        self.host = host
        self.port = port
        self.verbose = verbose

        self.player_connections = []

        self.initialize()

    def initialize(self):
        """
        Sets everything up neede for the server.
        This includes a custom signal handler.
        """
        # Set the interrupt signal to a custom handler first
        self.original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.clean_exit)

    def clean_exit(self):
        """
        Tell how Ctrl-C should be handled.
        Meaning show a nicer response than the default handling does.
        """
        # Reset the signal handler
        signal.signal(signal.SIGINT, self.original_sigint)
        print('\nQuitting the server...')
        sys.exit(1)

    def start_server(self):
        """
        Running a server on host and port.
        The server sends the clients data which is prepended by a + or - to indicate
        the active player. After that the board data will be send.
        All in all it looks like
        +R,N,B,Q,K,B,N,R.P,P,P,P,P,P,P. and so on
        The dot indicates a line break.
        """
        print(f'Starting the server on port {self.port}... (Press Ctrl-C to quit)')

        # Create the socket and set options
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Try to bind the socket and if the port is already in use
        # the function will throw an OSError. If so quit the program
        try:
            listen_socket.bind((self.host, self.port))
        except OSError:
            print(
                f'The port {self.port} is already in use.\n'
                'Maybe the server is already running?'
            )
            return 1
            
        # If binding was successfull listen to input
        listen_socket.listen(1)
        if self.verbose:
            print(f'Listening on port {self.port} ...')
        
        # For multiple connections
        client_addresses = []
        while True:
            # Listen to the first connection
            client_connection, client_address = listen_socket.accept()
            self.player_connections.append(client_connection)
            client_addresses.append(client_address)

            # Get the first data and print it
            request_data = client_connection.recv(1024)
            if self.verbose: print(request_data.decode('utf-8'))

            # The first response for the first client to connect
            response = b"You are the first one to connect!"
            # Send the first response
            client_connection.sendall(response)

            # 2nd connection ----------------------
            # Then wait for second connection
            client_connection, client_address = listen_socket.accept()
            self.player_connections.append(client_connection)
            client_addresses.append(client_address)
            response = b"You are the second one to connect!"
            # Send the first response
            client_connection.sendall(response)

            # Get the second data and print it
            request_data = client_connection.recv(1024)
            if self.verbose: print(request_data.decode('utf-8'))

            # The first response for the first client to connect
            self.start_game()

            # Then close all connections
            for connection in self.player_connections:
                connection.close()

            # Then return a success
            return 0

    def start_game(self):
        """
        Starts the chess game with its loop and handles input and output to clients.
        Depends on established client connections.
        """
        # Create a chess game
        chess_game = ChessGame()

        # Send both clients initial information
        current_board = chess_game.board_as_bytes
        self.player_connections[chess_game.active_player]\
            .sendall(b'+' + current_board)
        self.player_connections[chess_game.inactive_player]\
            .sendall(b'-' + current_board)

        # Then play until check_mate
        while True:
            uniqueness_count = 0 # Needed if sending same data over and over again

            # Until there is some valid input ask for it
            while True:
                try:
                    request_data = self.player_connections[chess_game.active_player].recv(1024)
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    print('At least one client closed the connection')
                    sys.exit(1)

                # Check if the input is valid (a1 to h8 etc.)
                if self.validate_request_data(request_data):
                    # If the input is valid make the move
                    request = request_data.decode('utf-8')
                    move = chess_game.make_move(
                        request[0], int(request[1]), request[-2], int(request[-1]))

                    # If the move was invalid ask again for input
                    if move == ChessMove.INVALID_MOVE:
                        if self.verbose: print(f"Invalid move {request[0]}{request[1]} to {request[-2]}{request[-1]}")
                        self.player_connections[chess_game.active_player]\
                            .sendall(b'++Invalid move ' + str(uniqueness_count).encode())
                        self.player_connections[chess_game.inactive_player]\
                            .sendall(b'.')

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
                        + str(uniqueness_count).encode())
                    try:
                        self.player_connections[chess_game.active_player].sendall(response)
                        self.player_connections[chess_game.inactive_player].sendall(b'.')
                    except BrokenPipeError:
                        print('At least one client closed the connection')
                        sys.exit(1)
                uniqueness_count += 1

            # After valid input and a valid move send both clients a response
            if self.verbose: print(f"Requested: {request_data.decode('utf-8')}")

            # First send information to active player and then the data
            self.player_connections[chess_game.active_player]\
                .sendall(b'Its your turn.')
            self.player_connections[chess_game.active_player]\
                .sendall(b'+' + chess_game.board_as_bytes)

            # First send information to opponent player and then the data
            self.player_connections[chess_game.inactive_player]\
                .sendall(b'-' + chess_game.board_as_bytes)
            self.player_connections[chess_game.inactive_player]\
                .sendall(b'Its your opponents turn.')
            

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
