import unittest
from .exercise10 import MeteorStation


class MyTestCase(unittest.TestCase):
    def test_input_1(self):
        input_1 = ".#..#\n" \
                  ".....\n" \
                  "#####\n" \
                  "....#\n" \
                  "...##\n"
        meteor_station = MeteorStation(input_1.split())
        actual = meteor_station.get_bases()
        self.assertEqual((8, (4, 3)), actual)

    def test_input_2(self):
        input_2 = "......#.#.\n" \
                  "#..#.#....\n" \
                  "..#######.\n" \
                  ".#.#.###..\n" \
                  ".#..#.....\n" \
                  "..#....#.#\n" \
                  "#..#....#.\n" \
                  ".##.#..###\n" \
                  "##...#..#.\n" \
                  ".#....####\n"
        meteor_station = MeteorStation(input_2.split())
        actual = meteor_station.get_bases()
        self.assertEqual((33, (8, 5)), actual)

    def test_input_3(self):
        input_3 = ".#..##.###...#######\n" \
                  "##.############..##.\n" \
                  ".#.######.########.#\n" \
                  ".###.#######.####.#.\n" \
                  "#####.##.#.##.###.##\n" \
                  "..#####..#.#########\n" \
                  "####################\n" \
                  "#.####....###.#.#.##\n" \
                  "##.#################\n" \
                  "#####.##.###..####..\n" \
                  "..######..##.#######\n" \
                  "####.##.####...##..#\n" \
                  ".#####..#.######.###\n" \
                  "##...#.##########...\n" \
                  "#.##########.#######\n" \
                  ".####.#.###.###.#.##\n" \
                  "....##.##.###..#####\n" \
                  ".#.#.###########.###\n" \
                  "#.#.#.#####.####.###\n" \
                  "###.##.####.##.#..##\n"
        meteor_station = MeteorStation(input_3.split())
        actual = meteor_station.get_bases()
        self.assertEqual((210, (13, 11)), actual)

        meteor_station.set_base((13, 11))

        for n in range(200):
            jobber = meteor_station.fire_gun_and_remove_asteroid()
            print("Shot [%d] Meteorite [%s]" % (n+1, str(jobber)))


        # keys = sorted(meteors.keys())
        # index = keys.index(-90.0)
        # print(meteors[keys[index]])
        # print(meteors[keys[index+1]])
        # print(keys)
        # n = len(keys)
        # for i in range(n):
        #     thisKey = keys[i]
        #     if some_condition():
        #         nextKey = keys[(i + 1) % n]
        #         nextValue = dict1[nextKey]
        #         print
        #         thisKey, nextValue
        #
        #
        # print("----")
        # for angle in sorted(meteors.keys()):
        #     print("angle [%s]: %s" % (angle, meteors[angle]))
        # print("----")

        # meteor_station.set_gun_angle(-90.0)


if __name__ == '__main__':
    unittest.main()
