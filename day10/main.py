from directions import StraightDirection, translate_position
from grid import Grid2D
from utils import read_input

import networkx as nx

TEST_ANSWER_PART1 = 36
TEST_ANSWER_PART2 = 81


def build_graph(grid: Grid2D) -> nx.DiGraph:
    graph = nx.DiGraph()

    for pos, val in grid.items():
        # graph.add_node(pos)
        for direction in StraightDirection:
            neighbor = translate_position(pos, direction)
            if neighbor in grid and int(grid[neighbor]) - int(val) == 1:
                graph.add_edge(pos, neighbor)

    return graph


def part1(lines: list[str]) -> int:
    grid = Grid2D.from_lines(lines)
    graph = build_graph(grid)

    score = 0
    for zero_pos in grid.get_positions("0"):
        for nine_pos in grid.get_positions("9"):
            if nx.has_path(graph, zero_pos, nine_pos):
                score += 1

    return score


def part2(lines: list[str]) -> int:
    grid = Grid2D.from_lines(lines)
    graph = build_graph(grid)

    total_rating = 0
    for zero_pos in grid.get_positions("0"):
        for nine_pos in grid.get_positions("9"):
            if nx.has_path(graph, zero_pos, nine_pos):
                total_rating += sum(1 for _ in nx.all_simple_paths(graph, zero_pos, nine_pos))

    return total_rating


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
