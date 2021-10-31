from pico2d import *
import random
import game_framework


class Mario:
    def __init__(self):
        self.x, self.y = 100,90
        self.frame = 0
        self.image = load_image('Assets/mario_t.png')
        self.speedX = 0

    def update(self):
        if self.speedX == 1:
            self.x += 5
        if self.speedX == -1:
            self.x -= 5

    def draw(self):
        if self.speedX < 0:
            self.image.clip_draw(self.frame * 27, 52, 27, 39, self.x, self.y)
        elif self.speedX > 0:
            self.image.clip_composite_draw(self.frame * 27, 52, 27, 39, 0, 'h', self.x, self.y, 27, 39)

class Grass():
    pass

def enter():
    global boy, grass
    boy = Mario()
    grass = Grass()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if(boy.speedX < 1):
                boy.speedX += 1

        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            if(boy.speedX >= 1):
                boy.speedX -= 1

        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            pass




running = True