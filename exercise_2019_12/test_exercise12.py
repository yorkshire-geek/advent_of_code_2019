import unittest
from .exercise12 import Planet
from .exercise12 import System


input_data = "<x=-1, y=0, z=2>\n" \
        "<x=2, y=-10, z=-7>\n" \
        "<x=4, y=-8, z=8>\n" \
        "<x=3, y=5, z=-1>"


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.system = None

    def setup_test_data(self):
        self.system = System()
        for planet_data in input_data.split('\n'):
            planet = Planet(planet_data)
            self.system.add_planet(planet)

    def test_adding_planet_from_input(self):
        planet_1_data = input_data.split('\n')[0]
        planet = Planet(planet_1_data)

        self.assertEqual({'x': -1, 'y': 0, 'z': 2}, planet._position)
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, planet._velocity)

    def test_adding_planets_to_system(self):
        self.setup_test_data()
        self.assertEqual(4, len(self.system.planets))

    def test_get_combinations(self):
        self.setup_test_data()
        self.assertEqual([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], self.system._get_combinations())

    def test_jobber(self):
        final_state = False
        self.setup_test_data()
        while not final_state:
            final_state = self.system.do_step()
        self.system.show_data()


if __name__ == '__main__':
    unittest.main()