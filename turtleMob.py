import game_framework
from pico2d import *
import random

import game_world

# turtle Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 8.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# turtle Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1



# turtle Event
STAMPED, REVERSE_TIMER = range(2)

# turtle States

class IdleState:

    def enter(TurtleMob, event):
        if (random.randint(1, 100) // 2) == 0:
            TurtleMob.velocity += RUN_SPEED_PPS * 2
        else:
            TurtleMob.velocity -= RUN_SPEED_PPS * 2

        TurtleMob.dir = clamp(-1, TurtleMob.velocity, 1)
        TurtleMob.velocity = clamp(-RUN_SPEED_PPS, TurtleMob.velocity, RUN_SPEED_PPS)


    def exit(TurtleMob, event):
        pass

    def do(TurtleMob):
        TurtleMob.frame = (TurtleMob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        TurtleMob.x += TurtleMob.velocity * game_framework.frame_time
        TurtleMob.x = clamp(25, TurtleMob.x, 800 - 25)
        if TurtleMob.x >= 350:
            TurtleMob.velocity -= RUN_SPEED_PPS * 2
        if TurtleMob.x <= 100:
            TurtleMob.velocity += RUN_SPEED_PPS * 2

        TurtleMob.dir = clamp(-1, TurtleMob.velocity, 1)
        TurtleMob.velocity = clamp(-RUN_SPEED_PPS, TurtleMob.velocity, RUN_SPEED_PPS)

    def draw(TurtleMob):
        if TurtleMob.dir == 1:
            TurtleMob.image.clip_draw(int(TurtleMob.frame) * 32, 0, 32, 50, TurtleMob.x, TurtleMob.y, 25, 50)

        else:
            TurtleMob.image.clip_composite_draw(int(TurtleMob.frame) * 32, 0, 32, 50, 0, 'h', TurtleMob.x, TurtleMob.y, 25, 50)

class ReverseState:

    def enter(TurtleMob, event):
        TurtleMob.frame = 0
        TurtleMob.timer = 500


    def exit(TurtleMob, event):
        pass

    def do(TurtleMob):
        TurtleMob.frame = (TurtleMob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        TurtleMob.timer -= 1
        if TurtleMob.timer == 0:
            TurtleMob.add_event(REVERSE_TIMER)

    def draw(TurtleMob):
            TurtleMob.image.clip_composite_draw(3 * 32, 0, 32, 50, 0, 'h', TurtleMob.x, TurtleMob.y, 25, 50)






next_state_table = {
    IdleState: {STAMPED: ReverseState, REVERSE_TIMER: IdleState},
    ReverseState: {STAMPED: ReverseState, REVERSE_TIMER: IdleState}
}

class TurtleMob:

    def __init__(self):
        self.x, self.y = 200, 75
        # TurtleMob is only once created, so instance image loading is fine
        self.image = load_image('Assets/m1.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20


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
