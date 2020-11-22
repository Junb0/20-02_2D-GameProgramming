from pico2d import *
import gfw
import gobj
import random

class Bullet:
    images = {}
    ACTION = ['move', 'hit']
    FPS = 12
    def __init__(self, pos, delta, speed, char, damage, stun):
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.char = char
        self.damage = damage
        self.images = Bullet.load_images(self.char)
        self.time = 0
        self.fidx = 0
        self.stun = stun
        self.action = 'move'
        self.width = self.images['move'][0].w * gobj.PIXEL_SCOPE
        self.height = self.images['move'][0].h * gobj.PIXEL_SCOPE

    @staticmethod
    def load_images(char):
        if char in Bullet.images:
            return Bullet.images[char]
        images = {}
        count = 0
        file_fmt = '%s/Sprites/Bullets/%s/%s/spr_blt_%s_%s%d.png'

        for action in Bullet.ACTION:
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, char, action, char, action, n)
                if os.path.isfile(fn):
                    action_images.append((gfw.image.load(fn)))
                else:
                    break
                count += 1
            images[action] = action_images
        Bullet.images[char] = images
        print('%d images loaded for %s' % (count, char))
        return images

    def do_move(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Bullet.FPS)
        x, y = self.pos
        dx, dy = self.delta

        x += dx * self.speed * gfw.delta_time
        y += dy * self.speed * gfw.delta_time

        self.pos = x, y

        if self.pos[0] + self.width // 2 > get_canvas_width():
            self.action = 'hit'
            self.time = 0
        elif self.pos[0] - self.width // 2 < 0:
            self.action = 'hit'
            self.time = 0

    def do_hit(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Bullet.FPS)
        if self.fidx >= len(self.images['hit']):
            self.remove()

    def update(self):
        if self.action == 'move':
            self.do_move()
        elif self.action == 'hit':
            self.do_hit()

    def remove(self):
        gfw.world.remove(self)

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        flip = 'h' if self.delta[0] < 0 else ''
        image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

class LongBullet(Bullet):
    def __init__(self, pos, damage, stun):
        super().__init__(pos, (1, 0), 1500, 'long', damage, stun)
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        LongBullet.load_images('long')

    def get_bb(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 2 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y + 1 * gobj.PIXEL_SCOPE
    def get_ground(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 11 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y - 11 * gobj.PIXEL_SCOPE

class ShortBullet(Bullet):
    def __init__(self, pos, damage, stun):
        super().__init__(pos, (1, 0), 1000, 'short', damage, stun)
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        LongBullet.load_images('short')

    def get_bb(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 2 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y + 1 * gobj.PIXEL_SCOPE
    def get_ground(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 11 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y - 11 * gobj.PIXEL_SCOPE


class KnhBullet(Bullet):
    def __init__(self, pos, damage):
        super().__init__(pos, (-1, 0), 1000, 'knh', damage, 0)
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        KnhBullet.load_images('knh')
    def get_ground(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 9 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y - 9 * gobj.PIXEL_SCOPE

class NkmBullet(Bullet):
    def __init__(self, pos, damage):
        super().__init__(pos, (-1, 0), 1000, 'nkm', damage, 0)
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        NkmBullet.load_images('nkm')
    def get_ground(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, y - 9 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y - 9 * gobj.PIXEL_SCOPE

class KrkBullet(Bullet):
    def __init__(self, pos, damage, rain_num):
        super().__init__(pos, (0, 0), 0, 'krk', 0, 0)
        self.rain_num = rain_num
        self.rain_delay = 0.2
        self.rain_cooltime = 0
        self.action = 'hit'
        self.is_draw = True
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        KrkBullet.load_images('krk')

    def get_ground(self):
        x, y = self.pos
        return x - 14 * gobj.PIXEL_SCOPE, get_canvas_height(), x + 14 * gobj.PIXEL_SCOPE, get_canvas_height()

    def draw(self):
        if self.is_draw:
            images = self.images[self.action]
            image = images[self.fidx % len(images)]
            flip = 'h' if self.delta[0] < 0 else ''
            image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

    def update(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Bullet.FPS)
        if self.fidx >= len(self.images['hit']):
            self.is_draw = False
        if not self.is_draw:
            self.rain_cooltime -= gfw.delta_time
            if self.rain_cooltime <= 0:
                # generate rain
                dest = (self.pos[0] + random.randint(-80, 80), self.pos[1] + random.randint(-40, 40))
                rain = RainBullet((dest[0], dest[1] + get_canvas_height()), self.damage, dest)
                gfw.world.add(gfw.layer.any, rain)
                self.rain_cooltime = self.rain_delay
                self.rain_num -= 1
            if self.rain_num <= 0:
                self.remove()

class RainBullet(Bullet):
    def __init__(self, pos, damage, dest_pos):
        super().__init__(pos, (0, -1), 2000, 'rain', damage, 0)
        self.dest_pos = dest_pos
        self.images = Bullet.load_images(self.char)

    @staticmethod
    def load_all_images():
        KrkBullet.load_images('krk')

    def get_ground(self):
        x, y = self.pos
        if self.action == 'move':
            return x - 14 * gobj.PIXEL_SCOPE, 0, x + 14 * gobj.PIXEL_SCOPE, 0
        else:
            return x - 14 * gobj.PIXEL_SCOPE, y - 8 * gobj.PIXEL_SCOPE, x + 14 * gobj.PIXEL_SCOPE, y - 8 * gobj.PIXEL_SCOPE

    def do_move(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Bullet.FPS)
        x, y = self.pos
        dx, dy = self.delta

        x += dx * self.speed * gfw.delta_time
        y += dy * self.speed * gfw.delta_time

        self.pos = x, y

        if self.pos[1] <= self.dest_pos[1]:
            self.action = 'hit'
            self.time = 0
            print('bullet hit')