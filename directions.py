"""Direction constant enums from a topleft zero perspective"""

from enum import Enum
from functools import total_ordering
from typing import Self

type Position = tuple[int, int]
type Position3D = tuple[int, int, int]


@total_ordering
class Direction(Enum):
    pass

    def __lt__(self, other):
        return self.value < other.value


class StraightDirection(Direction):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def from_char(cls, char: chr) -> Self:
        match char:
            case "^":
                return cls.UP
            case "v":
                return cls.DOWN
            case "<":
                return cls.LEFT
            case ">":
                return cls.RIGHT
            case _:
                raise ValueError(f"Invalid direction symbol: {char}")


class DiagonalDirection(Direction):
    UPRIGHT = (1, -1)
    DOWNRIGHT = (1, 1)
    DOWNLEFT = (-1, 1)
    UPLEFT = (-1, -1)


ALL_DIRECTIONS: list[Direction] = list(StraightDirection) + list(DiagonalDirection)

TURN_LEFT = {
    StraightDirection.UP: StraightDirection.LEFT,
    StraightDirection.RIGHT: StraightDirection.UP,
    StraightDirection.DOWN: StraightDirection.RIGHT,
    StraightDirection.LEFT: StraightDirection.DOWN,
}

TURN_RIGHT = {
    StraightDirection.UP: StraightDirection.RIGHT,
    StraightDirection.RIGHT: StraightDirection.DOWN,
    StraightDirection.DOWN: StraightDirection.LEFT,
    StraightDirection.LEFT: StraightDirection.UP,
}

REVERSE_DIRECTION = {
    StraightDirection.UP: StraightDirection.DOWN,
    StraightDirection.DOWN: StraightDirection.UP,
    StraightDirection.LEFT: StraightDirection.RIGHT,
    StraightDirection.RIGHT: StraightDirection.LEFT,
}


def translate_position(pos: Position, direction: Direction, steps: int = 1) -> Position:
    return (
        pos[0] + steps * direction.value[0],
        pos[1] + steps * direction.value[1],
    )


class Direction3D(Enum):
    UP = (0, -1, 0)
    DOWN = (0, 1, 0)
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    ABOVE = (0, 0, 1)
    BELOW = (0, 0, -1)


def translate_position_3d(pos: Position3D, direction: Direction3D, steps: int = 1) -> Position3D:
    return (
        pos[0] + steps * direction.value[0],
        pos[1] + steps * direction.value[1],
        pos[2] + steps * direction.value[2],
    )
