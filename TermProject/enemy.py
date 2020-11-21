import gobj
import gfw
from pico2d import *
from bullet import KnhBullet
from bullet import NkmBullet

class Enemy:
    ACTIONS = ['attack', 'hit', 'idle', 'walk', 'die']
    images = {}
    FPS = 12

    def __init__(self, pos, delta, speed, char, damage, hp, attack_range, attack_delay, bullet, fire_point):
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.char = char
        self.damage = damage
        self.hp = hp
        self.images= Enemy.load_images(self.char)
        self.time = 0
        self.fidx = 0
        self.action = 'walk'
        self.attack_range = attack_range
        self.attack_delay = attack_delay
        self.bullet = bullet
        self.fire_point = fire_point
        self.attack_cooltime = 0
        self.current_action = self.action
        self.stun = 0

    @staticmethod
    def load_images(char):
        if char in Enemy.images:
            return Enemy.images[char]
        images = {}
        count = 0
        file_fmt = '%s/Sprites/enemies/%s/%s/spr_enm_%s_%s%d.png'

        for action in Enemy.ACTIONS:
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
        Enemy.images[char] = images
        print('%d images loaded for %s' % (count, char))
        return images

    def do_walk(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Enemy.FPS)
        x, y = self.pos
        dx, dy = self.delta

        x += dx * self.speed * gfw.delta_time
        y += dy * self.speed * gfw.delta_time

        self.pos = x, y

        if self.pos[0] < self.attack_range:
            self.action = 'idle'
            self.time = 0
            print('start attack')

    def do_attack(self):
        if self.attack_cooltime <= 0:
            blt = self.bullet(gobj.point_add(self.pos, self.fire_point), self.damage)
            gfw.world.add(gfw.layer.any, blt)
            self.attack_cooltime = self.attack_delay
            self.time = 0
        self.time += gfw.delta_time
        self.attack_cooltime -= gfw.delta_time
        self.fidx = round(self.time * Enemy.FPS)
        if self.fidx >= len(self.images['attack']):
            self.time = 0
            self.action = 'idle'

    def do_idle(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Enemy.FPS)
        self.attack_cooltime -= gfw.delta_time
        if not self.pos[0] < self.attack_range:
            self.action = 'walk'
            self.time = 0
        elif self.attack_cooltime <= 0:
            self.time = 0
            self.action = 'attack'

    def do_hit(self):
        self.time += gfw.delta_time
        self.stun -= gfw.delta_time
        self.fidx = round(self.time * Enemy.FPS)
        if self.stun <= 0:
            self.time = 0
            self.action = 'idle'

    def do_die(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Enemy.FPS)
        if self.fidx >= len(self.images['die']):
            self.remove()

    def update(self):
        if self.action == 'walk':
            Enemy.do_walk(self)
        elif self.action == 'attack':
            Enemy.do_attack(self)
        elif self.action == 'idle':
            Enemy.do_idle(self)
        elif self.action == 'hit':
            Enemy.do_hit(self)
        elif self.action == 'die':
            Enemy.do_die(self)

    def remove(self):
        gfw.world.remove(self)

    def decrease_life(self, amount, stun):
        self.hp -= amount
        self.time = 0
        if self.hp <= 0:
            self.action = 'die'
        else:
            self.action = 'hit'
            self.stun = stun
        return self.hp <= 0

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        flip = 'h' if self.delta[0] < 0 else ''
        image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

class Knh(Enemy):
    def __init__(self, pos, add_damage, add_hp):
        super().__init__(pos, (-1, 0), 200, 'knh', 3 + add_damage, 60 + add_hp, 500, 1.0, KnhBullet,(-50, -30))

    @staticmethod
    def load_all_images():
        Knh.load_images('knh')

    def get_bb(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 13 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y + 5 * gobj.PIXEL_SCOPE

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE

