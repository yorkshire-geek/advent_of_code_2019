from typing import List

_ADDITION = 1
_MULTIPLY = 2
_INPUT = 3
_OUTPUT = 4
_JUMP_IF_TRUE = 5
_JUMP_IF_FALSE = 6
_LESS_THAN = 7
_EQUAL_TO = 8
_EXIT = 99


def program_as_list(program: str):
    return [int(x) for x in program.split(',')]


class IntCodeComputer:
    def __init__(self, program_data: str, auto_mode=False):
        self.program_list = [int(x) for x in program_data.split(',')]
        self.instruction_pointer = 0
        self._auto_mode = auto_mode
        self._input_buffer = []

    def is_not_finished(self) -> bool:
        return self.program_list[self.instruction_pointer] != _EXIT

    def _get_current_with_offset(self, offset: int) -> int:
        return self.program_list[self.instruction_pointer + offset]

    def _get_position_or_immediate(self, offset: int, mask: str) -> int:
        if mask == "0":  # position
            return self._get_absolute(self.program_list[self.instruction_pointer + offset])
        elif mask == "1":  # immediate
            return self.program_list[self.instruction_pointer + offset]

    def _get_current(self) -> int:
        return self._get_current_with_offset(0)

    def _get_absolute(self, offset: int) -> int:
        return self.program_list[offset]

    def _get_current_as_string(self) -> str:
        return str(self.program_list[self.instruction_pointer])

    def add_input(self, input_int):
        self._input_buffer.append(input_int)

    def _get_input(self):
        return self._input_buffer.pop(0)

    def _set_output(self, output_value):
        self._output_buffer = output_value

    def get_output(self):
        return self._output_buffer

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
        result = result[0:len(result) - 2]
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
        elif (op_code % 10) == _JUMP_IF_TRUE or (op_code % 10) == _JUMP_IF_FALSE:
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
        if self._auto_mode:
            entered_value = self._get_input()
            print("auto-mode value entered: [%d]" % entered_value)
        else:
            entered_value = input("input a value: ")

        self.program_list[command["param1"]] = int(entered_value)
        self.instruction_pointer += 2

    def do_output(self, command):
        output_value = self.program_list[command["param1"]]
        print("output value: %d " % output_value)
        self._set_output(output_value)
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


if __name__ == "__main__":
    pass
    # test_1 = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    # test_2 = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    #
    # computer = IntCodeComputer(program_as_list(input_program))
    # computer.execute()
