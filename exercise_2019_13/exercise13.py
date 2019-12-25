from utils.utils import read_file
from intcomputer.intcomputer import IntCodeComputer


class BreakoutIntComputer(IntCodeComputer):

    def __init__(self, *args, **kwargs):
        super(BreakoutIntComputer, self).__init__(*args, **kwargs)
        self.system = None
        self.history_pointer = 0
        self.screen_buffer = dict()
        self.score = None
        self.ball_address = None
        self.ball_address_previous = None
        self.paddle_address = None
        self.turn_count = 0

    def print_game(self):
        # 0 is an empty tile. No game object appears in this tile.
        # 1 is a wall tile. Walls are indestructible barriers.
        # 2 is a block tile. Blocks can be broken by the ball.
        # 3 is a horizontal paddle tile. The paddle is indestructible.
        # 4 is a ball tile.
        #
        # Grid is 38 x 21
        #
        for _y in range(21):
            line = ""
            for _x in range (38):
                if (_x, _y) in self.screen_buffer:
                    char = self.screen_buffer[(_x, _y)]
                    if char == 0:
                        line += "    "
                    elif char == 1:
                        line += u'\u2588\u2588\u2588\u2588'
                    elif char == 2:
                        line += "[##]"
                    elif char == 3:
                        line += "<==>"
                    elif char == 4:
                        line += " () "
                else:
                    line += "    "
            print(line)

        print("Turn: %d Score: [%d] Ball: %s Paddle %s " % (self.turn_count, self.score, str(self.ball_address), str(self.paddle_address)))

    def process_history(self):
        buffer = computer.get_output_history()
        while self.history_pointer < len(buffer):
            x = buffer[self.history_pointer]
            self.history_pointer += 1
            y = buffer[self.history_pointer]
            self.history_pointer += 1
            z = buffer[self.history_pointer]
            self.history_pointer += 1
            if (x, y) == (-1, 0):
                self.score = z
            else:
                if z == 4:
                    self.ball_address_previous = self.ball_address
                    self.ball_address = (x, y)
                if z == 3:
                    self.paddle_address = (x, y)
                self.screen_buffer[(x, y)] = z

    def get_ball_base_line(self) -> int:
        result = self.paddle_address[0]
        if self.ball_address_previous:
            if self.ball_address_previous[1] > self.ball_address[1]:  # coming down
                result = self.ball_address[0] + \
                     ((self.ball_address[0] - self.ball_address_previous[0]) * (19 - self.ball_address[1]))
            else:
                result = self.ball_address[0]
        return result

    def get_paddle_direction(self):
        result = 0

        if self.get_ball_base_line() < self.paddle_address[0]:
            result = -1
        elif self.get_ball_base_line() > self.paddle_address[0]:
            result = 1
        return result

    def run_break_out(self):
        super().execute()
        self.process_history()
        self.print_game()

        finished, self.turn_count = False, 0
        while not finished:
            self.turn_count += 1
            super().add_input(self.get_paddle_direction())
            super().resume()
            self.process_history()
            self.print_game()
            if self.ball_address[1] == 20:
                print("Turn [%d] game over" % self.turn_count)
                exit(-1)
            if self.turn_count > 5301:
                finished = True


if __name__ == '__main__':
    computer = BreakoutIntComputer(read_file(), auto_mode=True, grow_mode=True)
    computer.program_list[0] = 2
    computer.run_break_out()

    print('-------------------------------')

