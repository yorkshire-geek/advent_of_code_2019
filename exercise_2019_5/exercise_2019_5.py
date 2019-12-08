from enum import Enum
from typing import List

_ADDITION = 1
_MULTIPLY = 2
_INPUT = 3  # 1 parameter: integer as input and saves it to the position given by its only parameter.
# For example, the instruction 3,50 would take an input value and store it at address 50.
_OUTPUT = 4  # 1 parameter. For example, the instruction 4,50 would output the value at address 50.
_JUMP_IF_TRUE = 5
_JUMP_IF_FALSE = 6
_LESS_THAN = 7
_EQUAL_TO = 8
_EXIT = 99


instruction_pointer = 0


def program_as_list(program: str):
    return [int(x) for x in program.split(',')]


class IntCodeComputer:
    def __init__(self, program_list: List[str]):
        self.program_list = program_list
        self.instruction_pointer = 0

    def is_not_finished(self) -> bool:
        return self.program_list[self.instruction_pointer] != _EXIT

    def _get_current_with_offset(self, offset: int) -> int:
        return self.program_list[self.instruction_pointer + offset]

    def _get_position_or_immediate(self, offset: int, mask: str) -> int:
        if mask == "0":    # position
            return self._get_absolute(self.program_list[self.instruction_pointer + offset])
        elif mask == "1":  # immediate
            return self.program_list[self.instruction_pointer + offset]

    def _get_current(self) -> int:
        return self._get_current_with_offset(0)

    def _get_absolute(self, offset: int) -> int:
        return self.program_list[offset]

    def _get_current_as_string(self) -> str:
        return str(self.program_list[self.instruction_pointer])

    @staticmethod
    def _parse_op_code(op_code: int) -> int:
        return op_code % 10

    @staticmethod
    def _parse_op_code_mask(op_code: int) -> str:
        result = str(op_code)
        if len(result) > 4:
            print("Big op-code found: %d " % op_code)
            exit(-1)
        if len(result) == 1:
            return "000"
        result = result[0:len(result)-2]
        result = result.rjust(3, "0")
        return result

    def parse_frame(self):
        op_code = self._get_current()

        if (op_code % 10) == _ADDITION or (op_code % 10) == _MULTIPLY:
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "op_code_mask": op_code_mask,
                "param1": self._get_position_or_immediate(1, op_code_mask[2]),
                "param2": self._get_position_or_immediate(2, op_code_mask[1]),
                "param3": self._get_current_with_offset(3),
            }
        elif op_code == _INPUT:
            result = {
                "op_code": _INPUT,
                "op_code_mask": "",
                "param1": self._get_current_with_offset(1),
            }
        elif op_code in {_OUTPUT, 104}:
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": _OUTPUT,
                "op_code_mask": op_code_mask,
                "param1": self._get_current_with_offset(1)
            }
        elif (op_code % 10) == _JUMP_IF_TRUE or (op_code % 10) == _JUMP_IF_FALSE :
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "op_code_mask": op_code_mask,
                "param1": self._get_position_or_immediate(1, op_code_mask[2]),
                "param2": self._get_position_or_immediate(2, op_code_mask[1])
            }
        elif (op_code % 10) == _LESS_THAN or (op_code % 10) == _EQUAL_TO:
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "op_code_mask": op_code_mask,
                "param1": self._get_position_or_immediate(1, op_code_mask[2]),
                "param2": self._get_position_or_immediate(2, op_code_mask[1]),
                "param3": self._get_current_with_offset(3)
            }
        else:
            print("unexpected op_code [%d] ptr = [%d]" % (op_code, self.instruction_pointer))
            exit(-1)

        return result

    def run_command(self, command: dict):
        if command["op_code"] == _ADDITION:
            self.do_addition(command)
        elif command["op_code"] == _MULTIPLY:
            self.do_multiply(command)
        elif command["op_code"] == _INPUT:
            self.do_input(command)
        elif command["op_code"] == _OUTPUT:
            self.do_output(command)
        elif command["op_code"] == _JUMP_IF_TRUE:
            self.do_jump_if_true(command)
        elif command["op_code"] == _JUMP_IF_FALSE:
            self.do_jump_if_false(command)
        elif command["op_code"] == _LESS_THAN:
            self.do_less_than(command)
        elif command["op_code"] == _EQUAL_TO:
            self.do_equal_to(command)
        else:
            print("unexpected command op_code [%s]" % command)
            exit(-1)

    def do_addition(self, command):
        self.program_list[command["param3"]] = command["param1"] + command["param2"]
        self.instruction_pointer += 4

    def do_multiply(self, command):
        self.program_list[command["param3"]] = command["param1"] * command["param2"]
        self.instruction_pointer += 4

    def do_input(self, command):
        entered_value = input("input a value: ")
        self.program_list[command["param1"]] = int(entered_value)
        self.instruction_pointer += 2

    def do_output(self, command):
        print("output value: %d " % self.program_list[command["param1"]])
        self.instruction_pointer += 2

    def do_jump_if_true(self, command):
        if command["param1"]:
            self.instruction_pointer = command["param2"]
        else:
            self.instruction_pointer += 3

    def do_jump_if_false(self, command):  # refactor to use do_jump_if_false ? DRY or WET??
        if command["param1"] == 0:
            self.instruction_pointer = command["param2"]
        else:
            self.instruction_pointer += 3

    def do_less_than(self, command):
        if command["param1"] < command["param2"]:  # less than = true
            self.program_list[command["param3"]] = 1
        else:
            self.program_list[command["param3"]] = 0

        self.instruction_pointer += 4

    def do_equal_to(self, command):
        if command["param1"] == command["param2"]:
            self.program_list[command["param3"]] = 1
        else:
            self.program_list[command["param3"]] = 0

        self.instruction_pointer += 4

    def execute(self):
        while self.is_not_finished():
            frame = self.parse_frame()
            self.run_command(frame)

        print("finished ---")


input_program = '3,225,1,225,6,6,1100,1,238,225,104,0,1002,92,42,224,1001,224,-3444,224,4,224,102,8,223,223,101,4,' \
                '224,224,1,224,223,223,1102,24,81,225,1101,89,36,224,101,-125,224,224,4,224,102,8,223,223,101,5,224,' \
                '224,1,224,223,223,2,118,191,224,101,-880,224,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,' \
                '1102,68,94,225,1101,85,91,225,1102,91,82,225,1102,85,77,224,101,-6545,224,224,4,224,1002,223,8,223,' \
                '101,7,224,224,1,223,224,223,1101,84,20,225,102,41,36,224,101,-3321,224,224,4,224,1002,223,8,223,101,' \
                '7,224,224,1,223,224,223,1,188,88,224,101,-183,224,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,' \
                '223,1001,84,43,224,1001,224,-137,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1102,71,92,225,' \
                '1101,44,50,225,1102,29,47,225,101,7,195,224,101,-36,224,224,4,224,102,8,223,223,101,6,224,224,1,223,' \
                '224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,' \
                '99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,' \
                '1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,' \
                '99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,677,224,1002,223,2,223,1006,224,329,' \
                '1001,223,1,223,1108,226,677,224,102,2,223,223,1006,224,344,101,1,223,223,1107,226,226,224,1002,223,' \
                '2,223,1006,224,359,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,374,1001,223,1,223,1107,677,' \
                '226,224,102,2,223,223,1005,224,389,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,404,1001,' \
                '223,1,223,108,677,677,224,102,2,223,223,1005,224,419,1001,223,1,223,1107,226,677,224,102,2,223,223,' \
                '1006,224,434,101,1,223,223,1008,226,226,224,1002,223,2,223,1006,224,449,1001,223,1,223,107,226,226,' \
                '224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,479,1001,223,' \
                '1,223,1108,226,226,224,102,2,223,223,1006,224,494,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,' \
                '224,509,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,524,101,1,223,223,1008,677,226,224,102,' \
                '2,223,223,1005,224,539,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,554,1001,223,1,223,' \
                '1108,677,226,224,102,2,223,223,1005,224,569,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,' \
                '584,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,108,226,677,224,1002,' \
                '223,2,223,1006,224,614,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,629,101,1,223,223,7,' \
                '677,677,224,102,2,223,223,1005,224,644,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,659,' \
                '1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226 '

if __name__ == "__main__":

    test_1 = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    test_2 = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'

    computer = IntCodeComputer(program_as_list(input_program))
    computer.execute()

    # input 1 = 9961446
