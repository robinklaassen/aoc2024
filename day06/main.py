from directions import StraightDirection
from grid import Grid2D
from utils import read_input

TURN_RIGHT = {
    StraightDirection.UP: StraightDirection.RIGHT,
    StraightDirection.RIGHT: StraightDirection.DOWN,
    StraightDirection.DOWN: StraightDirection.LEFT,
    StraightDirection.LEFT: StraightDirection.UP,
}

def part1(lines: list[str]) -> int:
    grid = Grid2D.from_lines(lines)
    start = None
    for (i, j), char in grid.items():
        if char == "^":
            start = i, j
            break

    visited_points = set()
    visited_points.add(start)
    direction = StraightDirection.UP
    pos = start

    while True:
        next_pos = pos[0] + direction.value[0], pos[1] + direction.value[1]
        if next_pos not in grid:
            break

        match grid[next_pos]:
            case "." | "^":
                pos = next_pos
                visited_points.add(pos)
            case "#":
                direction = TURN_RIGHT[direction]
            case _:
                raise Exception(f"Unexpected symbol {grid[next_pos]}")

    return len(visited_points)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 41

    input_lines = read_input()
    print(part1(input_lines))