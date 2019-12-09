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
        self.assertEqual(frame, {"op_code": 1, "op_code_mask": "000", "param1": 30, "param2": 40, "param3": 3})

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

    def test_amp_circuit(self):
        # input 4, 3, 2, 1, 0

        computer_a = IntCodeComputer('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', True)
        computer_a.add_input(4)
        computer_a.add_input(0)
        computer_a.execute()

        computer_b = IntCodeComputer('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', True)
        computer_b.add_input(3)
        computer_b.add_input(computer_a.get_output())
        computer_b.execute()

        computer_c = IntCodeComputer('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', True)
        computer_c.add_input(2)
        computer_c.add_input(computer_b.get_output())
        computer_c.execute()

        computer_d = IntCodeComputer('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', True)
        computer_d.add_input(1)
        computer_d.add_input(computer_c.get_output())
        computer_d.execute()

        computer_e = IntCodeComputer('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', True)
        computer_e.add_input(0)
        computer_e.add_input(computer_d.get_output())
        computer_e.execute()

        self.assertEqual(computer_e.get_output(), 43210)




if __name__ == '__main__':
    unittest.main()
