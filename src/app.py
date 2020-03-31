import pyxel


class App:
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

        self.pipe_total_time = 4
        self.pipe_width = 32
        self.pipe_pair = {
            'high': {
                'x': 128,
                'y': 0,
                'u': 160,
                'v': 56,
                'w': 192,
                'h': 144,
            },
            'low': {
                'x': 128,
                'y': 96,
                'u': 160,
                'v': 56,
                'w': 192,
                'h': -144,
            },
        }
        self.pipe_moving_speed = (pyxel.width+self.pipe_width) / self.pipe_total_time / self.board_fps

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
            16 if self.bird_jump is True else 0,
            0,
            16,
            16,
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
