import unittest
from .exercise2 import FullData
from .exercise2 import OpCode
from .exercise2 import Jobber

input_data_test_1 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]


class MyTestCase(unittest.TestCase):

    def test_slice_is_addition(self):
        test_data = FullData(input_data_test_1)
        self.assertEqual(test_data.get_current_slice().op_code, OpCode.ADDITION)
        self.assertEqual(test_data.get_current_slice().param_noun, 9)
        self.assertEqual(test_data.get_current_slice().param_verb, 10)
        self.assertEqual(test_data.get_current_slice().param_address, 3)
        # print(test)
        #self.assertEqual(test_data.get_current_slice(), Jobber(1, 9, 10, 3))


if __name__ == '__main__':
    unittest.main()
