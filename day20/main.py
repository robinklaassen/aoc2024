import networkx as nx

from directions import StraightDirection, translate_position, REVERSE_DIRECTION
from grid import Grid2D, Position
from utils import read_input

TEST_ANSWER_PART1 = 5
TEST_ANSWER_PART2 = 41


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


def part1(lines: list[str], min_time_saved: int) -> int:
    grid = RaceGrid.from_lines(lines)
    start = grid.get_positions("S")[0]
    end = grid.get_positions("E")[0]

    times = nx.shortest_path_length(grid.base_graph, source=None, target=end)
    time_saved: list[int] = []
    for pos, normal_time in times.items():
        for d in StraightDirection:
            new_pos = translate_position(pos, d, 2)
            new_time = times.get(new_pos, None)
            if new_time is None:
                continue  # wall, or out of bounds

            if new_time >= normal_time - 2:
                continue  # not a shortcut

            time_saved.append(normal_time - new_time - 2)

    # print(sorted(time_saved))
    return sum(1 for ts in time_saved if ts >= min_time_saved)


def part2(lines: list[str], min_time_saved: int) -> int:
    grid = RaceGrid.from_lines(lines)
    start = grid.get_positions("S")[0]
    end = grid.get_positions("E")[0]

    # make a list of possible diffs for 20 ps
    diffs: list[Position] = []
    for x in range(-20, 21):
        for y in range(-20, 21):
            if abs(x) + abs(y) > 20:
                continue
            diffs.append((x, y))

    times = nx.shortest_path_length(grid.base_graph, source=None, target=end)
    time_saved: list[int] = []
    for pos, normal_time in times.items():
        for diff in diffs:
            jump_time = abs(diff[0]) + abs(diff[1])
            new_pos = (pos[0] + diff[0], pos[1] + diff[1])
            new_time = times.get(new_pos, None)
            if new_time is None:
                continue  # wall, or out of bounds

            if new_time >= normal_time - jump_time:
                continue  # not a shortcut

            time_saved.append(normal_time - new_time - jump_time)

    # print(sorted(time_saved))
    return sum(1 for ts in time_saved if ts >= min_time_saved)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines, 20) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines, 100))

    assert part2(test_lines, 70) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines, 100))
