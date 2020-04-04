import pyxel


class Bird:
    BIRD_WIDTH = 16
    BIRD_HEIGHT = 16
    DROP_BIRD_X = 0
    JUMP_BIRD_X = 16
    BIRD_Y = 0
    BIRD_DROP_SPEED = 0

    def __init__(self, x, y, is_jump=False, is_alive=True):
        self.x = x
        self.y = y
        self.u = self.JUMP_BIRD_X if is_jump else self.DROP_BIRD_X
        self.v = self.BIRD_Y
        self.w = self.BIRD_WIDTH
        self.h = self.BIRD_HEIGHT
        self.speed = self.BIRD_DROP_SPEED
        self.is_alive = is_alive


class Pipe:
    PIPE_WIDTH = 32
    PIPE_HEIGHT = 144
    PIPE_X = 160
    PIPE_Y = 0
    PIPE_VERTICAL_GAP = 64
    PIPE_HORIZONTAL_GAP = 96
    PIPE_TOTAL_TIME = 4

    def __init__(self, x, y, height, is_up=True):
        self.x = x
        self.y = y
        self.u = self.PIPE_X
        self.v = self.PIPE_Y
        self.w = self.PIPE_WIDTH
        self.h = -height if is_up else height
        self.height = height


class PipePair:
    def __init__(self, up_pipe, screen_height):
        self.up = up_pipe
        self.down = Pipe(
            self.up.x,
            self.up.y + self.up.height + Pipe.PIPE_VERTICAL_GAP,
            screen_height - self.up.height - Pipe.PIPE_VERTICAL_GAP,
            False,
        )


class App:
    # Position in resources file.
    BIRD_WIDTH = 16
    BIRD_HEIGHT = 16
    DROP_BIRD_X = 0
    DROP_BIRD_Y = 0
    JUMP_BIRD_X = 16
    JUMP_BIRD_Y = 0

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
        # TODO: generate randomly
        self.pipe_pair = PipePair(
            Pipe(128, 0, 88),
            pyxel.height,
        )
        self.pipe_moving_speed = (pyxel.width+Pipe.PIPE_WIDTH) / Pipe.PIPE_TOTAL_TIME / self.board_fps

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_bird()
        self.update_pipe_moving_speed()
        self.update_pipe_pair()

    def draw(self):
        # render background with color 12
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
        self.pipe_pair.up.x = self.pipe_pair.down.x = (
            self.pipe_pair.up.x + Pipe.PIPE_WIDTH - self.pipe_moving_speed
        ) % (pyxel.width + Pipe.PIPE_WIDTH) - Pipe.PIPE_WIDTH

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
        pyxel.blt(
            self.pipe_pair.up.x,
            self.pipe_pair.up.y,
            0,
            self.pipe_pair.up.u,
            self.pipe_pair.up.v,
            self.pipe_pair.up.w,
            self.pipe_pair.up.h,
            0
        )
        pyxel.blt(
            self.pipe_pair.down.x,
            self.pipe_pair.down.y,
            0,
            self.pipe_pair.down.u,
            self.pipe_pair.down.v,
            self.pipe_pair.down.w,
            self.pipe_pair.down.h,
            0
        )


App()
