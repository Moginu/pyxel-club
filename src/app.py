import pyxel


class App:
    # Position in resources file.
    BIRD_WIDTH = 16
    BIRD_HEIGHT = 16
    DROP_BIRD_X = 0
    DROP_BIRD_Y = 0
    JUMP_BIRD_X = 16
    JUMP_BIRD_Y = 0
    PIPE_WIDTH = 32
    PIPE_HEIGHT = 144
    PIPE_X = 160
    PIPE_Y = 0
    PIPE_VERTICAL_GAP = 64

    def __init__(self):
        pyxel.init(200, 240, caption="Flappy Bird")
        pyxel.load("assets/jump_game.pyxres")

        # board properties
        self.board_fps = 30

        # birds properties
        self.bird_x = 65
        self.bird_y = 100

        self.bird_is_alive = True

        self.seconds = 1/self.board_fps

        self.total_time = 1000*self.seconds
        self.bird_falling_speed = 0
        self.max_falling_speed = pyxel.height/self.total_time

        self.bird_acceleration = 2*pyxel.height/(self.total_time*self.total_time)

        self.bird_rising_speed = 2*self.max_falling_speed
        self.bird_jump = False

        # pipes properties
        self.pipe_total_time = 4
        # TODO: generate randomly
        self.up_pipe_height = 88
        self.pipe_x = 128
        self.pipe_pair = {
            'up': {
                'x': self.pipe_x,
                'y': 0,
                'u': self.PIPE_X,
                'v': self.PIPE_Y,
                'w': self.PIPE_X + self.PIPE_WIDTH,
                'h': -self.up_pipe_height,
            },
            'down': {
                'x': self.pipe_x,
                'y': self.up_pipe_height + self.PIPE_VERTICAL_GAP,
                'u': self.PIPE_X,
                'v': self.PIPE_Y,
                'w': self.PIPE_X + self.PIPE_WIDTH,
                'h': self.up_pipe_height,
            },
        }
        self.pipe_moving_speed = (pyxel.width+self.PIPE_WIDTH) / self.pipe_total_time / self.board_fps

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_bird()
        self.update_pipe_moving_speed()
        self.update_pipe_pair()

    def draw(self):
        # render background wiht color 12
        pyxel.cls(12)

        # draw bird
        self.draw_bird()
        # draw pipe pair
        self.draw_pipe_pair()

    def update_bird(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bird_y = (self.bird_y-self.bird_rising_speed) % pyxel.height
            self.bird_falling_speed = 0
            self.bird_jump = True
        else:
            if self.bird_falling_speed < self.max_falling_speed:
                self.bird_falling_speed += self.bird_acceleration*self.seconds
            self.bird_y = (self.bird_y+self.bird_falling_speed) % pyxel.height
            self.bird_jump = False

    def update_pipe_moving_speed(self):
        self.pipe_moving_speed += 2 / 10000

    def update_pipe_pair(self):
        for pipe, location in self.pipe_pair.items():
            self.pipe_pair[pipe]['x'] = (location['x'] - self.pipe_moving_speed) % pyxel.width

    def draw_bird(self):
        pyxel.blt(
            self.bird_x,
            self.bird_y,
            0,
            self.JUMP_BIRD_X if self.bird_jump else self.DROP_BIRD_X,
            self.JUMP_BIRD_Y if self.bird_jump else self.DROP_BIRD_Y,
            self.BIRD_WIDTH,
            self.BIRD_HEIGHT,
            12
        )

    def draw_pipe_pair(self):
        for _, location in self.pipe_pair.items():
            pyxel.blt(
                location['x'],
                location['y'],
                0,
                location['u'],
                location['v'],
                location['w'],
                location['h'],
                0
            )


App()
