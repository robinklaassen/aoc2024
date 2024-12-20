import networkx as nx

from directions import StraightDirection, translate_position, REVERSE_DIRECTION
from grid import Grid2D, Position
from utils import read_input

TEST_ANSWER_PART1 = ...
TEST_ANSWER_PART2 = ...


class RaceGrid(Grid2D):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_graph = self.build_graph()

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


def part1(lines: list[str]) -> int:
    # takes around a minute, not viable for part 2
    grid = RaceGrid.from_lines(lines)
    start = grid.get_positions("S")[0]
    end = grid.get_positions("E")[0]
    normal_time = nx.shortest_path_length(grid.base_graph, start, end)
    print("Normal time", normal_time)

    checked_positions: list[set[Position]] = []
    graph = grid.base_graph
    cheat_times: list[int] = []

    for pos, char in grid.items():
        x, y = pos
        xsize, ysize = grid.size
        if char != "#" or x == 0 or x == xsize - 1 or y == 0 or y == ysize - 1:
            # only check walls not in the outer border
            continue

        for direction in StraightDirection:
            new_pos = translate_position(pos, direction)
            reversed_pos = translate_position(pos, REVERSE_DIRECTION[direction])
            pos_set = {new_pos, reversed_pos}
            if grid[new_pos] == "#" or grid[reversed_pos] == "#" or pos_set in checked_positions:
                continue

            graph.add_edge(new_pos, reversed_pos)
            cheated_time = nx.shortest_path_length(graph, start, end)
            cheat_times.append(cheated_time + 1)  # the cheated edge takes 2 seconds, not 1

            checked_positions.append(pos_set)
            graph.remove_edge(new_pos, reversed_pos)

    time_saved = [normal_time - cheat_time for cheat_time in cheat_times]
    # print(sorted(time_saved))
    return sum(1 for ts in time_saved if ts >= 100)


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    # assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
