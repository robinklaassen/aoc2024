"""Infi is one of the sponsors of AoC 2024. They made their own puzzle at https://aoc.infi.nl/2024"""

import networkx as nx

from directions import Direction3D, translate_position_3d
from utils import read_input

TEST_ANSWER_PART1 = 5686200


def dimension_value(val: str, x: int, y: int, z: int) -> int:
    match val.lower():
        case "x":
            return x
        case "y":
            return y
        case "z":
            return z
        case _:
            return int(val)


def run_instructions(instructions: list[str], x: int, y: int, z: int) -> int:
    program_counter = 0
    stack: list[int] = []

    while True:
        inst = instructions[program_counter]
        if inst == "ret":
            return stack.pop()
        elif inst == "add":
            first = stack.pop()
            second = stack.pop()
            stack.append(first + second)
        elif inst.startswith("push"):
            val = inst.split(" ")[-1]
            stack.append(dimension_value(val, x, y, z))
        elif inst.startswith("jmpos"):
            offset = inst.split(" ")[-1]
            if stack.pop() >= 0:
                program_counter += int(offset)
        else:
            raise ValueError

        program_counter += 1


def make_snow_map(lines: list[str]) -> dict[tuple[int, int, int], int]:
    return {
        (x, y, z): run_instructions(lines, x, y, z)
        for x in range(30)
        for y in range(30)
        for z in range(30)
    }


def part1(lines: list[str]) -> int:
    return sum(make_snow_map(lines).values())


def part2(lines: list[str]) -> int:
    snow_map = {k: v for k, v in make_snow_map(lines).items() if v > 0}  # only actual snow

    graph = nx.Graph()
    for pos in snow_map:
        for d in Direction3D:
            neighbor = translate_position_3d(pos, d)
            if neighbor not in snow_map:
                continue
            graph.add_edge(pos, neighbor)

    return len(list(nx.connected_components(graph)))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    # assert part2(test_lines) == TEST_ANSWER_PART2
    # print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
