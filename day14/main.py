import math
from collections import defaultdict
from pathlib import Path

from PIL import Image

from utils import read_input

TEST_ANSWER_PART1 = 12
TEST_ANSWER_PART2 = ...


def parse_line(line: str) -> tuple[int, int, int, int]:
    numbers = []
    for part in line.split(" "):
        part = part.lstrip("pv=")
        numbers.extend(int(x) for x in part.split(","))
    return tuple(numbers)  # type: ignore


def part1(lines: list[str], xsize: int, ysize: int) -> int:
    quadrant_counts = defaultdict(int)
    for line in lines:
        sx, sy, vx, vy = parse_line(line)

        # determine position after 100 seconds
        px = sx + 100 * vx
        py = sy + 100 * vy

        rpx = px % xsize
        rpy = py % ysize

        assert 0 <= rpx < xsize
        assert 0 <= rpy < ysize

        # determine quadrant
        mid_x = (xsize - 1) // 2
        mid_y = (ysize - 1) // 2

        if rpx == mid_x or rpy == mid_y:
            continue

        quadrant = ""
        if rpx < mid_x and rpy < mid_y:
            quadrant = "ul"
        if rpx > mid_x and rpy < mid_y:
            quadrant = "ur"
        if rpx < mid_x and rpy > mid_y:
            quadrant = "dl"
        if rpx > mid_x and rpy > mid_y:
            quadrant = "dr"

        quadrant_counts[quadrant] += 1

    return math.prod(quadrant_counts.values())


def part2(lines: list[str], xsize: int, ysize: int) -> int:
    robots = [parse_line(line) for line in lines]
    for i in range(10_000):
        positions = set()
        for sx, sy, vx, vy in robots:
            px = (sx + i * vx) % xsize
            py = (sy + i * vy) % ysize
            positions.add((px, py))

        img = Image.new("RGB", (xsize, ysize), color=(0, 0, 0))
        pixels = img.load()
        for x, y in positions:
            pixels[x, y] = (0, 255, 0)

        fname = f"chr_{i}.png"
        img.save("output/" + fname)


        # for y in range(ysize):
        #     chars = ["#" if (x, y) in positions else "." for x in range(xsize)]
        #     print("".join(chars))
        #
        # i += 1


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines, 11, 7) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines, 101, 103))

    # assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines, 101, 103))
