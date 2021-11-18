from pico2d import *

class Grass:
    def __init__(self):
        self.leftgrassimage = load_image('Assets/b6.png')
        self.rightgrassimage = load_image('Assets/b7.png')
        self.middlegrassimage = load_image('Assets/b0.png')
        self.undergrassimage = load_image('Assets/b1.png')

    def update(self):
        pass

    def draw(self):
        self.leftgrassimage.draw(15, 39)
        for i in range(0, 24):
            self.middlegrassimage.draw((i * 32) + 45, 39)
        for i in range(0, 26):
            self.undergrassimage.draw((i * 32) + 15, 9)
        self.rightgrassimage.draw(787, 39)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600-1, 50
