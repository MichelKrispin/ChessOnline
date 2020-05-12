#!/usr/bin/env python3

import socket
import sys

# HOST, PORT = '46.91.230.197', 30123
# HOST, PORT = '', 30123
HOST, PORT = '127.0.0.1', 30123

def connect_to_server(verbose=True):
    if verbose: print(f'Connecting to {HOST}:{PORT}')
    old_data = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError as e:
            print("It seems like the server isn't running right now.")
            if verbose: print(e) 
            sys.exit(1)

        address, port = s.getsockname()
        s.sendall(b'Hello from ' + address.encode() + b':' + str(port).encode())
        while True:
            data = s.recv(1024)
            if old_data != data:
                old_data = data
                if data != b'':
                    # print(f"Received: {data.decode('utf-8')}")
                    print(render_received_byte_text(data))
                    # render_received_byte_text(data)
                    pass
                else:
                    print('The connection was closed')
                    sys.exit(0)
                # Only get input if active player
                if b'+' in data:
                    send_data = input('>> ')
                    s.sendall(send_data.encode())

def render_received_byte_text(byte_data):
    """
    Renders the byte data text to a nicely printable text and returns it.
    The default board would be outputted as
      _______________
    8|R N B Q K B N R|
    7|P P P P P P P P|
    6|               |
    5|               |
    4|               |
    3|               |
    2|p p p p p p p p|
    1|r n b q k b n r|
     |_______________|
      a b c d e f g h
    """
    # The string has to start with an active or not active indicator
    if chr(byte_data[0]) not in ['+', '-']:
        return byte_data.decode('utf-8')

    # If the byte_data only consist of a + don't show it
    if len(byte_data) < 2:
        return ''

    # If the first two elements are ++ its an error message so print it
    if chr(byte_data[0]) == '+' and chr(byte_data[1]) == '+':
        return byte_data[2:].decode('utf-8')

    result = '  _______________\n8|'
    row_counter = 8
    for char in byte_data:
        c = chr(char) # Converts the ASCII int to a string
        if c in ['+', '-']:
            continue
        if c == '.':
            result += '|\n'
            if row_counter > 1:
                row_counter -= 1
                result += str(row_counter) + '|'
        elif c == ',':
            result += ' '
        else:
            result += c

    result += ' |_______________|\n'
    result += '  a b c d e f g h'
    return result

if __name__ == '__main__':
    connect_to_server()
