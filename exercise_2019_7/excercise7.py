from intcomputer.intcomputer import IntCodeComputer
from itertools import permutations


def _run_chained_computer(program: str, input_a: int, input_b: int) -> int:
    computer = IntCodeComputer(program, True)
    computer.add_input(input_a)
    computer.add_input(input_b)
    computer.execute()

    return computer.get_output()


def run_chained_computers_from_input(program: str, input_list) -> int:
    output = _run_chained_computer(program, input_list[0], 0)
    output = _run_chained_computer(program, input_list[1], output)
    output = _run_chained_computer(program, input_list[2], output)
    output = _run_chained_computer(program, input_list[3], output)
    output = _run_chained_computer(program, input_list[4], output)

    return output


input_program = '3,8,1001,8,10,8,105,1,0,0,21,42,55,76,89,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,1001,9,' \
                '3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,4,9,99,3,9,102,3,9,9,101,5,9,9,1002,9,2,9,101,4,9,9,4,' \
                '9,99,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,1001,9,5,9,1002,9,2,9,101,2,9,9,4,9,' \
                '99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,' \
                '101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,' \
                '1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,' \
                '9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,' \
                '9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,' \
                '1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,' \
                '9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,' \
                '9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,' \
                '1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,' \
                '2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99 '


if __name__ == '__main__':
    # computer = IntCodeComputer()
    perm = permutations([0, 1, 2, 3, 4])
    max_total = 0
    for input_params in perm:
        total = run_chained_computers_from_input(input_program, list(input_params))
        if total > max_total:
            max_total = total
    print("max_total %d" % max_total)
