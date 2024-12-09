from itertools import groupby

from utils import read_input

TEST_ANSWER_PART1 = 1928
TEST_ANSWER_PART2 = 2858


class DiskSpace:
    def __init__(self, line: str):
        self.line = line
        self.item_index = 0
        self.current_file_id = 0
        self.current_blocks = []

    def next_block(self) -> int | None:
        while not self.current_blocks:
            block_count = int(self.line[self.item_index])
            if self.item_index % 2 == 0:
                # item is a file
                file_id = self.current_file_id
                self.current_file_id += 1
            else:
                # item is free space
                file_id = None

            self.current_blocks = block_count * [file_id]
            self.item_index += 1

        return self.current_blocks.pop()


class FileBlocks:
    def __init__(self, line: str):
        self.line = line
        self.file_block_sizes = [int(x) for i, x in enumerate(line) if i % 2 == 0]
        self.total_file_blocks = sum(self.file_block_sizes)
        self.current_blocks = []

    def last_file_block(self) -> int:
        if not self.current_blocks:
            file_id = len(self.file_block_sizes) - 1
            block_count = self.file_block_sizes.pop()
            self.current_blocks = block_count * [file_id]

        return self.current_blocks.pop()


def part1(lines: list[str]) -> int:
    assert len(lines) == 1
    line = lines[0]

    checksum = 0
    disk_space = DiskSpace(line)
    file_blocks = FileBlocks(line)
    for i in range(file_blocks.total_file_blocks):
        file_id = disk_space.next_block()
        if file_id is None:
            file_id = file_blocks.last_file_block()

        checksum += i * file_id

    return checksum


def build_blocks(line: str) -> list[int | None]:
    blocks = []
    file_id = 0

    for i, x in enumerate(line):
        size = int(x)
        if i % 2 == 0:
            # file
            value = file_id
            file_id += 1
        else:
            # space
            value = None

        blocks += size * [value]

    return blocks


def get_free_space_locations(blocks: list[int | None]) -> dict[int, int]:
    # dict of starting index to size of empty space
    output = {}
    index = 0
    for k, v in groupby(blocks):
        contiguous_size = len(list(v))
        if k is None:
            output[index] = contiguous_size
        index += contiguous_size

    return output


def remove_all_occurrences(blocks: list[int | None], value: int):
    # set occurrences to zero, mutates original list
    while True:
        try:
            idx = blocks.index(value)
            blocks[idx] = None
        except ValueError:
            break


def print_blocks(blocks: list[int | None]):
    output = ""
    for el in blocks:
        output += (str(el) if el is not None else ".")
    print(output)


def part2(lines: list[str]) -> int:
    assert len(lines) == 1
    line = lines[0]
    blocks = build_blocks(line)
    file_block_sizes = [int(x) for i, x in enumerate(line) if i % 2 == 0]

    while file_block_sizes:
        file_id = len(file_block_sizes) - 1
        file_size = file_block_sizes.pop()
        free_space = get_free_space_locations(blocks)

        for idx, size in free_space.items():
            if size < file_size:
                continue

            if idx > blocks.index(file_id):
                # do not move files to the right!
                continue

            # move the file
            remove_all_occurrences(blocks, file_id)
            for s in range(file_size):
                blocks[idx + s] = file_id

            break

    # calculate checksum
    checksum = 0
    for i, x in enumerate(blocks):
        if x is None:
            continue

        checksum += i * x

    return checksum


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
