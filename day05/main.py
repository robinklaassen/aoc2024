import itertools
from collections import defaultdict
from math import floor

import networkx as nx
from ipysigma import Sigma

from utils import read_input, generate_sections

type RuleSet = list[tuple[int, int]]
type Update = list[int]


def process_input(lines: list[str]) -> tuple[RuleSet, list[Update]]:
    sections = list(generate_sections(lines))
    rules = list()

    for line in sections[0]:
        rule = tuple(int(r) for r in line.split("|"))
        assert len(rule) == 2
        rules.append(rule)

    updates = list()
    for line in sections[1]:
        updates.append([int(p) for p in line.split(",")])

    return rules, updates


def update_is_valid(rules: RuleSet, pages: Update) -> bool:
    for rule in rules:
        if rule[0] not in pages or rule[1] not in pages:
            continue

        if pages.index(rule[0]) > pages.index(rule[1]):
            return False

    return True


def part1(lines: list[str]) -> int:
    rules, updates = process_input(lines)
    answer = 0
    for pages in updates:
        if not update_is_valid(rules, pages):
            continue

        answer += pages[floor(len(pages) / 2)]

    return answer


def part2(lines: list[str]) -> int:
    rules, updates = process_input(lines)

    answer = 0

    for pages in updates:
        if update_is_valid(rules, pages):
            continue

        pages_copy = pages.copy()
        while not update_is_valid(rules, pages_copy):
            for left, right in rules:
                if left not in pages_copy or right not in pages_copy:
                    continue

                i, j = pages_copy.index(left), pages_copy.index(right)
                if i > j:
                    # swap the offending numbers
                    pages_copy[i], pages_copy[j] = pages_copy[j], pages_copy[i]

        answer += pages_copy[floor(len(pages_copy) / 2)]

    return answer


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 143

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == 123
    print(part2(input_lines))
