from functools import cache

from utils import read_input, generate_sections

TEST_ANSWER_PART1 = 6
TEST_ANSWER_PART2 = ...

@cache
def count_matches(design: str, patterns: frozenset[str]) -> int:
    match_count = 0
    matching_patterns = [pat for pat in patterns if design.startswith(pat)]
    if not matching_patterns:
        return 0

    for mp in matching_patterns:
        remainder = design.lstrip(mp)
        if not remainder:
            match_count += 1
            continue

        remainder_match_count = count_matches(remainder, patterns)
        match_count += remainder_match_count

        # remainder_matches = count_matches(remainder, patterns)
        # for rm in remainder_matches:
        #     matches.append([mp] + rm)

    return match_count


def part1(lines: list[str]) -> int:
    sections = list(generate_sections(lines))
    patterns = frozenset(sections[0][0].split(", "))  # set is not hashable so cannot be cached
    designs = sections[1]

    count = 0
    for design in designs:
        matches = count_matches(design, patterns)
        # print(matches)
        if matches:
            count += 1

    return count


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
