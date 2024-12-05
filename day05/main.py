from utils import read_input, generate_grids


def process_input(lines: list[str]):
    sections = list(generate_grids(lines))
    rules = list()

    for line in sections[0]:
        rule = tuple(r for r in line.split("|"))
        assert len(rule) == 2
        rules.append(rule)

    updates = list()
    for line in sections[1]:
        updates.append([int(p) for p in line.split(",")])

    return rules, updates


def page_is_valid(rules: list[tuple[int, int]], pages: [list[list[int]]]) -> bool:
    for rule in rules:
        if rule[0] not in pages or rule[1] not in pages:
            continue

        if pages.index(rule[0]) > pages.index(rule[1]):
            return False

    return True


def part1(lines: list[str]) -> int:
    rules, updates = process_input(lines)
    for update in updates:
        print(page_is_valid(rules, update))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 143

    input_lines = read_input()
    print(part1(input_lines))
