import gobj
import gfw
from pico2d import *
from bullet import KnhBullet
from bullet import NkmBullet
from bullet import KrkBullet
import random
import sound

class Enemy:
    ACTIONS = ['attack', 'hit', 'idle', 'walk', 'die']
    images = {}
    FPS = 12

    def __init__(self, pos, delta, speed, char, damage, hp, attack_range, attack_delay, bullet, fire_point, drop_gold, drop_score, attack_timing = 0):
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
        self.attack_timing = attack_timing
        self.drop_gold = drop_gold
        self.drop_score = drop_score

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

    def generate_bullet(self):
        blt = self.bullet(gobj.point_add(self.pos, self.fire_point), self.damage)
        gfw.world.add(gfw.layer.any, blt)

    def do_attack(self):
        if self.attack_cooltime <= 0 and self.fidx == self.attack_timing:
            self.generate_bullet()
            self.attack_cooltime = self.attack_delay
            sound.se_enemy_attack.play()

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
            self.fidx = 0
        elif self.attack_cooltime <= 0:
            self.time = 0
            self.action = 'attack'
            self.fidx = 0

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
        super().__init__(pos, (-1, 0), 130, 'knh', 3 + add_damage, 60 + add_hp, 400, 1.0, KnhBullet,(-50, -30), 4 + random.randint(0, 2), 50)

    @staticmethod
    def load_all_images():
        Knh.load_images('knh')

    def get_bb(self):
        x, y = self.pos
        return x - 5 * gobj.PIXEL_SCOPE, y - 13 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y + 5 * gobj.PIXEL_SCOPE

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE

class Nkm(Enemy):
    def __init__(self, pos, add_damage, add_hp):
        super().__init__(pos, (-1, 0), 110, 'nkm', 6 + add_damage, 90 + add_hp, 500, 1.8, NkmBullet,(-50, -48), 7+ random.randint(0, 3), 90 ,2)

    @staticmethod
    def load_all_images():
        Nkm.load_images('nkm')

    def get_bb(self):
        x, y = self.pos
        return x - 5 * gobj.PIXEL_SCOPE, y - 20 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y + 2 * gobj.PIXEL_SCOPE

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE

class Krk(Enemy):
    def __init__(self, pos, add_damage, add_hp):
        super().__init__(pos, (-1, 0), 80, 'krk', 1 + add_damage, 140 + add_hp, 450, 4.0, KrkBullet,(-50, -70), 13 + random.randint(0, 5), 160)

    @staticmethod
    def load_all_images():
        Nkm.load_images('krk')

    def get_bb(self):
        x, y = self.pos
        return x - 5 * gobj.PIXEL_SCOPE, y - 20 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y + 2 * gobj.PIXEL_SCOPE

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE

    def generate_bullet(self):
        blt = self.bullet((50, self.pos[1] + self.fire_point[1]), self.damage, 6)
        gfw.world.add(gfw.layer.any, blt)