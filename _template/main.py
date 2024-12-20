from utils import read_input

TEST_ANSWER_PART1 = ...
TEST_ANSWER_PART2 = ...


def part1(lines: list[str]) -> int:
    ...


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
