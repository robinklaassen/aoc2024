from directions import StraightDirection, translate_position
from grid import Grid2D, Position
from utils import read_input, generate_sections

TEST_ANSWER_PART1 = 10092
TEST_ANSWER_PART2 = 9021


class WarehouseGrid(Grid2D):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.robot_pos = self.get_positions("@")[0]
        self[self.robot_pos] = "."  # keep things tidy

    def parse_movements(self, movements: str):
        for m in movements:
            d = StraightDirection.from_char(m)
            p = self.robot_pos
            boxes_to_move: list[Position] = []
            while True:
                p = translate_position(p, d)
                if self[p] == "#":
                    # wall, nothing happens
                    break
                elif self[p] == "O":
                    boxes_to_move.append(p)
                elif self[p] == ".":
                    # move boxes
                    new_box_positions = [translate_position(b, d) for b in boxes_to_move]
                    for old_box in boxes_to_move:
                        self[old_box] = "."
                    for new_box in new_box_positions:
                        self[new_box] = "O"

                    # move robot
                    self.robot_pos = translate_position(self.robot_pos, d)

                    # don't do anything else!
                    break

    @property
    def boxes_gps_sum(self) -> int:
        return sum(
            i + 100 * j for i, j in self.get_positions("O")
        )


class ExtendedWarehouseGrid(WarehouseGrid):

    def box_can_move(self, left_pos: Position, direction: StraightDirection) -> bool:
        pl = translate_position(left_pos, direction)
        right_pos = translate_position(left_pos, StraightDirection.RIGHT)
        pr = translate_position(right_pos, direction)
        if self[pl] == "#" or self[pr] == "#":
            return False

        ...

    def parse_movements(self, movements: str):
        for m in movements:
            d = StraightDirection.from_char(m)
            p = self.robot_pos
            boxes_to_move: set[tuple[Position, Position]] = set()
            while True:
                p = translate_position(p, d)
                if self[p] == "#":
                    # wall, nothing happens
                    break
                elif self[p] == "[":
                    p_right = translate_position(p, StraightDirection.RIGHT)
                    boxes_to_move.add((p, p_right))
                elif self[p] == "]":
                    p_left = translate_position(p, StraightDirection.LEFT)
                    boxes_to_move.add((p_left, p))
                elif self[p] == ".":
                    # move boxes
                    new_lefts = []
                    new_rights = []
                    for left, right in boxes_to_move:
                        new_lefts.append(translate_position(left, d))
                        new_rights.append(translate_position(right, d))
                        self[left] = "."
                        self[right] = "."

                    for l in new_lefts:
                        self[l] = "["

                    for r in new_rights:
                        self[r] = "]"

                    # move robot
                    self.robot_pos = translate_position(self.robot_pos, d)

                    # don't do anything else!
                    break

    @property
    def boxes_gps_sum(self) -> int:
        return sum(
            i + 100 * j for i, j in self.get_positions("[")
        )


def part1(lines: list[str]) -> int:
    sections = list(generate_sections(lines))
    grid = WarehouseGrid.from_lines(sections[0])
    movements = "".join(line for line in sections[1])
    grid.parse_movements(movements)
    return grid.boxes_gps_sum


def extend_grid(lines: list[str]) -> list[str]:
    extended_grid: list[str] = []
    for line in lines:
        extended_line = ""
        for c in line:
            match c:
                case "#":
                    nc = "##"
                case "O":
                    nc = "[]"
                case ".":
                    nc = ".."
                case "@":
                    nc = "@."
                case _:
                    raise ValueError
            extended_line += nc
        extended_grid.append(extended_line)
    return extended_grid


def part2(lines: list[str]) -> int:
    sections = list(generate_sections(lines))
    extended_lines = extend_grid(sections[0])
    grid = ExtendedWarehouseGrid.from_lines(extended_lines)
    movements = "".join(line for line in sections[1])

    grid.print()
    print("***")
    grid.parse_movements(movements)
    grid.print()

    return grid.boxes_gps_sum


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
