import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="test")
        pyxel.load("assets/jump_game.pyxres")
        self.bird_x = 0
        self.bird_y = 0
        self.bird_is_alive = True
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
        pass


App()
