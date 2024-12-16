import heapq

from directions import StraightDirection, translate_position, TURN_LEFT, TURN_RIGHT
from grid import Grid2D
from utils import read_input

TEST_ANSWER_PART1 = 7036
TEST_ANSWER_PART2 = ...


class ReindeerMaze(Grid2D):
    def solve_maze(self) -> int:
        start = self.get_positions("S")[0]
        end = self.get_positions("E")[0]

        heap = [
            (0, start, StraightDirection.RIGHT, set())  # score, node, direction, visited nodes
        ]
        heapq.heapify(heap)

        while True:
            score, current_node, direction, visited_nodes = heapq.heappop(heap)
            if current_node == end:
                return score

            new_visited_nodes = visited_nodes.union({current_node})

            for new_direction in [direction, TURN_LEFT[direction], TURN_RIGHT[direction]]:
                new_node = translate_position(current_node, new_direction)
                if self[new_node] != "#" and new_node not in visited_nodes:
                    new_score = score + 1 if new_direction == direction else score + 1001
                    heapq.heappush(heap, (new_score, new_node, new_direction, new_visited_nodes))

    # def dijkstra(self):
    #     start = self.get_positions("S")[0]
    #     end = self.get_positions("E")[0]
    #
    #     unvisited_nodes: set[Position] = set(self.get_positions(".")).union(start, end)
    #     distance_map = {n: math.inf for n in unvisited_nodes}
    #     distance_map[start] = 0
    #
    #     while True:
    #         if not unvisited_nodes:
    #             break
    #
    #         current_node = min(distance_map, key=distance_map.get)
    #         if distance_map[current_node] == math.inf:
    #             break


def part1(lines: list[str]) -> int:
    maze = ReindeerMaze.from_lines(lines)
    return maze.solve_maze()


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test part 1 success!")

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
