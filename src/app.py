import pyxel
import random
from collections import deque


SCREEN_WIDTH = 200
SCREEN_HEIGHT = 240


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
    PIPE_HORIZONTAL_GAP = (SCREEN_WIDTH - PIPE_WIDTH) / 2
    PIPE_TOTAL_TIME = 3

    def __init__(self, x, y, height, is_up=True):
        self.x = x
        self.y = y
        self.u = self.PIPE_X
        self.v = self.PIPE_Y
        self.w = self.PIPE_WIDTH
        self.h = -height if is_up else height
        self.height = height


class PipePair:
    def __init__(self, up_pipe):
        self.up = up_pipe
        self.down = Pipe(
            self.up.x,
            self.up.y + self.up.height + Pipe.PIPE_VERTICAL_GAP,
            pyxel.height - self.up.height - Pipe.PIPE_VERTICAL_GAP,
            False,
        )
        self.is_drawn = True
        self.is_append = False
        self.is_scored = False


class App:
    # Position in resources file.
    BIRD_WIDTH = 16
    BIRD_HEIGHT = 16
    DROP_BIRD_X = 0
    DROP_BIRD_Y = 0
    JUMP_BIRD_X = 16
    JUMP_BIRD_Y = 0
    score = 0

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Flappy Bird")
        pyxel.load("assets/jump_game.pyxres")

        # board properties
        self.board_fps = 30

        # birds properties
        self.bird_x = 65
        self.bird_y = 100

        self.bird_is_alive = True

        self.seconds_per_frame = 1 / self.board_fps

        self.total_time = 7
        self.bird_falling_speed = 0
        self.max_falling_speed = 2 * pyxel.height / self.total_time

        self.bird_acceleration = 2 * pyxel.height / (self.total_time * self.total_time)

        self.bird_rising_speed = 1 * self.max_falling_speed / 2
        self.bird_jump = False

        # pipes properties

        self.pipe_pairs = deque()
        self.pipe_pairs.append(self.generate_random_pipe_pair())

        self.pipe_moving_speed = (pyxel.width + Pipe.PIPE_WIDTH) / Pipe.PIPE_TOTAL_TIME / self.board_fps
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.bird_is_alive:
            self.update_bird()
            self.update_pipe_moving_speed()
            self.update_pipe_pair()
            self.update_score()
            self.death_judgment()

    def draw(self):
        # render background with color 12
        if self.bird_is_alive:
            pyxel.cls(12)
            # draw bird
            self.draw_bird()
            # draw pipe pair
            self.draw_pipe_pair()
            self.draw_score()
        else:
            self.draw_death()

    def update_bird(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bird_y = (self.bird_y - self.bird_rising_speed) % pyxel.height
            self.bird_falling_speed = 0
            self.bird_jump = True
        else:
            if self.bird_falling_speed < self.max_falling_speed:
                self.bird_falling_speed += self.bird_acceleration * self.seconds_per_frame
            self.bird_y = (self.bird_y + self.bird_falling_speed) % pyxel.height
            self.bird_jump = False

    def update_pipe_moving_speed(self):
        self.pipe_moving_speed += 2 / 10000

    def update_pipe_pair(self):
        is_append = False
        is_popleft = False
        for i,pipe_pair in enumerate(self.pipe_pairs):
            pipe_pair.up.x = pipe_pair.down.x = (
                pipe_pair.up.x - self.pipe_moving_speed
            )
            if pipe_pair.is_append is False:
                if pipe_pair.up.x - (Pipe.PIPE_HORIZONTAL_GAP) <= 0:
                    self.pipe_pairs[i].is_append = True
                    is_append = True
            if pipe_pair.up.x < -Pipe.PIPE_WIDTH:
                is_popleft = True

        if is_append is True:
            self.pipe_pairs.append(self.generate_random_pipe_pair())
        if is_popleft is True:
            self.pipe_pairs.popleft()

    def update_score(self):
        for pipe_pair in self.pipe_pairs:
            if self.bird_x + Bird.BIRD_WIDTH >= pipe_pair.up.x and not pipe_pair.is_scored:
                self.score += 1
                pipe_pair.is_scored = True

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
        for pipe_pair in self.pipe_pairs:
            if pipe_pair.is_drawn:
                pyxel.blt(
                    pipe_pair.up.x,
                    pipe_pair.up.y,
                    0,
                    pipe_pair.up.u,
                    pipe_pair.up.v,
                    pipe_pair.up.w,
                    pipe_pair.up.h,
                    0
                )
                pyxel.blt(
                    pipe_pair.down.x,
                    pipe_pair.down.y,
                    0,
                    pipe_pair.down.u,
                    pipe_pair.down.v,
                    pipe_pair.down.w,
                    pipe_pair.down.h,
                    0
                )

    def death_judgment(self):
        bird_rec = self._generate_rectangle(
            self.bird_x,
            self.bird_y,
            self.BIRD_WIDTH,
            self.BIRD_HEIGHT
        )
        up_pipe_rec = self._generate_rectangle(
            self.pipe_pairs[0].up.x,
            self.pipe_pairs[0].up.y,
            Pipe.PIPE_WIDTH,
            -self.pipe_pairs[0].up.h
        )
        down_pipe_rec = self._generate_rectangle(
            self.pipe_pairs[0].down.x,
            self.pipe_pairs[0].down.y,
            Pipe.PIPE_WIDTH,
            pyxel.height - self.pipe_pairs[0].up.h - Pipe.PIPE_VERTICAL_GAP
        )

        self._check_death(bird_rec, up_pipe_rec)
        self._check_death(bird_rec, down_pipe_rec)

    def _generate_rectangle(self, x, y, width, height):
        return [x, y, x+width, y+height]

    def _check_death(self, bird_rec, pipe_rec):
        if (
            not (
                bird_rec[2] <= pipe_rec[0] or
                bird_rec[3] <= pipe_rec[1] or
                bird_rec[0] >= pipe_rec[2] or
                bird_rec[1] >= pipe_rec[3]
            )
        ) or (
            not bird_rec[1] <= SCREEN_HEIGHT - Bird.BIRD_HEIGHT and
            bird_rec[1] >= 0
        ):
            self.bird_is_alive = False

    def draw_death(self):
        pyxel.cls(col=0)
        pyxel.text(55, 41, "Game over", pyxel.frame_count % 16)

    def generate_random_pipe_pair(self):
        return PipePair(Pipe(200, 0, random.randint(32, 144)))

    def draw_score(self):
        pyxel.text(20, 20, str(self.score), 7)


App()
