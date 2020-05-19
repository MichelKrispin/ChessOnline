#!/usr/bin/env python3

import argparse

from Server.Testing import *
from Server.Testing.Tests import run_all_tests

def parse_arguments():
    """
    Parse the command line arguments if there are any.
    """
    parser = argparse.ArgumentParser(description='Test all existing test cases.')
    # Add the shorten argument
    parser.add_argument(
            'shorten',
            nargs='?',
            help='Shorten the output to print only the details of failed tests.',
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    run_all_tests(True if args.shorten else False)