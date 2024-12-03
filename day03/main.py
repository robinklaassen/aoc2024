import re

from utils import read_input


def calculate_part1(line: str) -> int:
    pat = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pat, line)
    return sum(int(x) * int(y) for x, y in matches)


def find_muls_with_index(line: str) -> dict[int, int]:
    pat = r"mul\((\d+),(\d+)\)"
    output = dict()
    for m in re.finditer(pat, line):
        idx = m.start()
        x, y = m.groups()
        val = int(x) * int(y)
        output[idx] = val
    return output


def find_do_donts(line: str) -> dict[int, bool]:
    pat = r"(do\(\)|don't\(\))"
    output = dict()
    output[0] = True  # start enabled
    for m in re.finditer(pat, line):
        idx = m.start()
        match m.groups()[0]:
            case "do()":
                val = True
            case "don't()":
                val = False
            case _:
                raise Exception()
        output[idx] = val
    return output


def calculate_part2(line: str) -> int:
    muls = find_muls_with_index(line)
    dodonts = find_do_donts(line)
    answer = 0
    for idx, val in muls.items():
        enabled = [v for k, v in dodonts.items() if k < idx][-1]
        if enabled:
            answer += val
    return answer


if __name__ == "__main__":
    test_line = r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert calculate_part1(test_line) == 161

    input_lines = read_input("input.txt")
    whole_input = "".join(input_lines)
    print(calculate_part1(whole_input))

    # part 2
    test_line2 = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert calculate_part2(test_line2) == 48

    print(calculate_part2(whole_input))
