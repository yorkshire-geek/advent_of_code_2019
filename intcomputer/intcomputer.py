from typing import List

_ADDITION = 1
_MULTIPLY = 2
_INPUT = 3
_INPUT_203 = 203
_OUTPUT = 4
_OUTPUT_104 = 104
_OUTPUT_204 = 204
_JUMP_IF_TRUE = 5
_JUMP_IF_FALSE = 6
_LESS_THAN = 7
_EQUAL_TO = 8
_RELATIVE_BASE = 9
_RELATIVE_BASE_109 = 109
_RELATIVE_BASE_209 = 209
_EXIT = 99


def program_as_list(program: str):
    return [int(x) for x in program.split(',')]


class IntCodeComputer:

    # class CommandAdd:
    #     def run(self):
    #        self.
    #         pass

    def __init__(self, program_data: str, auto_mode=False, grow_mode=False):
        self.program_list = [int(x) for x in program_data.split(',')]
        self.instruction_pointer = 0
        self._auto_mode = auto_mode
        self._grow_mode = grow_mode
        self._input_buffer = []
        self.finished = False
        self.debug = False
        self.suspended = False
        self.debug_name = ""
        self.relative_base = 0
        self._output_buffer = None
        self._output_buffer_history = []
        if grow_mode:
            self.program_list.extend([0] * (150 * len(self.program_list)))

    def _get(self, offset: int) -> int:
        return self.program_list[offset]

    def _get_from_cursor(self, offset: int) -> int:
        return self.program_list[self.instruction_pointer + offset]

    def _get_value_from_relative_base(self, offset: int) -> int:
        return self._get(self.relative_base + self._get_from_cursor(offset))

    def _get_address_of_relative_base(self, offset: int) -> int:
        return self.relative_base + self._get_from_cursor(offset)

    def _get_input(self):
        return self._input_buffer.pop(0)

    def _set_output(self, output_value):
        self._output_buffer_history.append(output_value)
        self._output_buffer = output_value

    def is_not_finished(self) -> bool:
        return self.program_list[self.instruction_pointer] != _EXIT

    def add_input(self, input_int):
        self._input_buffer.append(input_int)

    def get_output(self):
        return self._output_buffer


    @staticmethod
    def _parse_op_code_mask(op_code: int) -> str:
        result = str(op_code)
        if len(result) > 5:
            print("Big op-code found: %d " % op_code)
            exit(-1)
        if len(result) == 1:
            return "000"
        result = result[0:len(result) - 2]
        result = result.rjust(3, "0")
        return result

    def _get_read_address(self, offset: int, mask: str) -> int:
        if mask == "0":    # position
            return self._get(self._get_from_cursor(offset))
        elif mask == "1":  # immediate
            return self._get_from_cursor(offset)
        elif mask == "2":  # relative
            return self._get_value_from_relative_base(offset)

    def _get_write_address(self, offset, mask: str):
        if mask == "0":
            return self._get_from_cursor(offset)
        elif mask == "2":
            return self.relative_base + self._get_from_cursor(offset)
        else:
            print("Unexpected write address mask [%s] at instruction pointer [%d]", offset, self.instruction_pointer)
            exit(-1)

    def parse_frame(self):
        op_code = self._get_from_cursor(0)

        # if (op_code % 10) == _ADDITION or (op_code % 10) == _MULTIPLY:
        if op_code in (22201, 21101, 21201, 2101, 1201, 1101, 1001, 101, 1, 21202, 22102, 21102, 2102, 1202, 1102, 1002, 102, 2):
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "param1": self._get_read_address(1, op_code_mask[2]),
                "param2": self._get_read_address(2, op_code_mask[1]),
                "address": self._get_write_address(3, op_code_mask[0])
            }
        elif (op_code % 10) == _INPUT:
            result = {"op_code": _INPUT}
            if op_code == _INPUT:
                result["address"] = self._get_from_cursor(1)
            elif op_code == _INPUT_203:
                result["address"] = self._get_address_of_relative_base(1)
            else:
                print("unexpected op-code found [%d]" % op_code)
                exit(-1)

        elif (op_code % 10) == _OUTPUT:
            result = {"op_code": _OUTPUT}
            if op_code == _OUTPUT:
                result["address"] = self._get_from_cursor(1)
            elif op_code == _OUTPUT_204:
                result["address"] = self._get_address_of_relative_base(1)
            elif op_code == _OUTPUT_104:
                result["value"] = self._get_from_cursor(1)
            else:
                print("unexpected op-code found [%d]" % op_code)
                exit(-1)

        # elif (op_code % 10) == _JUMP_IF_TRUE or (op_code % 10) == _JUMP_IF_FALSE:
        elif op_code in (2105, 1205, 1105, 1005, 105, 5, 2106, 1206, 1106, 1006, 106, 6):
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "param1": self._get_read_address(1, op_code_mask[2]),
                "address": self._get_read_address(2, op_code_mask[1])
            }
        elif (op_code % 10) == _LESS_THAN or (op_code % 10) == _EQUAL_TO:
            op_code_mask = self._parse_op_code_mask(op_code)
            result = {
                "op_code": op_code % 10,
                "param1": self._get_read_address(1, op_code_mask[2]),
                "param2": self._get_read_address(2, op_code_mask[1]),
                "address": self._get_write_address(3, op_code_mask[0])
            }
        elif (op_code % 10) == _RELATIVE_BASE:
            result = {'op_code': (op_code % 10) }
            if op_code == _RELATIVE_BASE:
                result['offset'] = self.program_list[self._get_from_cursor(1)]
            if op_code == _RELATIVE_BASE_109:
                result['offset'] = self._get_from_cursor(1)
            if op_code == _RELATIVE_BASE_209:
                result['offset'] = self.program_list[self.relative_base + self._get_from_cursor(1)]
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
        elif command["op_code"] == _RELATIVE_BASE:
            self.do_relative_base(command)
        else:
            print("unexpected command op_code [%s]" % command)
            exit(-1)

    def do_addition(self, command):
        self.program_list[command["address"]] = command["param1"] + command["param2"]
        self.instruction_pointer += 4

    def do_multiply(self, command):
        self.program_list[command["address"]] = command["param1"] * command["param2"]
        self.instruction_pointer += 4

    def do_input(self, command):

        if self._auto_mode and not self._input_buffer:  # input buffer empty, go into suspend mode.
            self.suspended = True
            return

        entered_value = self._get_input() if self._auto_mode else int(input("input a value: "))

        self.program_list[command["address"]] = entered_value
        self.instruction_pointer += 2

    def do_output(self, command):
        if 'value' in command:
            output_value = command['value']
        elif 'address' in command:
            output_value = self.program_list[command["address"]]
        self._set_output(output_value)

        self.instruction_pointer += 2

        if not self._auto_mode:
            print(output_value)

    def do_jump_if_true(self, command):
        if command["param1"]:
            self.instruction_pointer = command["address"]
        else:
            self.instruction_pointer += 3

    def do_jump_if_false(self, command):  # refactor to use do_jump_if_false ? DRY or WET??
        if command["param1"] == 0:
            self.instruction_pointer = command["address"]
        else:
            self.instruction_pointer += 3

    def _set(self, offset: int, value: int ):
        self.program_list[offset] = value

    def do_less_than(self, command):
        value = 1 if command["param1"] < command["param2"] else 0
        self._set(command["address"], value)
        self.instruction_pointer += 4

    def do_equal_to(self, command):
        value = 1 if command["param1"] == command["param2"] else 0
        self._set(command["address"], value)
        self.instruction_pointer += 4

    def do_relative_base(self, command):
        self.relative_base += command["offset"]

        self.instruction_pointer += 2

    def resume(self):
        self.suspended = False
        self.execute()

    def execute(self):
        if self.debug:
            print("start: " + self.debug_name + str(self.program_list))
            print("buffer:" + str(self._input_buffer))

        while self.is_not_finished() and not self.suspended:
            frame = self.parse_frame()
            self.run_command(frame)

        if not self.suspended:
            self.finished = True

        if self.debug:
            print("End: " + self.debug_name + str(self.program_list))


if __name__ == "__main__":
    pass
    # test_1 = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    # test_2 = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    #
    # computer = IntCodeComputer(program_as_list(input_program))
    # computer.execute()
