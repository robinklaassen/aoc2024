from directions import StraightDirection, TURN_RIGHT, translate_position
from grid import Grid2D
from utils import read_input


class LoopError(Exception):
    pass


def walk_the_grid(grid: Grid2D) -> set[tuple[int, int]]:
    start = None
    for (i, j), char in grid.items():
        if char == "^":
            start = i, j
            break

    direction = StraightDirection.UP
    pos = start

    history = set()
    history.add((*pos, direction))

    while True:
        next_pos = translate_position(pos, direction)
        if (*next_pos, direction) in history:
            raise LoopError()

        if next_pos not in grid:
            break

        match grid[next_pos]:
            case "." | "^":
                pos = next_pos
                history.add((*pos, direction))
            case "#":
                direction = TURN_RIGHT[direction]
            case _:
                raise Exception(f"Unexpected symbol {grid[next_pos]}")

    return set((i, j) for i, j, d in history)


def part1(lines: list[str]) -> int:
    grid = Grid2D.from_lines(lines)
    visited_points = walk_the_grid(grid)
    return len(visited_points)


def part2(lines: list[str]) -> int:
    grid = Grid2D.from_lines(lines)
    normal_route = walk_the_grid(grid)

    loop_count = 0
    for target_pos in normal_route:
        if grid[target_pos] != ".":
            continue

        new_grid = grid.copy()
        new_grid[target_pos] = "#"
        try:
            walk_the_grid(new_grid)
        except LoopError:
            loop_count += 1

    return loop_count


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 41

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == 6
    print(part2(input_lines))
