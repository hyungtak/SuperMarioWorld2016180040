from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('Assets/background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)
        #self.image.draw(800, 30)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600-1, 50
