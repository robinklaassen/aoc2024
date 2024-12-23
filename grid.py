from collections import UserDict
from operator import itemgetter
from pathlib import Path
from typing import Self

import networkx as nx

from directions import Direction, StraightDirection, translate_position
from utils import read_input

type Position = tuple[int, int]


class Grid2D(UserDict[tuple[int, int], str]):
    """An Advent of Code favorite. Indexed by (x, y) from top left."""

    @classmethod
    def empty(cls, xsize: int, ysize: int) -> Self:
        return cls({
            (i, j): "."
            for i in range(xsize)
            for j in range(ysize)
        })

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

    @property
    def unique_chars(self) -> set[str]:
        return set(self.values())

    def get_positions(self, char: str) -> list[Position]:
        return [p for p, c in self.items() if c == char]

    def print(self):
        xsize, ysize = self.size
        for y in range(ysize):
            print("".join(self[x, y] for x in range(xsize)))

    def build_graph(self) -> nx.Graph:
        graph = nx.Graph()
        for pos, char in self.items():
            if char == "#":
                continue

            graph.add_node(pos)
            for direction in StraightDirection:
                neighbor = translate_position(pos, direction)
                neighbor_char = self.get(neighbor, None)
                if neighbor_char != "#":
                    graph.add_edge(pos, neighbor)
        return graph

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
    # TODO this is just really specific to day 4, move it there
    input_lines = read_input(Path(__file__).parent / "day04" / "input.txt")
    grid = Grid2D.from_lines(input_lines)
    print(grid.size)
    for direction in StraightDirection:
        print(grid.concat_in_direction(1, 1, 4, direction))
