import gobj
import gfw
from pico2d import *
from bullet import LongBullet

class Tower:
    ACTIONS = ['idle', 'attack']
    images = {}
    FPS = 12

    def __init__(self, pos, damage, attack_delay):
        self.pos = pos
        self.damage = damage
        self.attack_delay = attack_delay
        self.time = 0
        self.fidx = 0
        self.action = 'idle'
        self.char = 'tower'
        self.images = Tower.load_images(self.char)

    @staticmethod
    def load_images(char):
        if char in Tower.images:
            return Tower.images[char]
        images = {}
        count = 0
        file_fmt = '%s/Sprites/Objects/%s/%s/spr_obj_%s_%s%d.png'

        for action in Tower.ACTIONS:
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, char, action, char, action, n)
                if os.path.isfile(fn):
                    action_images.append(gfw.image.load(fn))
                else:
                    break
                count += 1
            images[action] = action_images
        Tower.images[char] = images
        print('%d images loaded for %s' % (count, char))
        return images

    def update(self):
        pass

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        flip = ''
        image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE
