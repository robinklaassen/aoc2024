from collections import UserDict
from operator import itemgetter
from pathlib import Path
from typing import Self

from directions import Direction, StraightDirection
from utils import read_input


class Grid2D(UserDict[tuple[int, int], str]):
    """An Advent of Code favorite. Indexed by (x, y) from top left."""

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return cls({
            (i, j): lines[j][i]
            for i in range(len(lines[0]))
            for j in range(len(lines))
        })

    @property
    def size(self) -> tuple[int, int]:
        return (
            max(self.keys(), key=itemgetter(0))[0] + 1,
            max(self.keys(), key=itemgetter(1))[1] + 1,
        )

    def concat_in_direction(self, x_start: int, y_start: int, length: int, direction: Direction) -> str:
        output = ""
        for s in range(length):
            x = x_start + s * direction.value[0]
            y = y_start + s * direction.value[1]
            if (x, y) not in self:
                break

            output += self[x, y]

        return output


if __name__ == "__main__":
    # some testing with the word search from day 4
    input_lines = read_input(Path(__file__).parent / "day04" / "input.txt")
    grid = Grid2D.from_lines(input_lines)
    print(grid.size)
    for direction in StraightDirection:
        print(grid.concat_in_direction(1, 1, 4, direction))
