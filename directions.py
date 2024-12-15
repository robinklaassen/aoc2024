"""Direction constant enums from a topleft zero perspective"""

from enum import Enum
from typing import Self


class Direction(Enum):
    pass


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


def translate_position(pos: tuple[int, int], direction: Direction, steps: int = 1) -> tuple[int, int]:
    return (
        pos[0] + steps * direction.value[0],
        pos[1] + steps * direction.value[1],
    )
