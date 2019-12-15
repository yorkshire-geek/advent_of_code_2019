import unittest
from .exercise8 import return_layers
from .exercise8 import get_display_layer


class MyTestCase(unittest.TestCase):

    def test_get_display_layer(self):
        contents = '0222112222120000'
        test_layers = return_layers(contents, 2, 2)
        visible_layer = get_display_layer(test_layers, 2, 2)
        self.assertEqual(visible_layer, [['0', '1'], ['1', '0']])

    def test_return_layers(self) -> int:
        contents = '012345678901'
        test_layers = return_layers(contents, 2, 2)

        self.assertEqual(test_layers[0], [['0', '1'], ['2', '3']])
        self.assertEqual(test_layers[0][0][0], '0')
        self.assertEqual(test_layers[0][0][1], '1')
        self.assertEqual(test_layers[0][1][0], '2')
        self.assertEqual(test_layers[0][1][1], '3')
        self.assertEqual(test_layers[1][0][0], '4')


if __name__ == '__main__':
    unittest.main()
