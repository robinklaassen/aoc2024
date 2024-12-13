import math

from utils import read_input, generate_sections

TEST_ANSWER_PART1 = 480
TEST_ANSWER_PART2 = ...


def extract_button(line: str):
    chars = "".join([c for c in line if c.isdigit() or c == ","])
    return tuple(int(x) for x in chars.split(","))


def win_prize(btn_a, btn_b, prize) -> int | None:
    coins = set()
    for a in range(1, 101):
        for b in range(1, 101):
            pos = (a * btn_a[0] + b * btn_b[0], a * btn_a[1] + b * btn_b[1])
            if pos != prize:
                continue

            coins.add(3 * a + b)

    return min(coins) if coins else None

def win_prize_smarter(btn_a, btn_b, prize) -> int | None:
    # no it's not lcm...
    x_lcm = math.lcm(btn_a[0], btn_b[0])


def part1(lines: list[str]) -> int:
    total_spent = 0
    for section in generate_sections(lines):
        btn_a = extract_button(section[0])
        btn_b = extract_button(section[1])
        prize = extract_button(section[2])

        coins = win_prize(btn_a, btn_b, prize)
        if coins is not None:
            total_spent += coins

    return total_spent


def part2(lines: list[str]) -> int:
    total_spent = 0
    for section in generate_sections(lines):
        btn_a = extract_button(section[0])
        btn_b = extract_button(section[1])
        prize = extract_button(section[2])

        higher_prize = (10000000000000 + prize[0], 10000000000000 + prize[1])
        coins = win_prize_smarter(btn_a, btn_b, higher_prize)
        if coins is not None:
            total_spent += coins

    return total_spent


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    # assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
