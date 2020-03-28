import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 240, caption="test")
        pyxel.load("assets/jump_game.pyxres")

        # board properties
        self.board_fps = 30

        # birds properties
        self.bird_x = 65
        self.bird_y = 100

        self.bird_is_alive = True

        self.total_time = 10
        self.bird_falling_speed = pyxel.height/self.total_time/self.board_fps
        self.bird_rising_speed = 10*self.bird_falling_speed
        self.bird_jump = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_bird()

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
            self.bird_jump = True
        else:
            self.bird_y = (self.bird_y+self.bird_falling_speed) % pyxel.height
            self.bird_jump = False

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
        pyxel.blt(
            128,
            0,
            0,
            160,
            56,
            192,
            144,
            0
        )
        pyxel.blt(
            128,
            96,
            0,
            160,
            56,
            192,
            -144,
            0
        )


App()
