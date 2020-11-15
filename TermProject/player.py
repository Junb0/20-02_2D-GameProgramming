import gobj
import gfw
from pico2d import *

class Body:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT): (-1, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (1, 0),
        (SDL_KEYDOWN, SDLK_DOWN): (0, -1),
        (SDL_KEYDOWN, SDLK_UP): (0, 1),
        (SDL_KEYUP, SDLK_LEFT): (1, 0),
        (SDL_KEYUP, SDLK_RIGHT): (-1, 0),
        (SDL_KEYUP, SDLK_DOWN): (0, 1),
        (SDL_KEYUP, SDLK_UP): (0, -1),
    }
    ACTIONS = ['die', 'hit', 'idle', 'moveback', 'movefront']
    images = {}
    FPS = 12


    def __init__(self):
        self.pos = (get_canvas_width() // 2, get_canvas_height() // 2)
        self.delta = 0, 0
        self.char = 'hana'
        self.file_fmt = '%s/Sprites/actors/%s/%s/spr_chr_hna_%s%d.png'
        self.images = Body.load_images(self.char, self.file_fmt)
        self.action = 'idle'
        self.speed = 300
        self.fidx = 0
        self.time = 0
        self.mag = 1

    @staticmethod
    def load_all_images():
        Body.load_images('hana', '%s/Sprites/actors/%s/%s/spr_chr_hna_%s%d.png')

    @staticmethod
    def load_images(char, file_fmt):
        if char in Body.images:
            return Body.images[char]
        images = {}
        count = 0

        for action in Body.ACTIONS:
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, char, action, action, n)
                if os.path.isfile(fn):
                    action_images.append((gfw.image.load(fn)))
                else:
                    break
                count += 1
            images[action] = action_images
        Body.images[char] = images
        print('%d images loaded for %s' % (count, char))
        return images

    def do_idle(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Body.FPS)

    def do_move(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Body.FPS)
        x,y = self.pos
        dx,dy = self.delta
        uniform = 1
        if dx != 0 and dy != 0:
            uniform = 2 ** 0.5

        x += dx * self.speed * self.mag * gfw.delta_time / uniform
        y += dy * self.speed * self.mag * gfw.delta_time / uniform

        self.pos = x, y

    def update(self):
        if self.action == 'idle':
            Body.do_idle(self)
        if self.action == 'movefront' or self.action == 'moveback':
            Body.do_move(self)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Body.KEY_MAP:
            self.delta = gobj.point_add(self.delta, Body.KEY_MAP[pair])
            dx = self.delta[0]
            dy = self.delta[1]
            self.action = \
                'movefront' if dx > 0 or dy != 0 else \
                'moveback' if dx < 0 else \
                'idle'

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        image.composite_draw(0, '', *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

class Weapon(Body):
    ACTIONS = ['fire', 'idle', 'reload', 'walk']

    def __init__(self):
        super().__init__()
        self.delay = 0.5
        self.file_fmt = '%s/Sprites/weapons/%s/%s/spr_wpn_type89_%s%d.png'
        self.char = 'Assault Rifle'
        self.images = Weapon.load_images(self.char, self.file_fmt)

    @staticmethod
    def load_all_images():
        Weapon.load_images('Assault Rifle', '%s/Sprites/weapons/%s/%s/spr_wpn_type89_%s%d.png')

    @staticmethod
    def load_images(char, file_fmt):
        if char in Weapon.images:
            return Weapon.images[char]
        images = {}
        count = 0

        for action in Weapon.ACTIONS:
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, char, action, action, n)
                if os.path.isfile(fn):
                    action_images.append((gfw.image.load(fn)))
                else:
                    break
                count += 1
            images[action] = action_images
        Body.images[char] = images
        print('%d images loaded for %s' % (count, char))
        return images

    def update(self, pos, fidx):
        if self.action == 'idle' or self.action == 'walk':
            Weapon.do_idle(self)
        self.pos = pos
        self.fidx = fidx

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Body.KEY_MAP:
            self.delta = gobj.point_add(self.delta, Body.KEY_MAP[pair])
            dx = self.delta[0]
            dy = self.delta[1]
            self.action = \
                'walk' if dx != 0 or dy != 0 else \
                'idle'

class Player:
    def __init__(self):
        self.body = Body()
        self.weapon = Weapon()

    def update(self):
        self.body.update()
        self.weapon.update(self.body.pos, self.body.fidx)

    def draw(self):
        self.body.draw()
        self.weapon.draw()

    def handle_event(self, e):
        self.body.handle_event(e)
        self.weapon.handle_event(e)

    @staticmethod
    def load_all_images():
        Body.load_all_images()
        Weapon.load_all_images()
