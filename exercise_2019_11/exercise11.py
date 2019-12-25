from intcomputer.intcomputer import IntCodeComputer
from utils.utils import read_file
from enum import Enum


class Colour(Enum):
    BLACK = 0
    WHITE = 1


class Turn(Enum):
    LEFT = 0
    RIGHT = 1


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class PaintingRobot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.panel_grid = dict()
        self.panel_grid[(0, 0)] = {'colour': Colour.WHITE}  # Needed for exercise 2
        self.direction = Direction.UP

        self.minx = 0
        self.miny = 0
        self.maxx = 0
        self.maxy = 0

    def change_direction(self, turn: Turn):
        if turn == Turn.LEFT:
            if self.direction == Direction.UP:
                self.direction = Direction.LEFT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.LEFT:
                self.direction = Direction.DOWN
        elif turn == Turn.RIGHT:
            if self.direction == Direction.UP:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.LEFT:
                self.direction = Direction.UP
            elif self.direction == Direction.DOWN:
                self.direction = Direction.LEFT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN

    def input(self, paint: int, turn: int):
        self.panel_grid[(self.x, self.y)] = {'colour': Colour(paint)}

        self.change_direction(Turn(turn))

        if self.direction == Direction.UP:
            self.y += 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.DOWN:
            self.y -= 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        self.minx = min(self.minx, self.x)
        self.miny = min(self.miny, self.y)
        self.maxx = max(self.maxx, self.x)
        self.maxy = max(self.maxy, self.y)

    def get_current_cell_colour(self) -> int:
        if (self.x, self.y) in self.panel_grid:
            result = self.panel_grid[(self.x, self.y)]['colour']
        else:
            result = Colour.BLACK

        return result.value

    def print_message(self):

        for y in range(0, -6, -1):
            msg = ""
            for x in range(0, 43):
                if (x, y) in self.panel_grid and self.panel_grid[(x, y)]['colour'] == Colour.WHITE:
                    msg += u"\u2588"
                else:
                    msg += " "
            print(msg)


if __name__ == '__main__':
    robot = PaintingRobot()

    computer = IntCodeComputer(read_file(), auto_mode=True, grow_mode=True)
    computer.add_input(1)
    computer.execute()

    count = 0
    while computer.is_not_finished():
        count += 1
        print("cycle %d: Location [%d, %d]" % ( count, robot.x, robot.y))
        print("output from int computer [%d, %d]" % (computer.get_output_previous(), computer.get_output()))
        robot.input(computer.get_output_previous(), computer.get_output())
        print("output from robot [%d]" % robot.get_current_cell_colour())
        computer.add_input(robot.get_current_cell_colour())
        computer.resume()

    print("output [%d, %d]" % (computer.get_output_previous(), computer.get_output()))
    print(len(robot.panel_grid))
    print(robot.panel_grid.keys())

    # Exercise 2 - 45 points
    #
    robot.print_message()
