#!/usr/bin/env python3

import socket
import sys

# HOST, PORT = '46.91.230.197', 30123
HOST, PORT = '', 30123

old_data = ''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("It seems like the server isn't running right now.")
        sys.exit(1)

    s.sendall(b'Hello World')
    while True:
        data = s.recv(1024)
        if old_data != data:
            old_data = data
            if data != b'':
                print('Received', repr(data))
            else:
                print('The connection was closed')
                sys.exit(0)
            # Only get input if active player
            if b'+' in data:
                send_data = input('>> ')
                s.sendall(send_data.encode())

