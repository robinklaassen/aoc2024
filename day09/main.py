from collections import deque

from utils import read_input

TEST_ANSWER_PART1 = 1928
TEST_ANSWER_PART2 = ...


def part1(lines: list[str]) -> int:
    assert len(lines) == 1
    line = lines[0]

    # make entire disk with ints and Nones
    disk = []
    for i, x in enumerate(line):
        if i % 2 == 0:
            ...

    # make a deque of all file blocks
    file_block_sizes = [int(x) for i, x in enumerate(line) if i % 2 == 0]

    file_blocks = deque()
    for i, s in enumerate(file_block_sizes):
        file_blocks += s * [i]

    total_block_count = sum(file_block_sizes)
    checksum = 0
    for i in range(total_block_count):
        # determine if index is originally occupied in the line (then popleft) or empty (then popright)
        ...


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
