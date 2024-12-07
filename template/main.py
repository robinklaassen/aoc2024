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

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
