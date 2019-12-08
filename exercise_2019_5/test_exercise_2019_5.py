import unittest
from .exercise_2019_5 import IntCodeComputer
from .exercise_2019_5 import program_as_list

_test_data = '1,9,10,3,2,3,11,0,99,30,40,50'


class MyTestCase(unittest.TestCase):
    def test_program_as_list(self):
        program_list = program_as_list('1002,4,3,4,33')
        self.assertEqual(len(program_list), 5)

    def test_get_next_op_code(self):
        computer = IntCodeComputer(program_as_list('99,4,3,4,33'))
        self.assertEqual(computer.is_not_finished(), False)

    def test_simple_add_parse_frame(self):
        computer = IntCodeComputer(program_as_list('1,9,10,3,2,3,11,0,99,30,40,50'))
        frame = computer.parse_frame()
        self.assertEqual(frame, {"op_code": 1, "op_code_mask": "000", "param1": 30, "param2": 40, "param3": 3})

    def test_run_command_add(self):
        computer = IntCodeComputer(program_as_list(_test_data))
        computer.run_command(computer.parse_frame())
        self.assertEqual(computer.program_list, program_as_list('1,9,10,70,2,3,11,0,99,30,40,50'))

    def test_run_command_add_multiply(self):
        computer = IntCodeComputer(program_as_list(_test_data))
        computer.run_command(computer.parse_frame())  # add
        computer.run_command(computer.parse_frame())  # multiply
        self.assertEqual(computer.program_list, program_as_list('3500,9,10,70,2,3,11,0,99,30,40,50'))

    def test_execute_computer(self):
        computer = IntCodeComputer(program_as_list(_test_data))
        computer.execute()
        self.assertEqual(computer.program_list, program_as_list('3500,9,10,70,2,3,11,0,99,30,40,50'))

    def test_multiply_with_mask(self):
        computer = IntCodeComputer(program_as_list('1002,4,3,4,33'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, program_as_list('1002,4,3,4,99'))

    # Op-code 5 is jump-if-true: if the first parameter is non-zero,
    # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    def test_op_code_5(self):
        computer = IntCodeComputer(program_as_list('1105,1,5,0,0,99'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 5)

    def test_op_code_5_false(self):
        computer = IntCodeComputer(program_as_list('1105,0,5,99,0,99'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 3)

    # Op-code 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the
    # second parameter. Otherwise, it does nothing
    def test_op_code_6(self):
        computer = IntCodeComputer(program_as_list('1106,0,5,0,0,99'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 5)

    # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
    # given by the third parameter.Otherwise, it stores 0.
    def test_op_code_7(self):
        computer = IntCodeComputer(program_as_list('1107,0,5,4,9'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, program_as_list('1107,0,5,4,1'))

    def test_op_code_7_false(self):
        computer = IntCodeComputer(program_as_list('1107,5,5,4,9'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, program_as_list('1107,5,5,4,0'))

    # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
    # given by the third parameter. Otherwise, it stores 0.
    def test_op_code_8(self):
        computer = IntCodeComputer(program_as_list('1108,5,5,4,9'))
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, program_as_list('1108,5,5,4,1'))


if __name__ == '__main__':
    unittest.main()
