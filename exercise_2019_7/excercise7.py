from intcomputer.intcomputer import IntCodeComputer
from itertools import permutations


def _run_chained_computer(program: str, input_a: int, input_b: int) -> int:
    computer = IntCodeComputer(program, True)
    return _run_chained_computer_with_two_inputs(computer, input_a, input_b)


def _run_chained_computer_with_two_inputs(computer: IntCodeComputer, input_a: int, input_b: int) -> int:
    computer.add_input(input_a)
    computer.add_input(input_b)
    computer.debug_name = ("amp [%d] input [%d]" % (input_a, input_b))
    computer.resume()

    return computer.get_output()


def _run_chained_computer_with_single_input(computer: IntCodeComputer, input_value: int) -> int:
    computer.add_input(input_value)
    computer.debug_name = "input value: " + str(input_value)
    computer.resume()

    return computer.get_output()


def run_chained_computers_from_input(program: str, input_list) -> int:
    output = _run_chained_computer(program, input_list[0], 0)
    output = _run_chained_computer(program, input_list[1], output)
    output = _run_chained_computer(program, input_list[2], output)
    output = _run_chained_computer(program, input_list[3], output)
    output = _run_chained_computer(program, input_list[4], output)

    return output


def run_chained_computers_with_feedback(program: str, input_list) -> int:
    computer_a = IntCodeComputer(program, True)
    computer_b = IntCodeComputer(program, True)
    computer_c = IntCodeComputer(program, True)
    computer_d = IntCodeComputer(program, True)
    computer_e = IntCodeComputer(program, True)
    output_from_a = _run_chained_computer_with_two_inputs(computer_a, input_list[0], 0)
    output_from_b = _run_chained_computer_with_two_inputs(computer_b, input_list[1], output_from_a)
    output_from_c = _run_chained_computer_with_two_inputs(computer_c, input_list[2], output_from_b)
    output_from_d = _run_chained_computer_with_two_inputs(computer_d, input_list[3], output_from_c)
    output_from_e = _run_chained_computer_with_two_inputs(computer_e, input_list[4], output_from_d)

    finished = False
    while not finished:
        output_from_a = _run_chained_computer_with_single_input(computer_a, output_from_e)
        output_from_b = _run_chained_computer_with_single_input(computer_b, output_from_a)
        output_from_c = _run_chained_computer_with_single_input(computer_c, output_from_b)
        output_from_d = _run_chained_computer_with_single_input(computer_d, output_from_c)
        output_from_e = _run_chained_computer_with_single_input(computer_e, output_from_d)
        finished = computer_e.finished

    return output_from_e


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
    # Exercise 1
    #
    # perm = permutations([0, 1, 2, 3, 4])
    # max_total = 0
    # for input_params in perm:
    #     total = run_chained_computers_from_input(input_program, list(input_params))
    #     if total > max_total:
    #         max_total = total
    # print("max_total %d" % max_total)

    # Exercise 2
    #
    perm = permutations([5, 6, 7, 8, 9])
    max_total = 0
    for input_params in perm:
        total = run_chained_computers_with_feedback(input_program, list(input_params))
        if total > max_total:
            max_total = total
    print("max_total %d" % max_total)
