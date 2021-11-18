import game_framework
from pico2d import *
import random

import game_world

# Goomba Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 8.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Goomba Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1



# Goomba Event
STAMPED, REVERSE_TIMER = range(2)

# Goomba States

class IdleState:

    def enter(Goomba, event):
        if (random.randint(1, 100) // 2) == 0:
            Goomba.velocity += RUN_SPEED_PPS * 2
        else:
            Goomba.velocity -= RUN_SPEED_PPS * 2

        Goomba.dir = clamp(-1, Goomba.velocity, 1)
        Goomba.velocity = clamp(-RUN_SPEED_PPS, Goomba.velocity, RUN_SPEED_PPS)


    def exit(Goomba, event):
        pass

    def do(Goomba):
        Goomba.frame = (Goomba.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        Goomba.x += Goomba.velocity * game_framework.frame_time
        Goomba.x = clamp(25, Goomba.x, 800 - 25)
        if Goomba.x >= 750:
            Goomba.velocity -= RUN_SPEED_PPS * 2
        if Goomba.x <= 500:
            Goomba.velocity += RUN_SPEED_PPS * 2

        Goomba.dir = clamp(-1, Goomba.velocity, 1)
        Goomba.velocity = clamp(-RUN_SPEED_PPS, Goomba.velocity, RUN_SPEED_PPS)

    def draw(Goomba):
        if Goomba.dir == 1:
            Goomba.image.clip_draw(int(Goomba.frame) * 32, 0, 32, 32, Goomba.x, Goomba.y, 25, 25)

        else:
            Goomba.image.clip_composite_draw(int(Goomba.frame) * 32, 0, 32, 32, 0, 'h', Goomba.x, Goomba.y, 25, 25)

class ReverseState:

    def enter(Goomba, event):
        Goomba.frame = 0
        Goomba.timer = 500


    def exit(Goomba, event):
        pass

    def do(Goomba):
        Goomba.frame = (Goomba.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        Goomba.timer -= 1
        if Goomba.timer == 0:
            Goomba.add_event(REVERSE_TIMER)

    def draw(Goomba):
        if Goomba.dir == 1:
            Goomba.image.clip_composite_draw(int(Goomba.frame) * 32, 0, 32, 32, 0, 'v', Goomba.x, Goomba.y, 25, 25)
        else:
            Goomba.image.clip_composite_draw(int(Goomba.frame) * 32, 0, 32, 32, 330, ' ', Goomba.x, Goomba.y, 25, 25)






next_state_table = {
    IdleState: {STAMPED: ReverseState, REVERSE_TIMER: IdleState},
    ReverseState: {STAMPED: ReverseState, REVERSE_TIMER: IdleState}
}

class Goomba:

    def __init__(self):
        self.x, self.y = 600, 65
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('Assets/m0.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15


    def get_stamped(self):
        self.add_event(STAMPED)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())
