from itertools import pairwise

from utils import read_input


def line_is_safe(line: str) -> bool:
    numbers = [int(x) for x in line.split(" ")]
    diffs = [y - x for x, y in pairwise(numbers)]
    return set(diffs) <= {1, 2, 3} or set(diffs) <= {-1, -2, -3}


def line_is_safe_dampened(line: str) -> bool:
    # Brute forcing! The computer has more time than I do :)
    numbers = [int(x) for x in line.split(" ")]
    for idx in range(len(numbers)):
        numbers_copy = numbers.copy()
        numbers_copy.pop(idx)
        line_copy = " ".join(str(x) for x in numbers_copy)
        if line_is_safe(line_copy):
            return True
    return False


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    test_output = [line_is_safe(line) for line in test_lines]
    assert test_output == [True, False, False, False, False, True]

    lines = read_input("input.txt")
    print(sum(1 for line in lines if line_is_safe(line)))  # part 1

    print(sum(1 for line in lines if line_is_safe_dampened(line)))  # part 2
