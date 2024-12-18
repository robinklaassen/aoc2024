import networkx as nx

from directions import StraightDirection, translate_position
from grid import Grid2D
from utils import read_input

TEST_ANSWER_PART1 = 22
TEST_ANSWER_PART2 = "6,1"


class MemoryGrid(Grid2D):

    @property
    def graph(self) -> nx.Graph:
        graph = nx.Graph()
        for pos, char in self.items():
            if char == "#":
                continue

            graph.add_node(pos)
            for direction in StraightDirection:
                neighbor = translate_position(pos, direction)
                neighbor_char = self.get(neighbor, None)
                if neighbor_char == char:
                    graph.add_edge(pos, neighbor)

        return graph


def part1(lines: list[str], grid_size: int, num_bytes: int) -> int:
    grid = MemoryGrid.empty(grid_size, grid_size)
    for byte_idx in range(num_bytes):
        byte_pos = tuple(int(x) for x in lines[byte_idx].split(","))
        assert len(byte_pos) == 2
        grid[byte_pos] = "#"

    return nx.shortest_path_length(grid.graph, (0, 0), (grid_size - 1, grid_size - 1))


def part2(lines: list[str], grid_size: int) -> str:
    # brute forcing this, takes a few seconds which is fine
    grid = MemoryGrid.empty(grid_size, grid_size)
    graph = grid.graph
    for byte_idx in range(len(lines)):
        byte_pos = tuple(int(x) for x in lines[byte_idx].split(","))
        assert len(byte_pos) == 2

        graph.remove_node(byte_pos)

        if not nx.has_path(graph, (0, 0), (grid_size - 1, grid_size - 1)):
            return ",".join(str(x) for x in byte_pos)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines, 7, 12) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines, 71, 1024))

    assert part2(test_lines, 7) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines, 71))
