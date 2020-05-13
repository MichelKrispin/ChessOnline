#!/usr/bin/env python3

import socket
import sys
import signal
import argparse

from Chess import ChessGame

HOST, PORT = '', 30123

def start_server(verbose=True):
    """
    Running a server on HOST, PORT.
    If verbose is on all information will be printed.
    Otherwise only the bare minimum is printed.
    """
    print(f'Starting the server on port {PORT}... (Press Ctrl-C to quit)')

    # Create the socket and set options
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Try to bind the socket and if the port is already in use
    # the function will throw an OSError. If so quit the program
    try:
        listen_socket.bind((HOST, PORT))
    except OSError:
        print(
            f'The port {PORT} is already in use.\n'
             'Maybe the server is already running?'
        )
        return 1
        
    # If binding was successfull listen to input
    listen_socket.listen(1)
    if verbose:
        print(f'Listening on port {PORT} ...')
    
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
        if verbose:
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
        if verbose:
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


def exit_server(signum, frame):
    """
    Tell how Ctrl-C should be handled.
    Meaning show a nicer response than the default handling does.
    """
    # Reset the signal handler
    signal.signal(signal.SIGINT, original_sigint)
    print('\nQuitting the server...')
    sys.exit(1)


def parse_arguments():
    """
    Parse the command line arguments if there are any.
    """
    parser = argparse.ArgumentParser(description='Start a chess game server.')
    # Add the port argument
    parser.add_argument(
            '-p', '--port',
            dest='port',
            type=int,
            help='Set a custom port'
    )
    args = parser.parse_args()
    # If port is custom change the global variable
    if args.port:
        # Smaller than 1024 means common protocol port
        # which is normally blocked and too great doesn't exist
        if args.port < 1024 or args.port > 65535:
            print('Specified port is invalid. Using default.')
            return
        globals()['PORT'] = args.port


# If this file is started start the server
# -> Don't start it if its imported
if __name__ == '__main__':
    # Set the interrupt signal to a custom handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_server)

    # Parse the command arguments
    parse_arguments()

    # Start the serve
    result = start_server()
    sys.exit(result)

