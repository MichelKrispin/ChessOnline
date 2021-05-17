# Chess Online on the command line

A side project which implements a chess server which has a simple (and incomplete) backend. The chess backend is not complete.
The front end is a very simple client which connects to the running server instance and prints the chess board.

There should be no external dependencies to run the server, client or the tests.
Python 3 was used and it was only testes on Linux.

## Run the server
```
./run_server.py
```

The client will wait for two incoming connections and then handle the input.


## Run the client
```
./run_client.py
```

A client is only connecting to the server and responds to the messages sent by the server.
A move is made by typing `<from> <to>` where each value is the column and the row from a to h and 1 to 8.
So possible moves are:

1st player: `a2 a3`

2nd player: `a7 a6`


## Run the tests

```
./run_tests.py
```

The tests are fully written in plain python and make use of the python reflection system.
They search trough the `Server/Testing/` folder and check every `testing_<test_name>.py` for a function starting with `testing_`.
It then goes over a newly generated test board and tries to make some moves on that board and checks whether they pass or fail the board and if this behaviour was expected.

A test case creation looks like this:
1. Copy everything out of the TEST CASE TEMPLATE comment (the TEST CASE TEMPLATE comment itself isn't necessary...)
2. Create a new file inside of this folder and name it to something meaningful. The function should have the same name.
   !!! It has to start with testing_ . Otherwise it won't be noticed as a test.
   (The name will be used in the ouput)
3. Customize the test (you can look for reference in the other test files)
   3.1 Normally the board is adjusted for a specific move
   3.2 Then the to and from draws are customized for this test
   3.3 The description should be meaningful. If the test fails this will be helpful.
   3.4 The team is either 0 (white) or 1 (black)
   3.5 If the test should fail (e.g. the move should'nt work) its Expect.False and vice versa
   3.6 You can create custom helper functions inside of the files just don't let them start with testing_
4. Run the file and see whether the test has passed

Notes:
- The testing suppresses all printing to console of the actual functions

```python
# TEST CASE TEMPLATE
from .Helper import *
from ..Chess.ChessValidator import ChessValidator

def testing_chess_validator_template():
    result = []
    chess_validator = ChessValidator()

    # ------

    board = generate_board_from_string("""
8|R N B Q K B N R|
7|P P P P P P P P|
6|               |
5|               |
4|               |
3|               |
2|p p p p p p p p|
1|r n b q k b n r|
""")
    
    for from_string, to_string, description, active_player, expect in (
            ['a1', 'a1', 'Same position and same team', 0, Expect.FALSE],
            ['a1', 'a2', 'Same team', 0, Expect.FALSE],
            ['a1', 'a3', 'Different team ', 1, Expect.FALSE],
            ['a7', 'a9', 'Row out of board', 1, Expect.FALSE],
            ['h1', 'g1', 'Col out of board', 0, Expect.FALSE],
            ):
        result.append(run_individiual_chess_validate(line_number(),chess_validator.validate_move,
            board, from_string, to_string, active_player, description, expect))

    # ------

    result.append('> Finished')
    return result
```
