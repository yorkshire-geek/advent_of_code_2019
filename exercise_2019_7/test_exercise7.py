import unittest
from .excercise7 import run_chained_computers_from_input


class MyTestCase(unittest.TestCase):

    def test_amp_circuit(self):
        output = run_chained_computers_from_input('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0])

        self.assertEqual(output, 43210)


if __name__ == '__main__':
    unittest.main()
