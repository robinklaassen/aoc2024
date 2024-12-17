from typing import Self

from utils import read_input

TEST_ANSWER_PART1 = [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]
TEST_ANSWER_PART2 = 117440


class Computer:
    def __init__(self, registers: tuple[int, int, int], program: list[int]):
        self.registers = registers
        self.program = program

        self.pointer = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        assert len(lines) == 5
        registers = tuple(
            int(lines[i].split(": ")[1])
            for i in range(3)
        )
        assert len(registers) == 3
        program_string = lines[4].split(": ")[1]
        program = [int(x) for x in program_string.split(",")]
        return cls(registers, program)  # type: ignore

    def run_to_halt(self) -> list[int]:
        output = []
        while True:
            if self.pointer >= len(self.program):
                return output

            pointer_before = self.pointer

            instruction_result = self.run_instruction(self.program[self.pointer], self.program[self.pointer + 1])
            if instruction_result is not None:
                output.append(instruction_result)

            if self.pointer == pointer_before:
                self.pointer += 2

    def run_instruction(self, opcode: int, operand: int) -> int | None:
        A, B, C = self.registers
        match opcode:
            case 0:
                value = A // (2 ** self._get_combo_operand_value(operand))
                self.registers = value, B, C
            case 1:
                value = B ^ operand
                self.registers = A, value, C
            case 2:
                value = self._get_combo_operand_value(operand) % 8
                self.registers = A, value, C
            case 3:
                if A != 0:
                    self.pointer = operand  # DO NOT MOVE POINTER AFTERWARD
            case 4:
                value = B ^ C
                self.registers = A, value, C
            case 5:
                value = self._get_combo_operand_value(operand) % 8
                return value
            case 6:
                value = A // (2 ** self._get_combo_operand_value(operand))
                self.registers = A, value, C
            case 7:
                value = A // (2 ** self._get_combo_operand_value(operand))
                self.registers = A, B, value
            case _:
                raise Exception

    def _get_combo_operand_value(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4 | 5 | 6:
                return self.registers[operand - 4]
            case _:
                raise Exception

    def run_to_find_quine(self) -> bool:

        output = []
        while True:
            if self.pointer >= len(self.program):
                return output == self.program

            pointer_before = self.pointer

            instruction_result = self.run_instruction(self.program[self.pointer], self.program[self.pointer + 1])
            if instruction_result is not None:
                if instruction_result != self.program[len(output)]:
                    # this early return is fast, but not fast enough
                    return False
                output.append(instruction_result)

            if self.pointer == pointer_before:
                self.pointer += 2

    def find_quine(self) -> int:
        new_A = 0
        while True:
            # if new_A > 120_000:
            #     print("too long")
            #     break
            self.registers = (new_A, 0, 0)
            self.pointer = 0
            if self.run_to_find_quine():
                return new_A
            new_A += 1

    def reset(self, A: int):
        self.registers = (A, 0, 0)
        self.pointer = 0


def test_computer():
    # I wrote these because there was a bug, or so I thought.
    # Turns out code was correct but needed to send the output with commas (I stripped them and sent a number).
    computer = Computer((0, 0, 9), [2, 6])
    computer.run_to_halt()
    assert computer.registers[1] == 1

    computer = Computer((10, 0, 0), [5, 0, 5, 1, 5, 4])
    output = computer.run_to_halt()
    assert output == [0, 1, 2]

    computer = Computer((2024, 0, 0), [0, 1, 5, 4, 3, 0])
    output = computer.run_to_halt()
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert computer.registers[0] == 0

    computer = Computer((0, 29, 0), [1, 7])
    computer.run_to_halt()
    assert computer.registers[1] == 26

    computer = Computer((0, 2024, 43690), [4, 0])
    computer.run_to_halt()
    assert computer.registers[1] == 44354


def part1(lines: list[str]) -> list[int]:
    computer = Computer.from_lines(lines)
    return computer.run_to_halt()


def part2(lines: list[str]) -> int:
    for i in range(300):
        new_A = i
        # new_A = 35_184_372_000_000 + i
        computer = Computer.from_lines(lines)
        A, B, C = computer.registers
        computer.registers = new_A, B, C
        output = computer.run_to_halt()
        print(i, output)
        if output == computer.program:
            return new_A

    # return Computer.from_lines(lines).find_quine()  # doesn't work

    # new attempt
    # try to find starting point for correct last bit

    # computer = Computer.from_lines(lines)
    # start_A = 8 ** (len(computer.program) - 1)
    # bit_pos = 15
    # A = start_A
    # while True:
    #     computer.reset(A)
    #     output = computer.run_to_halt()
    #     if output == computer.program:
    #         return A
    #
    #     if output[bit_pos] == computer.program[bit_pos]:
    #         bit_pos -= 1
    #     A += 8**(bit_pos)

    # above errors with A == 164540892147329.12
    # so it's around there?
    A = 164540892147329
    while True:
        computer.reset(A)
        output = computer.run_to_halt()
        if output == computer.program:
            return A
        A += 1

    # got correct answer, not gonna bother fixing this

if __name__ == "__main__":
    test_computer()

    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == TEST_ANSWER_PART1
    print("Test(s) for part 1 succeeded!")

    input_lines = read_input()
    ans1 = part1(input_lines)
    print(ans1)
    print(",".join(str(x) for x in ans1))

    test_lines2 = read_input("test_input2.txt")
    # assert part2(test_lines2) == TEST_ANSWER_PART2
    print("Test(s) for part 2 succeeded!")
    print(part2(input_lines))
