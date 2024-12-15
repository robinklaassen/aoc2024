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

    def boxes_to_move_horizontal(self, box: Position, direction: StraightDirection) -> set[Position]:
        # we use only the left side of the box as position indicator
        match direction:
            case StraightDirection.LEFT:
                new_pos = translate_position(box, StraightDirection.LEFT, 1)
            case StraightDirection.RIGHT:
                new_pos = translate_position(box, StraightDirection.RIGHT, 2)
            case _:
                raise Exception

        if self[new_pos] == "#":
            return set()
        if self[new_pos] == ".":
            return {box}

        if self[new_pos] == "[":
            pass
            # new_pos = new_pos
        elif self[new_pos] == "]":
            new_pos = translate_position(new_pos, StraightDirection.LEFT)
        else:
            raise Exception

        extra_boxes = self.boxes_to_move_horizontal(new_pos, direction)
        if not extra_boxes:
            return set()

        return extra_boxes.union({box})

    def boxes_to_move_vertical(self, box: Position, direction: StraightDirection) -> set[Position]:
        new_pos_left = translate_position(box, direction)
        new_pos_right = translate_position(new_pos_left, StraightDirection.RIGHT)
        chars = self[new_pos_left] + self[new_pos_right]

        if "#" in chars:
            return set()  # wall

        match chars:
            case "..":
                return {box}
            case "].":
                new_pos = translate_position(new_pos_left, StraightDirection.LEFT)
                extra_boxes = self.boxes_to_move_vertical(new_pos, direction)
            case ".[":
                extra_boxes = self.boxes_to_move_vertical(new_pos_right, direction)
            case "[]":
                extra_boxes = self.boxes_to_move_vertical(new_pos_left, direction)
            case "][":
                new_pos = translate_position(new_pos_left, StraightDirection.LEFT)
                extra_boxes_left = self.boxes_to_move_vertical(new_pos, direction)
                extra_boxes_right = self.boxes_to_move_vertical(new_pos_right, direction)
                if not extra_boxes_left or not extra_boxes_right:
                    return set()  # either or both cannot extra's cannot move, so current box cannot move either
                extra_boxes = extra_boxes_left.union(extra_boxes_right)
            case _:
                raise ValueError

        if not extra_boxes:
            return set()

        return extra_boxes.union({box})

    def parse_movements(self, movements: str):
        for m in movements:
            d = StraightDirection.from_char(m)
            p = self.robot_pos
            target_pos = translate_position(p, d)
            if self[target_pos] == "#":
                # wall, do nothing
                continue

            if self[target_pos] == ".":
                # no box, only move robot
                self.robot_pos = target_pos
                continue

            # there is a box part in the target position of the robot
            if self[target_pos] == "[":
                box_pos = target_pos
            elif self[target_pos] == "]":
                box_pos = translate_position(target_pos, StraightDirection.LEFT)
            else:
                raise Exception

            if d in [StraightDirection.LEFT, StraightDirection.RIGHT]:
                boxes_to_move = self.boxes_to_move_horizontal(box_pos, d)
            else:
                boxes_to_move = self.boxes_to_move_vertical(box_pos, d)

            if not boxes_to_move:
                # boxes cannot move, do nothing
                continue

            # boxes can move, so do it
            new_box_positions = {translate_position(box, d) for box in boxes_to_move}
            for box in boxes_to_move:
                self[box] = "."
                self[translate_position(box, StraightDirection.RIGHT)] = "."

            for box in new_box_positions:
                self[box] = "["
                self[translate_position(box, StraightDirection.RIGHT)] = "]"

            # also move robot!
            self.robot_pos = target_pos

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
    grid.parse_movements(movements)
    return grid.boxes_gps_sum


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
