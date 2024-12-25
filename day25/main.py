import itertools

from utils import read_input, generate_sections, transpose_grid

TEST_ANSWER_PART1 = 3


def part1(lines: list[str]) -> int:
    locks = []
    keys = []

    for section in generate_sections(lines):
        is_lock = "#" in section[0]
        heights = [line.count("#") - 1 for line in transpose_grid(section)]
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)

    result = 0
    for lock, key in itertools.product(locks, keys):
        added_heights = [sum(x) for x in zip(lock, key)]
        if all(h <= 5 for h in added_heights):  # height is same for test and real input
            result += 1

    return result


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))
