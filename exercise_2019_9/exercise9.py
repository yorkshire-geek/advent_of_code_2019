from intcomputer.intcomputer import IntCodeComputer


def read_file():
    input_file = open("input.txt", "r")
    if input_file.mode == 'r':
        return input_file.read()


if __name__ == '__main__':
    computer = IntCodeComputer(read_file(), False, True)
    computer.execute()

    # Answer 1: 2406950601
    # Answer 2: 83239
