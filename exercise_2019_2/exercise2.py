from typing import List
from enum import Enum

input_data = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,19,23,2,23,6,27,2,6,27,31,2,13,31,35,1,10,35,39,2,39,13,' \
             '43,1,43,13,47,1,6,47,51,1,10,51,55,2,55,6,59,1,5,59,63,2,9,63,67,1,6,67,71,2,9,71,75,1,6,75,79,2,79,13,' \
             '83,1,83,10,87,1,13,87,91,1,91,10,95,2,9,95,99,1,5,99,103,2,10,103,107,1,107,2,111,1,111,5,0,99,2,14,0,0 '
# input_data_test_1 = '1,9,10,3,2,3,11,0,99,30,40,50'
input_list = [int(x) for x in input_data.split(',')]


class OpCode(Enum):
    ADDITION = 1
    MULTIPLY = 2
    EXIT = 99


class Jobber:
    def __init__(self):
        self.op_code = None
        self.param_noun = None
        self.param_verb = None
        self.param_address = None


class FullData:
    def __init__(self, list_data: List[int]):
        self.list_data = list_data
        self.offset = 0

    def get_current_slice(self) -> Jobber:
        jobber = Jobber()
        jobber.op_code = OpCode(self.list_data[self.offset])
        if jobber.op_code is not OpCode.EXIT:
            jobber.param_noun = self.list_data[self.offset + 1]
            jobber.param_verb = self.list_data[self.offset + 2]
            jobber.param_address = self.list_data[self.offset + 3]

        return jobber


class Slice:
    def __init__(self, offset: int):
        self.offset = offset
        self.op_code = input_list[offset]
        self.param_noun = input_list[offset + 1] if self.offset + 1 < len(input_list) else -1
        self.param_verb = input_list[offset + 2] if self.offset + 2 < len(input_list) else -1
        self.address = input_list[offset + 3] if self.offset + 3 < len(input_list) else -1

    def process_it(self) -> bool:
        # todo - add switch
        result = 0
        if self.op_code == 1:
            result = input_list[self.param_noun] + input_list[self.param_verb]
        elif self.op_code == 2:
            result = input_list[self.param_noun] * input_list[self.param_verb]
        elif self.op_code == 99:
            if input_list[0] == 19690720:
                print("found it")
                print("output: %d noun %d verb %d" % (input_list[0], noun, verb))
            return True
        else:
            print("error: unexpected op-code found %d" % self.op_code)
            return True

        input_list[self.address] = result
        return False


if __name__ == "__main__":
    # input_list[1] = 12
    # input_list[2] = 2

    for noun in range(0, 100):
        for verb in range(0, 100):

            input_list = [int(x) for x in input_data.split(',')]
            input_list[1] = noun
            input_list[2] = verb

            finished = False
            index = 0
            while (index < len(input_list)) and not finished:
                slice_input = Slice(index)
                finished = slice_input.process_it()
                index += 4

            # print("output: %d noun %d verb %d" % (input_list[0], noun, verb))

