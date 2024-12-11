from functools import cache

from utils import read_input

TEST_ANSWER_PART1 = 55312
TEST_ANSWER_PART2 = ...


def blink(stones: list[int]) -> list[int]:
    output = []
    for s in stones:
        if s == 0:
            output.append(1)
            continue

        st = str(s)
        if len(st) % 2 == 0:
            left, right = st[:len(st) // 2], st[len(st) // 2:]
            output.append(int(left))
            output.append(int(right))
            continue

        output.append(s * 2024)

    return output


def part1(lines: list[str]) -> int:
    assert len(lines) == 1
    line = lines[0]
    stones = [int(x) for x in line.split(" ")]

    for _ in range(25):
        stones = blink(stones)

    return len(stones)


@cache
def blink_single_stone_once(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    st = str(stone)
    if len(st) % 2 == 0:
        left, right = st[:len(st) // 2], st[len(st) // 2:]
        return [int(left), int(right)]

    return [stone * 2024]


@cache
def blinked_stone_count(stone: int, n: int) -> int:
    if n < 1:
        raise ValueError

    blinked_stones = blink_single_stone_once(stone)
    if n == 1:
        return len(blinked_stones)

    return sum(blinked_stone_count(s, n - 1) for s in blinked_stones)


def part2(lines: list[str]) -> int:
    assert len(lines) == 1
    line = lines[0]
    stones = [int(x) for x in line.split(" ")]

    return sum(blinked_stone_count(s, 75) for s in stones)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    print(part2(input_lines))
