from enum import Enum


class ChessMove(Enum):
    """
    Simple enum to determine the result of a move.
    """
    INVALID_MOVE = -1
    PASSED = 0
    CHECK_MATE = 1
    STALE_MATE = 2
