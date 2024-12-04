"""Direction constant enums from a topleft zero perspective"""

from enum import Enum


class Direction(Enum):
    pass


class StraightDirection(Direction):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class DiagonalDirection(Direction):
    UPRIGHT = (1, -1)
    DOWNRIGHT = (1, 1)
    DOWNLEFT = (-1, 1)
    UPLEFT = (-1, -1)


ALL_DIRECTIONS: list[Direction] = list(StraightDirection) + list(DiagonalDirection)
