from functools import cache

from utils import read_input


def parse_lines(lines: list[str]) -> list[tuple[int, list[int]]]:
    output = list()
    for line in lines:
        left, right = line.split(": ")
        output.append((int(left), [int(x) for x in right.split(" ")]))
    return output


@cache
def get_possible_operator_combinations(length: int, with_concat: bool = False) -> list[str]:
    output = ["+", "*"]
    if with_concat:
        output.append("|")
    for _ in range(length - 1):
        new_output = []
        for x in output:
            new_output.extend([x + "+", x + "*"])
            if with_concat:
                new_output.append(x + "|")
        output = new_output
    return output


def any_valid_operator_combo(result: int, numbers: list[int], with_concat: bool = False) -> bool:
    num_operators = len(numbers) - 1
    for operators in get_possible_operator_combinations(length=num_operators, with_concat=with_concat):
        num = numbers[0]
        for i in range(len(numbers) - 1):
            match operators[i]:
                case "+":
                    num = num + numbers[i + 1]
                case "*":
                    num = num * numbers[i + 1]
                case "|":
                    num = int(str(num) + str(numbers[i + 1]))
                case _:
                    raise Exception()

        if num == result:
            return True
    return False


def part1(lines: list[str]) -> int:
    equations = parse_lines(lines)
    return sum(result for result, numbers in equations if any_valid_operator_combo(result, numbers))


def part2(lines: list[str]) -> int:
    equations = parse_lines(lines)
    return sum(result for result, numbers in equations if
               any_valid_operator_combo(result, numbers, with_concat=True))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 3749

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == 11387
    print(part2(input_lines))
