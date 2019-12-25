from itertools import combinations
from utils.utils import read_file

class Planet:
    def _setup(self):
        self.position['x'] = int(self.starting_data.split(',')[0].split('=')[1])
        self.position['y'] = int(self.starting_data.split(',')[1].split('=')[1])
        self.position['z'] = int(self.starting_data.split('=')[3].split('>')[0])
        self.initial_position = self.position.copy()
        self.initial_velocity = self.velocity.copy()

    def __init__(self, starting_data: str):
        self.starting_data = starting_data
        self.position = {}
        self.velocity = {'x': 0, 'y': 0, 'z': 0}
        self._setup()

    def __repr__(self):
        return "Position %s Velocity %s Energy %d" % (self.position, self.velocity, self.get_total_energy())

    def apply_velocity_to_position(self):
        self.position['x'] += self.velocity['x']
        self.position['y'] += self.velocity['y']
        self.position['z'] += self.velocity['z']

    def get_total_energy(self):
        return int(abs(self.position['x']) + abs(self.position['y']) + abs(self.position['z'])) * \
               (abs(self.velocity['x']) + abs(self.velocity['y']) + abs(self.velocity['z']))


class System:
    def __init__(self):
        self.planets = []
        self.count = 0
        self.found_x = False
        self.found_y = False
        self.found_z = False

    def add_planet(self, planet: Planet):
        self.planets.append(planet)

    def _get_combinations(self):
        return list(combinations(range(len(self.planets)), 2))

    def _apply_gravity_to_velocity(self):
        for combo in self._get_combinations():
            self.modify_velocity(self.planets[combo[0]], self.planets[combo[1]])

    def _apply_velocity_to_position(self):
        for planet in self.planets:
            planet.apply_velocity_to_position()

    @staticmethod
    def modify_velocity(planet1 : Planet, planet2: Planet):
        for key in ('x', 'y', 'z'):
            if planet1.position[key] > planet2.position[key]:
                planet1.velocity[key] -= 1
                planet2.velocity[key] += 1
            elif planet1.position[key] < planet2.position[key]:
                planet1.velocity[key] += 1
                planet2.velocity[key] -= 1

    def initial_state_reached(self):

        if self.planets[0].initial_position['x'] == self.planets[0].position['x'] and \
               self.planets[1].initial_position['x'] == self.planets[1].position['x'] and \
               self.planets[2].initial_position['x'] == self.planets[2].position['x'] and \
               self.planets[3].initial_position['x'] == self.planets[3].position['x']:
            print("x repeats: [%d]" % self.count)
            self.found_x = True

        if self.planets[0].initial_position['y'] == self.planets[0].position['y'] and \
               self.planets[1].initial_position['y'] == self.planets[1].position['y'] and \
               self.planets[2].initial_position['y'] == self.planets[2].position['y'] and \
               self.planets[3].initial_position['y'] == self.planets[3].position['y']:
            print("y repeats: [%d]" % self.count)
            self.found_y = True

        if self.planets[0].initial_position['z'] == self.planets[0].position['z'] and \
                self.planets[1].initial_position['z'] == self.planets[1].position['z'] and \
                self.planets[2].initial_position['z'] == self.planets[2].position['z'] and \
                self.planets[3].initial_position['z'] == self.planets[3].position['z']:
            print("z repeats: [%d]" % self.count)
            self.found_z = True

        return self.found_x and self.found_y and self.found_z

    def do_step(self):
        self.count += 1
        self._apply_gravity_to_velocity()
        self._apply_velocity_to_position()

        return self.initial_state_reached()

    def show_data(self):
        print("Cycle [%d]" % self.count)
        print(self.planets[0])
        print(self.planets[1])
        print(self.planets[2])
        print(self.planets[3])
        print("sum of total energy %d" % (self.planets[0].get_total_energy() + self.planets[1].get_total_energy() +
              self.planets[2].get_total_energy() + self.planets[3].get_total_energy()))


if __name__ == '__main__':
    # Exercise 1
    #
    system = System()
    for planet_data in read_file().split('\n'):
        system.add_planet(Planet(planet_data))

    # for n in range(1000):
    #     system.do_step()
    # system.show_data()

    final_state = False
    while not final_state:
        final_state = system.do_step()

    system.show_data()


    # LCM x repeats 268295 y repeats 231614 z repeats 23326
    # LCM = 362,375,881,472,136



