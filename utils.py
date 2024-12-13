from pathlib import Path
from typing import Iterator


def read_input(filepath: Path | str = "input.txt") -> list[str]:
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()
    return lines


def generate_sections(lines: list[str], sep="") -> Iterator[list[str]]:
    grid = []
    for line in lines:
        if line == sep:
            yield grid
            grid = []
        else:
            grid.append(line)
    yield grid


def transpose_grid(lines: list[str]) -> list[str]:
    return ["".join(list(tup)) for tup in zip(*lines)]


def find_indexes(s: str, ch: str) -> list[int]:
    return [i for i, ltr in enumerate(s) if ltr == ch]


def lines_as_dict(lines: list[str]) -> dict[tuple[int, int], str]:
    output = dict()
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            output[i, j] = lines[j][i]
    return output
