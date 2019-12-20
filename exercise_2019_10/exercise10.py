import math


class MeteorStation:
    def __init__(self, list_of_lines: [], debug = False):
        self.raw_data = list_of_lines
        self.width = len(list_of_lines[0])
        self.height = len(list_of_lines)
        self.map_of_space = None
        self.debug = debug
        self.base = None
        self.angle = -90.0
        self.meteors = None

    def get_map_of_space(self) -> []:

        if self.map_of_space is None:
            self.map_of_space = []
            for y in range(self.height):
                self.map_of_space.append([])
                for x in range(self.width):
                    self.map_of_space[y].append(self.raw_data[y][x])

        return self.map_of_space
        # [[int(i) for i in line.split()] for line in data]

    @staticmethod
    def get_angle(x1, x2, y1, y2) -> int:
        degrees = round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 2)

        return degrees

    def get_meteor_angles(self, origin):
        result = dict()
        for y in range(self.height):
            for x in range(self.width):
                if origin != {'y': y, 'x': x}:
                    if self.get_map_of_space()[y][x] == "#":
                        angle = self.get_angle(origin['x'], x, origin['y'], y)

                        if angle in result:
                            result[angle].append((y, x))
                        else:
                            result[angle] = [(y, x)]
        if self.debug:
            print("origin [%s] => %s" % (str(origin), str(result)))
        return result

    def get_bases(self):
        max_result = (0, ())
        for y in range(self.height):
            for x in range(self.width):
                if self.get_map_of_space()[y][x] == "#":
                    found = len(self.get_meteor_angles({'y': y, 'x': x}))
                    if found > max_result[0]:
                        max_result = (found, (y, x))

        return max_result

    def set_base(self, base_location: ()):
        self.base = base_location
        self.meteors = self.get_meteor_angles({'y': self.base[0], 'x': self.base[1]})
        self.angle = -90.0

    def fire_gun_and_remove_asteroid(self):

        keys = sorted(self.meteors.keys())
        index = keys.index(self.angle)
        try:
            next_key = keys[index+1]
        except IndexError:
            next_key = keys[0]

        # print("item to delete: " + str(self.meteors[keys[index]]))
        # print("next key: " + str(next_key))

        result = self.meteors[keys[index]].pop(-1)
        # print(value)
        self.angle = next_key
        if not self.meteors[keys[index]]:   # empty list
            self.meteors.pop(keys[index])
            # print('deleting')

        return result


def read_file():
    input_file = open("input.txt", "r")
    if input_file.mode == 'r':
        return input_file.read()


if __name__ == '__main__':

    # Exercise 1
    #
    meteor_station = MeteorStation(read_file().split())
    best_base = meteor_station.get_bases()
    print(best_base)   # (296, (23, 17))

    # Exercise 2
    #
    meteor_station.set_base((23, 17))

    for n in range(200):
        jobber = meteor_station.fire_gun_and_remove_asteroid()
        print("Shot [%d] Meteorite [%s]" % (n + 1, str(jobber)))
