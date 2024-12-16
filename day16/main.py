import heapq

from directions import StraightDirection, translate_position, TURN_LEFT, TURN_RIGHT
from grid import Grid2D, Position
from utils import read_input

TEST_ANSWER_PART1 = 7036
TEST_ANSWER_PART2 = 45


class ReindeerMaze(Grid2D):
    def determine_lowest_score(self) -> int:
        start = self.get_positions("S")[0]
        end = self.get_positions("E")[0]

        lowest_scores = dict()

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

                    if ((new_node, new_direction) not in lowest_scores
                            or new_score < lowest_scores[new_node, new_direction]):
                        heapq.heappush(heap, (new_score, new_node, new_direction, new_visited_nodes))
                        lowest_scores[new_node, new_direction] = new_score

    def all_path_nodes_with_score(self, target_score: int) -> set[Position]:
        start = self.get_positions("S")[0]
        end = self.get_positions("E")[0]

        lowest_scores = dict()

        heap: list[tuple[int, Position, StraightDirection, list[Position]]] = [
            (0, start, StraightDirection.RIGHT, [])  # score, node, direction, visited nodes
        ]
        heapq.heapify(heap)

        path_nodes = set()

        while True:
            if not heap:
                break

            score, current_node, direction, visited_nodes = heapq.heappop(heap)
            if score > target_score:
                break

            new_visited_nodes = visited_nodes + [current_node]

            if current_node == end:
                print(new_visited_nodes)
                path_nodes.update(new_visited_nodes)

            for new_direction in [direction, TURN_LEFT[direction], TURN_RIGHT[direction]]:
                new_node = translate_position(current_node, new_direction)
                if self[new_node] == "#" or new_node in visited_nodes:
                    continue

                new_score = score + 1 if new_direction == direction else score + 1001
                if (new_node, new_direction) not in lowest_scores or new_score <= lowest_scores[new_node, new_direction]:
                    heapq.heappush(heap, (new_score, new_node, new_direction, new_visited_nodes))
                    lowest_scores[new_node, new_direction] = new_score

        return path_nodes


def part1(lines: list[str]) -> int:
    maze = ReindeerMaze.from_lines(lines)
    return maze.determine_lowest_score()


def part2(lines: list[str]) -> int:
    maze = ReindeerMaze.from_lines(lines)
    score = maze.determine_lowest_score()
    nodes = maze.all_path_nodes_with_score(score)
    return len(nodes)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test part 1 success!")

    test_lines2 = read_input("test_input2.txt")
    assert part1(test_lines2) == 11048
    print("Test part 1 success!")

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
