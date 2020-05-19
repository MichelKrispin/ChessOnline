#!/usr/bin/env python3
#!/usr/bin/env python3

import argparse
import re
import sys

from Client.ChessClient import ChessClient

def parse_arguments():
    """
    Parse the command line arguments if there are any.
    """
    parser = argparse.ArgumentParser(description='Start a chess game server.')
    
    # Add the host argument
    parser.add_argument(
            '-ho', '--host',
            dest='host',
            type=str,
            default='127.0.0.1',
            help='Set a custom host'
    )

    # Add the port argument
    parser.add_argument(
            '-p', '--port',
            dest='port',
            type=int,
            default=30123,
            help='Set a custom port'
    )
    
    # Add the verbose argument
    parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            default=True,
            help='If set the server will print way more information'
    )

    args = parser.parse_args()
 
    # Check the host for a valid IP
    # TODO: A real IP address checking
    if (args.host != 'localhost' and 
        not re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', args.host)):
        print('The IP address does not match the IPv4 address pattern')
        return False, None, None, None

    # Smaller than 1024 means common protocol port
    # which is normally blocked and too great doesn't exist
    if args.port < 1024 or args.port > 65535:
        print('Specified port is invalid. Using default.')
        return False, None, None, None

    return True, args.host, args.port, args.verbose

if __name__ == '__main__':
    # Parse the command arguments
    valid, host, port, verbose = parse_arguments()
    if not valid:
        sys.exit(1)

    # Start the client
    client = ChessClient(host, port, verbose)
    result = client.connect()
    sys.exit(result)
