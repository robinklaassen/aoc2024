from collections import defaultdict
from itertools import pairwise

from utils import read_input

TEST_ANSWER_PART1 = 37327623
TEST_ANSWER_PART2 = 23


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret % 16777216


def evolve_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def evolve_2000(secret: int) -> int:
    for _ in range(2000):
        secret = evolve_secret(secret)
    return secret


def part1(lines: list[str]) -> int:
    return sum(evolve_2000(int(num)) for num in lines)


def generate_prices(secret: int) -> list[int]:
    # could be an actual generator, if need be
    prices = [secret % 10]  # starting price
    for _ in range(2000):
        secret = evolve_secret(secret)
        prices.append(secret % 10)
    return prices


def prices_per_change_sequence(secret: int):
    output = dict()
    prices = generate_prices(secret)  # length 2001
    diffs = [v - u for u, v in pairwise(prices)]  # length 2000
    for i in range(3, len(diffs)):
        last_diffs = diffs[i - 3:i + 1]
        assert len(last_diffs) == 4

        if tuple(last_diffs) in output:
            continue

        output[tuple(last_diffs)] = prices[i + 1]

    return output


def part2(lines: list[str]) -> int:
    # print(prices_per_change_sequence(123))  # looks good

    total_bananas_per_change_sequence = defaultdict(int)
    for secret in lines:
        price_dict = prices_per_change_sequence(int(secret))
        for tup, val in price_dict.items():
            total_bananas_per_change_sequence[tup] += val

    return max(total_bananas_per_change_sequence.values())


if __name__ == "__main__":
    assert mix(42, 15) == 37
    assert prune(100000000) == 16113920

    assert evolve_2000(1) == 8685429

    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    print("Part 1 answer:", part1(input_lines))

    test_lines2 = read_input("test_input2.txt")
    assert part2(test_lines2) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print("Part 2 answer:", part2(input_lines))
