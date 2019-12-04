import unittest
from .exercise_2019_3 import split_commands
from .exercise_2019_3 import command_builder
from .exercise_2019_3 import plot_route
from .exercise_2019_3 import plot_command

input_1 = 'R8,U5,L5,D3'
input_2 = 'U7,R6,D4,L4'


class MyTestCase(unittest.TestCase):
    def test_splits_command(self):
        list_commands = split_commands(input_1)
        self.assertEqual(len(list_commands), 4)

    def test_first_command(self):
        command_list = command_builder(split_commands(input_1))
        command = command_list[0]
        self.assertEqual(command["command"], 'R')
        self.assertEqual(command['param'], 8)

        command = command_list[2]
        self.assertEqual(command["command"], 'L')
        self.assertEqual(command['param'], 5)

    def test_command_to_plot_R(self):
        command = command_builder(split_commands('R4'))[0]
        route, x, y = plot_command(command, 0, 0)
        self.assertEqual([(1, 0), (2, 0), (3, 0), (4, 0)], route)

    def test_command_to_plot_R(self):
        command = command_builder(split_commands('L4'))[0]
        route, x, y = plot_command(command, 0, 0)
        self.assertEqual(route, [(-1, 0), (-2, 0), (-3, 0), (-4, 0)])

    def test_command_to_plot_U(self):
        command = command_builder(split_commands('U2'))[0]
        route, x, y = plot_command(command, 0, 0)
        self.assertEqual(route, [(0, 1), (0, 2)])

    def test_command_to_plot_D(self):
        command = command_builder(split_commands('D2'))[0]
        route, x, y = plot_command(command, 0, 0)
        self.assertEqual(route, [(0, -1), (0, -2)])

    def test_plot_route(self):
        route_1 = plot_route(command_builder(split_commands(input_1)))
        route_2 = plot_route(command_builder(split_commands(input_2)))
        # intersection = route_1.intersection(route_2)
        #
        # my_intersection
        self.assertEqual({(3, 3), (6, 5)}, my_intersection(route_1, route_2))

if __name__ == '__main__':
    unittest.main()
