import gobj
import gfw
from pico2d import *
import enemy
from bullet import ShortBullet


class Tower:
    ACTIONS = ['idle', 'attack']
    images = {}
    FPS = 12

    def __init__(self, pos, attack_delay = 4, add_damage = 0):
        self.pos = pos
        self.damage = 20 + add_damage
        self.attack_delay = attack_delay
        self.attack_cooltime = 0
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

    def check_enemy(self):
        for e in gfw.world.objects_at(gfw.layer.any):
            if isinstance(e, enemy.Enemy):
                if e.action != 'die' and e.get_bb()[1] <= self.pos[1] - 5 * gobj.PIXEL_SCOPE and e.get_bb()[3] >= self.pos[1] - 5 * gobj.PIXEL_SCOPE:
                    return True
    def do_idle(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Tower.FPS)
        self.attack_cooltime -= gfw.delta_time
        if self.attack_cooltime <= 0 and self.check_enemy():
            self.time = 0
            self.action = 'attack'

    def generate_bullet(self):
        blt = ShortBullet((self.pos[0] + 18 * gobj.PIXEL_SCOPE, self.pos[1] - 5 * gobj.PIXEL_SCOPE), self.damage, 1.0)
        gfw.world.add(gfw.layer.any, blt)

    def do_attack(self):
        if self.attack_cooltime <= 0 and self.fidx == 4:
            self.generate_bullet()
            self.attack_cooltime = self.attack_delay
        self.time += gfw.delta_time
        self.attack_cooltime -= gfw.delta_time
        self.fidx = round(self.time * Tower.FPS)
        if self.fidx >= len(self.images['attack']):
            self.time = 0
            self.action = 'idle'

    def update(self):
        if self.action == 'idle':
            self.do_idle()
        elif self.action == 'attack':
            self.do_attack()

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        flip = ''
        image.composite_draw(0, flip, *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 16 * gobj.PIXEL_SCOPE
