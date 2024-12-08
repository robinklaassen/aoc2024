import itertools
from math import ceil

from grid import Grid2D, Position
from utils import read_input

TEST_ANSWER_PART1 = 14
TEST_ANSWER_PART2 = 34


class AntennaGrid(Grid2D):

    def get_antinodes_in_grid(self, char: str) -> list[Position]:
        antennas = self.get_positions(char)
        antinodes = []
        for a1, a2 in itertools.permutations(antennas, 2):
            node = (
                a1[0] + 2 * (a2[0] - a1[0]),
                a1[1] + 2 * (a2[1] - a1[1]),
            )
            if node in self:
                antinodes.append(node)

        return antinodes

    def get_harmonic_antinodes(self, char: str) -> list[Position]:
        antennas = self.get_positions(char)
        antinodes = []
        for a1, a2 in itertools.permutations(antennas, 2):
            dist = (a2[0] - a1[0], a2[1] - a1[1])
            times = ceil(max((
                self.size[0] / abs(dist[0]),
                self.size[1] / abs(dist[1]),
            )))

            for s in range(times):
                node = (
                    a1[0] + s * (a2[0] - a1[0]),
                    a1[1] + s * (a2[1] - a1[1]),
                )
                if node in self:
                    antinodes.append(node)

        return antinodes


def part1(lines: list[str]) -> int:
    grid = AntennaGrid.from_lines(lines)
    antinodes = set()
    for char in grid.unique_chars:
        if char == ".":
            continue

        antinodes.update(set(grid.get_antinodes_in_grid(char)))
    return len(antinodes)


def part2(lines: list[str]) -> int:
    grid = AntennaGrid.from_lines(lines)
    antinodes = set()
    for char in grid.unique_chars:
        if char == ".":
            continue

        antinodes.update(set(grid.get_harmonic_antinodes(char)))
    return len(antinodes)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
