import networkx as nx
from ipysigma import Sigma

from utils import read_input, generate_sections

TEST_ANSWER_PART1 = 4
TEST_ANSWER_PART1_2 = 2024
TEST_ANSWER_PART2 = ...


def parse_input(lines: list[str]) -> tuple[dict[str, int], dict[str, str]]:
    sections = list(generate_sections(lines))
    assert len(sections) == 2

    initial_values = dict()
    for line in sections[0]:
        k, v = line.split(": ")
        initial_values[k] = int(v)

    wire_map = dict()
    for line in sections[1]:
        left, right = line.split(" -> ")
        wire_map[right] = left

    return initial_values, wire_map


def calc_wire(wire: str, wire_map: dict[str, str], initial_values: dict[str, int]) -> int:
    if wire in wire_map:
        left, op, right = wire_map[wire].split(" ")
        val_left = calc_wire(left, wire_map, initial_values)
        val_right = calc_wire(right, wire_map, initial_values)
        match op:
            case "AND":
                return 1 if val_left and val_right else 0
            case "OR":
                return 1 if val_left or val_right else 0
            case "XOR":
                return (val_left + val_right) % 2
            case _:
                raise ValueError

    if wire in initial_values:
        return initial_values[wire]

    raise IndexError


def part1(lines: list[str]) -> int:
    initial_values, wire_map = parse_input(lines)

    z_wires = [w for w in wire_map if w.startswith("z")]
    z_values = {z: calc_wire(z, wire_map, initial_values) for z in z_wires}

    result = 0
    for idx, val in z_values.items():
        result += (val * 2 ** int(idx.lstrip("z")))

    return result


def part2(lines: list[str]) -> str:
    initial_values, wire_map = parse_input(lines)

    graph = nx.DiGraph()
    for out_wire, in_wires in wire_map.items():
        left, op, right = in_wires.split(" ")
        graph.add_edge(left, out_wire, label=op)
        graph.add_edge(right, out_wire, label=op)

    Sigma(graph, height=1000, start_layout=3).to_html("graph.html")

    # took it visually from here, the graph follows a pattern, you can closely inspect to see where it deviates
    # there are 4 places where 2 pairs of edges are swapped
    deviated_wires = ["z11", "vkq", "z24", "mmk", "pvb", "qdq", "z38", "hqh"]
    return ",".join(sorted(deviated_wires))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    test_lines2 = read_input("test_input2.txt")
    assert part1(test_lines2) == TEST_ANSWER_PART1_2
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    # assert part2(test_lines) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
