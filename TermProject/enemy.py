import gobj
import gfw
from pico2d import *
from bullet import KnhBullet
from bullet import NkmBullet

class Enemy:
    ACTIONS = ['attack', 'hit', 'idle', 'walk']
    images = {}
    FPS = 12

    def __init__(self, pos, delta, speed, char, damage, hp):
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

    def update(self):
        pass

    def remove(self):
        gfw.world.remove(self)

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        flip = 'h' if self.delta[0] < 0 else ''
        image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

class Knh(Enemy):
    def __init__(self, pos, add_damage, add_hp):
        super().__init__(pos, (-1, 0), 400, 'knh', 3 + add_damage, 60 + add_hp)

    @staticmethod
    def load_all_images():
        Knh.load_images('knh')

