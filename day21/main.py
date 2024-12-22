import itertools
from functools import cache
from itertools import pairwise

import networkx as nx

from directions import StraightDirection, translate_position
from grid import Grid2D
from utils import read_input

TEST_ANSWER_PART1 = 126384
TEST_ANSWER_PART2 = ...

NUMERIC_KEYPAD_LINES = [
    "789",
    "456",
    "123",
    "#0A",
]

DIRECTIONAL_KEYPAD_LINES = [
    "#^A",
    "<v>",
]


class Keypad(Grid2D):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.graph = self.build_graph()
        self.current_char = "A"

    def build_graph(self) -> nx.DiGraph:
        # customized with chars in edges
        graph = nx.DiGraph()
        for pos, char in self.items():
            if char == "#":
                continue

            graph.add_node(pos)
            for dir_char in "^v<>":
                direction = StraightDirection.from_char(dir_char)
                neighbor = translate_position(pos, direction)
                neighbor_char = self.get(neighbor, None)
                if neighbor_char is not None and neighbor_char != "#":
                    graph.add_edge(pos, neighbor, char=dir_char)
        return graph

    def all_ways_to_type_code(self, code: str) -> list[str]:
        # all possible sequences of moves for entire code
        self.current_char = "A"
        ways_per_char: list[list[str]] = []
        for char in code:
            ways = self.all_ways_to_move_to_and_press_char(char)
            ways_per_char.append(ways)

        ways = []
        for x in itertools.product(*ways_per_char):
            ways.append("".join(x))

        return ways

    def shortest_way_to_type_code(self, code: str) -> str:
        # one of the shortest ways, starts and ends with A
        if not code.endswith("A"):
            raise ValueError

        self.current_char = "A"
        moves = ""
        for char in code:
            moves += self.shortest_move_to_press_char(char)

        return moves

    def shortest_move_to_press_char(self, new_char: str) -> str:
        source = self.get_positions(self.current_char)[0]
        target = self.get_positions(new_char)[0]
        path = nx.shortest_path(self.graph, source, target)
        moves = ""
        for u, v in pairwise(path):
            moves += self.graph[u][v]["char"]
        moves += "A"  # press
        return moves

    def all_ways_to_move_to_and_press_char(self, new_char: str) -> list[str]:
        # all possible sequences of moves for single char (changes current position)
        source = self.get_positions(self.current_char)[0]
        target = self.get_positions(new_char)[0]
        possible_moves = []
        for path in nx.all_shortest_paths(self.graph, source, target):
            moves = ""
            for u, v in pairwise(path):
                moves += self.graph[u][v]["char"]

            self.current_char = new_char

            moves += "A"
            possible_moves.append(moves)
        return possible_moves


@cache
def new_directional_keypad() -> Keypad:
    return Keypad.from_lines(DIRECTIONAL_KEYPAD_LINES)


@cache
def directional_ways(code: str) -> list[str]:
    dir_keypad = new_directional_keypad()
    return dir_keypad.all_ways_to_type_code(code)


@cache
def shortest_directional_code(code: str) -> str:
    dir_keypad = new_directional_keypad()
    # return dir_keypad.shortest_way_to_type_code(code)
    ways = dir_keypad.all_ways_to_type_code(code)
    return min(ways, key=len)


@cache
def directional_shortest_sequence_length(code: str) -> int:
    dir_keypad = new_directional_keypad()
    return min(len(w) for w in dir_keypad.all_ways_to_type_code(code))


def segmentize(code: str) -> list[str]:
    # split the code in segments, where every segments ends with A
    assert code.endswith("A")
    return [part + "A" for part in code[:-1].split("A")]

    # output = []
    # for part in code.split("A"):
    #
    #     output.append(part + "A")
    #
    # return output

@cache
def recursive_pressing_code(code: str, n: int) -> str:
    if n == 0:
        return code

    result = ""
    for seg in segmentize(code):
        new_code = shortest_directional_code(seg)
        result += recursive_pressing_code(new_code, n - 1)

    return result



@cache
def recursive_pressing_length(code: str, n: int) -> int:
    if n == 0:
        return len(code)

    result = 0
    for seg in segmentize(code):
        new_code = shortest_directional_code(seg)
        result += recursive_pressing_length(new_code, n - 1)

    return result


def shortest_sequence_length(code: str, intermediate_keypad_count: int) -> int:
    num_keypad = Keypad.from_lines(NUMERIC_KEYPAD_LINES)

    lengths = []
    for num_keypad_way in num_keypad.all_ways_to_type_code(code):
        code = recursive_pressing_code(num_keypad_way, 1)
        print(code)

        lengths.append(recursive_pressing_length(num_keypad_way, intermediate_keypad_count))

        # for dir_way1 in directional_ways(num_keypad_way):
        #     for dir_way2 in directional_ways(dir_way1):
        #         shortest_length = min(shortest_length, len(dir_way2))

    return min(lengths)
    # return shortest_length


def part1(lines: list[str]) -> int:
    output = 0
    for code in lines:
        seq_len = shortest_sequence_length(code, 2)
        num_part = int(code.rstrip("A"))
        output += seq_len * num_part
    return output


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    assert shortest_sequence_length("029A", 2) == 68

    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
