"""I built the Grid2D class with methods for today's puzzle, but only after I finished it."""
from directions import DiagonalDirection, ALL_DIRECTIONS
from utils import read_input, lines_as_dict


def find_words_from_point(lines: list[str], i: int, j: int) -> int:
    return sum(1 for direction in ALL_DIRECTIONS if find_xmas_in_direction(lines, i, j, direction))


def find_xmas_in_direction(lines: list[str], i: int, j: int, direction) -> bool:
    if lines[j][i] != "X":
        return False

    word = ""
    for s in range(1, 4):
        new_i = i + s * direction.value[0]
        new_j = j + s * direction.value[1]

        if new_i < 0 or new_j < 0:
            return False

        try:
            line = lines[j + s * direction.value[1]]
            letter = list(line)[i + s * direction.value[0]]
            word += letter
        except IndexError:
            break

    return word == "MAS"


def part1(lines: list[str]) -> int:
    xsize = len(lines[0])
    ysize = len(lines)

    return sum(find_words_from_point(lines, i, j) for i in range(xsize) for j in range(ysize))


def part2(lines: list[str]) -> int:
    xsize = len(lines[0])
    ysize = len(lines)
    line_dict = lines_as_dict(lines)

    answer = 0

    for i in range(xsize):
        for j in range(ysize):
            if line_dict[i, j] != "A":
                continue

            try:
                letters = ""
                for direction in DiagonalDirection:
                    letters += line_dict[i + direction.value[0], j + direction.value[1]]

                if letters in {"SSMM", "SMMS", "MSSM", "MMSS"}:
                    answer += 1

            except KeyError:
                continue

    return answer


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 18

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == 9
    print(part2(input_lines))
