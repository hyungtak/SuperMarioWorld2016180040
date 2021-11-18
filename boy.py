import game_framework
from pico2d import *

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE_DOWN, SPACE_UP = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_DOWN
}

jumpTimer = 0
jumpPower = 50

# Boy States

class IdleState:

    def enter(boy, event):
        global jumpTimer, jumpPower
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS * 2
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS* 2
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS* 2
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS* 2
        boy.dir = clamp(-1, boy.velocity, 1)
        boy.velocity = clamp(-RUN_SPEED_PPS, boy.velocity, RUN_SPEED_PPS)

    def exit(boy, event):
        pass

    def do(boy):
        global jumpTimer, jumpPower
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if jumpTimer > 0:
            boy.y = ((12-jumpTimer) * (12-jumpTimer) * (-9.8) / 2) + ((12-jumpTimer) * jumpPower) + 70
        jumpTimer -= 0.025
        boy.y = clamp(70, boy.y, 800)

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(0, 52, 27, 39, boy.x, boy.y)
        else:
            boy.image.clip_composite_draw(0, 52, 27, 39, 0, 'h', boy.x, boy.y, 27, 39)



class RunState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS* 2
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS* 2
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS* 2
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS* 2
        boy.dir = clamp(-1, boy.velocity, 1)
        boy.velocity = clamp(-RUN_SPEED_PPS, boy.velocity, RUN_SPEED_PPS)

    def exit(boy, event):
        pass

    def do(boy):
        global jumpTimer, jumpPower
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        if jumpTimer > 0:
            boy.y = ((12-jumpTimer) * (12-jumpTimer) * (-9.8) / 2) + ((12-jumpTimer) * jumpPower) + 70
        jumpTimer -= 0.025
        boy.y = clamp(70, boy.y, 800)

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw((int(boy.frame) // 4) * 27, 52, 27, 39, 0, 'h', boy.x, boy.y, 27, 39)
        else:
            boy.image.clip_draw((int(boy.frame) // 4) * 27, 52, 27, 39, boy.x, boy.y)

class JumpState:

    def enter(boy, event):
        global jumpTimer
        if jumpTimer <= 0:
            jumpTimer = 12

    def exit(boy, event):
        pass

    def do(boy):
        global jumpTimer, jumpPower
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        if jumpTimer > 0:
            boy.y = ((12 - jumpTimer) * (12 - jumpTimer) * (-9.8) / 2) + ((12 - jumpTimer) * jumpPower) + 70
        jumpTimer -= 0.025
        boy.y = clamp(70, boy.y, 800)

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw((int(boy.frame) // 4) * 27, 52, 27, 39, 0, 'h', boy.x, boy.y, 27, 39)
        else:
            boy.image.clip_draw((int(boy.frame) // 4) * 27, 52, 27, 39, boy.x, boy.y)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE_DOWN: JumpState, SPACE_UP: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE_DOWN: JumpState, SPACE_UP: IdleState},
    JumpState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE_DOWN: JumpState, SPACE_UP: RunState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 800 // 2, 70
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('Assets/mario_t.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20


    def isJump(self):
        pass

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
        #self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        #draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

