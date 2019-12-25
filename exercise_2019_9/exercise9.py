from intcomputer.intcomputer import IntCodeComputer
from utils.utils import read_file


if __name__ == '__main__':
    computer = IntCodeComputer(read_file(), False, True)
    computer.execute()

    # Answer 1: 2406950601
    # Answer 2: 83239
