from utils.objectmother import ObjectMother
from utils.datawrapper import DataWrapper


def fuel_calculator(fuel: int) -> int:
    return (fuel // 3) - 2


def get_fuel_for_fuel(initial_mass: int) -> int:
    mass = initial_mass
    fuel = 0

    while fuel_calculator(mass) > 0:
        fuel += fuel_calculator(mass)
        mass = fuel_calculator(mass)

    return fuel


class Ex1DataWrapper (DataWrapper):

    @staticmethod
    def factory(data):
        return Ex1DataWrapper(data)

    def get_mass(self) -> int:
        return int(self.data)

    def get_fuel(self) -> int:
        return fuel_calculator(self.get_mass())


if __name__ == "__main__":
    mother = ObjectMother("input.txt")
    list_of_data = mother.return_list(Ex1DataWrapper.factory)

    total_fuel = 0
    for item in list_of_data:
        total_fuel += item.get_fuel()
        total_fuel += get_fuel_for_fuel(item.get_fuel())

    print("---")
    print("Total Fuel expected [5269882] found [%d]" % total_fuel)


# answer to 1 = 3515171
# answer to 2 = 5269882
# For a mass of 1969, the fuel required is 654.
# For a mass of 1969 total fuel = 966
# For a mass of 100756, the fuel required is 33583.
