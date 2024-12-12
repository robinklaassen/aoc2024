from functools import cached_property

import networkx as nx

from directions import StraightDirection, translate_position
from grid import Grid2D, Position
from utils import read_input

TEST_ANSWER_PART1 = 1930
TEST_ANSWER_PART2 = 1206


class GardenGrid(Grid2D):

    @cached_property
    def graph(self) -> nx.Graph:
        graph = nx.Graph()
        for pos, char in self.items():

            graph.add_node(pos)
            for direction in StraightDirection:
                neighbor = translate_position(pos, direction)
                neighbor_char = self.get(neighbor, None)
                if neighbor_char == char:
                    graph.add_edge(pos, neighbor)

        return graph


def get_perimeter_length(region: set[Position]) -> int:
    perimeter = 0
    for pos in region:
        for direction in StraightDirection:
            neighbor = translate_position(pos, direction)
            if neighbor not in region:
                perimeter += 1

    return perimeter


def part1(lines: list[str]) -> int:
    grid = GardenGrid.from_lines(lines)
    total_price = 0
    for region in nx.connected_components(grid.graph):
        region = set(region)
        price = len(region) * get_perimeter_length(region)
        total_price += price

    return total_price


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
