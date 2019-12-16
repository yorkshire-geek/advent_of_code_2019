import unittest
from .intcomputer import IntCodeComputer
from .intcomputer import program_as_list


class MyTestCase(unittest.TestCase):
    def test_program_as_list(self):
        program_list = program_as_list('1002,4,3,4,33')
        self.assertEqual(len(program_list), 5)

    def test_get_next_op_code(self):
        computer = IntCodeComputer('99,4,3,4,33')
        self.assertEqual(computer.is_not_finished(), False)

    def test_simple_add_parse_frame(self):
        computer = IntCodeComputer('1,9,10,3,2,3,11,0,99,30,40,50')
        frame = computer.parse_frame()
        self.assertEqual(frame, {"op_code": 1, "param1": 30, "param2": 40, "address": 3})

    def test_run_command_add(self):
        computer = IntCodeComputer('1,9,10,3,2,3,11,0,99,30,40,50')
        computer.run_command(computer.parse_frame())
        self.assertEqual(computer.program_list, [1,9,10,70,2,3,11,0,99,30,40,50])

    def test_run_command_add_multiply(self):
        computer = IntCodeComputer('1,9,10,3,2,3,11,0,99,30,40,50')
        computer.run_command(computer.parse_frame())  # add
        computer.run_command(computer.parse_frame())  # multiply
        self.assertEqual(computer.program_list, [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_execute_computer(self):
        computer = IntCodeComputer('1,9,10,3,2,3,11,0,99,30,40,50')
        computer.execute()
        self.assertEqual(computer.program_list, [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_multiply_with_mask(self):
        computer = IntCodeComputer('1002,4,3,4,33')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, [1002,4,3,4,99])

    def test_add_with_mask(self):
        computer = IntCodeComputer('1001, 5, -4, 5, 99, 0')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, [1001, 5, -4, 5, 99, -4])

    # Op-code 5 is jump-if-true: if the first parameter is non-zero,
    # it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    def test_op_code_5(self):
        computer = IntCodeComputer('1105,1,5,0,0,99')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 5)

    def test_op_code_5_false(self):
        computer = IntCodeComputer('1105,0,5,99,0,99')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 3)

    # Op-code 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the
    # second parameter. Otherwise, it does nothing
    def test_op_code_6(self):
        computer = IntCodeComputer('1106,0,5,0,0,99')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.instruction_pointer, 5)

    # Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
    # given by the third parameter.Otherwise, it stores 0.
    def test_op_code_7(self):
        computer = IntCodeComputer('1107,0,5,4,9')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, [1107,0,5,4,1])

    def test_op_code_7_false(self):
        computer = IntCodeComputer('1107,5,5,4,9')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, [1107,5,5,4,0])

    # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
    # given by the third parameter. Otherwise, it stores 0.
    def test_op_code_8(self):
        computer = IntCodeComputer('1108,5,5,4,9')
        frame = computer.parse_frame()
        computer.run_command(frame)
        self.assertEqual(computer.program_list, [1108,5,5,4,1])

    def test_auto_mode_add_input(self):
        computer = IntCodeComputer('99', True)
        computer.add_input(1)
        computer.add_input(2)
        self.assertEqual(computer._input_buffer, [1, 2])
        self.assertEqual(computer._get_input(), 1)
        self.assertEqual(computer._input_buffer, [2])

    def test_auto_mode_get_output(self):
        computer = IntCodeComputer('99', True)
        computer._set_output(1)
        self.assertEqual(computer.get_output(), 1)
        computer._set_output(2)
        self.assertEqual(computer.get_output(), 2)

    def test_suspended_flag(self):
        computer = IntCodeComputer('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,'
                                   '0,0,5', True)
        self.assertEqual(computer.suspended, False)
        computer.execute()
        self.assertEqual(computer.suspended, True)

    def test_exit_flag(self):
        computer = IntCodeComputer('99')
        self.assertEqual(computer.finished, False)
        computer.execute()
        self.assertEqual(computer.finished, True)

    def test_equality_in_auto_mode(self):
        #  3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8;
        #  output 1 (if it is) or 0 (if it is not).
        #
        computer = IntCodeComputer('3,9,8,9,10,9,4,9,99,-1,8', True)
        computer.add_input(1)
        computer.execute()
        self.assertEqual(computer.get_output(), 0)

        computer = IntCodeComputer('3,9,8,9,10,9,4,9,99,-1,8', True)
        computer.add_input(8)
        computer.execute()
        self.assertEqual(computer.get_output(), 1)

    def test_op_code_9(self):
        input_program = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
        computer = IntCodeComputer(input_program, True, True)
        computer.execute()
        self.assertEqual(computer._output_buffer_history, program_as_list(input_program))

    def test_op_code_9_109_209(self):
        input_program = '9,1,109,2,209,2,99'
        computer = IntCodeComputer(input_program, True, False)
        computer.execute()
        self.assertEqual(computer.relative_base, 5)

    def test_output_large_number(self):
        computer = IntCodeComputer('1102,34915192,34915192,7,4,7,99,0', True)
        computer.execute()
        self.assertEqual(computer.get_output(), 1219070632396864)

    def test_large_output(self):
        computer = IntCodeComputer('104,1125899906842624,99', True)
        computer.execute()
        self.assertEqual(computer.get_output(), 1125899906842624)

    def test_op_code_203(self):
        computer = IntCodeComputer('109,10,203,0,204,0,99', True, True)
        computer.add_input(100)
        computer.execute()
        self.assertEqual(computer.get_output(), 100)

    # def test_op_code_2106(self):
    #     computer = IntCodeComputer('2106, 5, 203, 1, 99, 0, 0', True)
    #     computer.add_input(1)
    #     computer.execute()
    #     self.assertEqual(computer.program_list, [109, 5, 203, 1, 99, 0, 1])


if __name__ == '__main__':
    unittest.main()
