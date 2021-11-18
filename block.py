import game_framework
import random
from pico2d import *

TIME_PER_ACTION_QUESTION = 0.6
TIME_PER_ACTION_ENABLED = 0.8
ACTION_PER_TIME_QUESTION = 1.0 / TIME_PER_ACTION_QUESTION
ACTION_PER_TIME_ENABLED = 1.0 / TIME_PER_ACTION_ENABLED
FRAMES_PER_ACTION_QUESTION = 6
FRAMES_PER_ACTION_ENABLED = 4

class Block:
    def __init__(self):
        self.questionblockimage = load_image('Assets/b2.png')
        self.enabledblockimage = load_image('Assets/b3.png')
        self.disabledblockimage = load_image('Assets/b4.png')
        self.blueblockimage = load_image('Assets/b5.png')
        self.questionframe = 0
        self.enabledframe = 0

    def update(self):
        self.questionframe = (self.questionframe + FRAMES_PER_ACTION_QUESTION * ACTION_PER_TIME_QUESTION * game_framework.frame_time) % 6
        self.enabledframe = (self.enabledframe + FRAMES_PER_ACTION_ENABLED * ACTION_PER_TIME_ENABLED * game_framework.frame_time) % 4

    def draw(self):

        for i in range(2, 7):
            self.questionblockimage.clip_draw(int(self.questionframe) * 32, 0, 32, 32, ((i*3) * 32) + 45, 350)
        for i in range(5, 20):
            self.enabledblockimage.clip_draw(0, 0, 32, 32, (i * 32) + 45, 150)
        for i in range(20, 24):
            self.enabledblockimage.clip_draw(int(self.enabledframe) * 32, 0, 32, 32, (i * 32) + 45, 150)
        for i in range(7, 12):
            self.disabledblockimage.draw(((i*2) * 32) + 15, 250)
        self.blueblockimage.draw(787, 39)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600-1, 50
