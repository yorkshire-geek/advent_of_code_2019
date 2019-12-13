import unittest
from .excercise7 import run_chained_computers_from_input
from .excercise7 import run_chained_computers_with_feedback


class MyTestCase(unittest.TestCase):

    def test_amp_circuit(self):
        output = run_chained_computers_from_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0])
        self.assertEqual(output, 43210)

    # Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
    #
    # 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    #
    def test_feedback_model(self):
        input_program = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
        output = run_chained_computers_with_feedback(input_program, [9, 8, 7, 6, 5])
        print(output)
        self.assertEqual(output, 139629729)

    # Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
    #
    # 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    # -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    # 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
    #
    def test_feedback_model_2(self):
        input_program = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
        output = run_chained_computers_with_feedback(input_program, [9, 7, 8, 5, 6])
        print(output)
        self.assertEqual(output, 18216)


if __name__ == '__main__':
    unittest.main()
