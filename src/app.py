import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 240, caption="test")
        pyxel.load("assets/jump_game.pyxres")

        self.bird_x = 65
        self.bird_y = 100

        self.bird_is_alive = True

        self.bird_falling_speed = 1
        self.bird_rising_speed = 10


        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_bird()

    def draw(self):
        pyxel.cls(12)

        # draw bird
        pyxel.blt(
            self.bird_x,
            self.bird_y,
            0,
            0,
            0,
            16,
            16,
            12,
        )

    def update_bird(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bird_y= (self.bird_y-self.bird_rising_speed) %pyxel.height
        else:
            self.bird_y = (self.bird_y+self.bird_falling_speed) % pyxel.height


App()
