from pico2d import *
import random

speedX = 0

class Mario:
    def __init__(self):
        self.x, self.y = 100,90
        self.frame = 0
        self.image = load_image('Assets/mario_t.png')

    def update(self):
        global speedX
        if speedX == 1:
            self.x += 5
        if speedX == -1:
            self.x -= 5

    def draw(self):
        pass

def handle_events():
    global running, speedX
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if(speedX < 1)
                speedX += 1

        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            if(speedX >= 1)
                speedX -= 1

        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            pass




running = True