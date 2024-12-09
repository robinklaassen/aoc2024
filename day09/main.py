from utils import read_input

TEST_ANSWER_PART1 = 1928
TEST_ANSWER_PART2 = ...


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

    # # make entire disk with ints and Nones
    # disk = []
    # for i, x in enumerate(line):
    #     if i % 2 == 0:
    #         ...
    #
    # # make a deque of all file blocks
    # file_block_sizes = [int(x) for i, x in enumerate(line) if i % 2 == 0]
    #
    # file_blocks = deque()
    # for i, s in enumerate(file_block_sizes):
    #     file_blocks += s * [i]
    #
    # total_block_count = sum(file_block_sizes)
    # checksum = 0
    # for i in range(total_block_count):
    #     # determine if index is originally occupied in the line (then popleft) or empty (then popright)
    #     ...


def part2(lines: list[str]) -> int:
    ...


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1

    input_lines = read_input()
    print(part1(input_lines))

    assert part2(test_lines) == TEST_ANSWER_PART2
    print(part2(input_lines))
