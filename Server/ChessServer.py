import socket
import signal
import sys

from .Chess.Chess import ChessGame

class ChessServer():
    def __init__(self, host='127.0.0.1', port=30123, verbose=True):
        self.host = host
        self.port = port
        self.verbose = verbose

    def start_server(self):
        """
        Running a server on host and port.
        If verbose is on all information will be printed.
        Otherwise only the bare minimum is printed.
        """
        # Set the interrupt signal to a custom handler first
        self.original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.clean_exit)

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
        client_connections = []
        client_addresses = []
        while True:
            # Listen to the first connection
            client_connection, client_address = listen_socket.accept()
            client_connections.append(client_connection)
            client_addresses.append(client_address)

            # Get the first data and print it
            request_data = client_connection.recv(1024)
            if self.verbose:
                print(request_data.decode('utf-8'))

            # The first response for the first client to connect
            response = b"You are the first one to connect!"
            # Send the first response
            client_connection.sendall(response)

            # 2nd connection ----------------------
            # Then wait for second connection
            client_connection, client_address = listen_socket.accept()
            client_connections.append(client_connection)
            client_addresses.append(client_address)
            response = b"You are the second one to connect!"
            # Send the first response
            client_connection.sendall(response)

            # Get the second data and print it
            request_data = client_connection.recv(1024)
            if self.verbose:
                print(request_data.decode('utf-8'))

            # The first response for the first client to connect
            """
            response = b"Established two connections!"
            for connection in client_connections:
                connection.sendall(response)
            """
            chess_game = ChessGame(client_connections[0], client_connections[1])

            # Then close all connections
            for connection in client_connections:
                connection.close()
            # And then delete all client_connections from the list
            client_connections = []

            # Then return a success
            return 0

    def clean_exit(self):
        """
        Tell how Ctrl-C should be handled.
        Meaning show a nicer response than the default handling does.
        """
        # Reset the signal handler
        signal.signal(signal.SIGINT, self.original_sigint)
        print('\nQuitting the server...')
        sys.exit(1)
