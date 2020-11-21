import gobj
import gfw
from pico2d import *
from bullet import LongBullet

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

        x = clamp(0 + 64 , x, 1280 - 64)
        y = clamp(0 + 64, y, 430)

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
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_z): (1, 0),
        (SDL_KEYUP, SDLK_z): (-1, 0),
        (SDL_KEYDOWN, SDLK_x): (0, 1),
        (SDL_KEYUP, SDLK_x): (0, -1)
    }

    ACTIONS = ['fire', 'idle', 'reload', 'walk']

    def __init__(self):
        super().__init__()
        self.fire_delay = 0.01
        self.reload_delay = 1.0
        self.file_fmt = '%s/Sprites/weapons/%s/%s/spr_wpn_type89_%s%d.png'
        self.char = 'Assault Rifle'
        self.images = Weapon.load_images(self.char, self.file_fmt)
        self.fire_time = 0
        self.reload_time = 0
        self.state = 0, 0
        self.on_fire = 0
        self.on_reload = 0
        self.dx = 0
        self.dy = 0
        self.fire_cool_time = 0
        self.reload_cool_time = 0
        self.ammo = 5
        self.max_ammo = 500
        self.damage = 10

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

    def do_fire(self):
        self.fire_time += gfw.delta_time
        self.time += gfw.delta_time
        self.fidx = round(self.fire_time * Body.FPS)
        if self.fidx >= len(self.images['fire']) - 1:
            self.fire_time = 0

    def do_reload(self):
        self.reload_time += gfw.delta_time
        self.time += gfw.delta_time
        self.fidx = round(self.reload_time * Body.FPS)
        if self.fidx >= len(self.images['reload']) - 1:
            self.reload_time = 0
            self.ammo = self.max_ammo
    def generate_bullet(self):
        pos = self.pos[0] + 30 * gobj.PIXEL_SCOPE, self.pos[1] - 5 * gobj.PIXEL_SCOPE
        blt = LongBullet(pos, self.damage, 0.2)
        gfw.world.add(gfw.layer.any, blt)

    def choose_action(self):
        if self.on_reload == 1 and self.reload_cool_time <= 0 and self.ammo < self.max_ammo:
            self.action = 'reload'
            print(self.action)
            self.reload_time = 0
            self.reload_cool_time = self.reload_delay
        elif self.reload_time != 0:
            self.action = 'reload'
        elif self.on_fire == 1 and self.fire_cool_time <= 0 and self.ammo > 0 and self.reload_cool_time <= 0: # 다른 상태에서 처음 fire 상태로 변경
            self.action = 'fire'
            print(self.action)
            self.fire_time = 0
            self.fire_cool_time = self.fire_delay
            # 총알 생성
            self.generate_bullet()
            self.ammo -= 1
            print('ammo : ', self.ammo)
        elif self.fire_time != 0: # fire 애니메이션 진행도중
            self.action = 'fire'
        elif self.dx != 0 or self.dy != 0:
            self.action = 'walk'
        else:
            self.action = 'idle'

    def update(self, pos):
        self.pos = pos
        if self.fire_cool_time > 0:
            self.fire_cool_time -= gfw.delta_time
        if self.reload_cool_time > 0:
            self.reload_cool_time -= gfw.delta_time
        Weapon.choose_action(self)

        if self.action == 'reload':
            Weapon.do_reload(self)
        elif self.action == 'fire':
            Weapon.do_fire(self)
        elif self.action == 'idle' or self.action == 'walk':
            Weapon.do_idle(self)

    def handle_event(self, e):
        pair = (e.type, e.key)

        if pair in Weapon.KEY_MAP or pair in Body.KEY_MAP:
            if pair in Weapon.KEY_MAP:
                self.state = gobj.point_add(self.state, Weapon.KEY_MAP[pair])
                self.on_fire = self.state[0]
                self.on_reload = self.state[1]
            else:
                self.delta = gobj.point_add(self.delta, Body.KEY_MAP[pair])
                self.dx = self.delta[0]
                self.dy = self.delta[1]

class Player:
    def __init__(self):
        self.body = Body()
        self.weapon = Weapon()

    def update(self):
        self.body.update()
        self.weapon.update(self.body.pos)

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

    def get_ground(self):
        x, y = self.body.pos
        return x - 16 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE, x + 16 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE
