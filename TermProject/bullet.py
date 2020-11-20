from pico2d import *
import gfw
import gobj

class Bullet:
    images = {}
    ACTION = ['move', 'hit']
    FPS = 12
    def __init__(self, pos, delta, speed, char):
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.char = char
        self.images = Bullet.load_images(self.char)
        self.time = 0
        self.fidx = 0
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

    def do_hit(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * Bullet.FPS)
        if self.fidx >= len(self.images['hit']):
            self.remove()

    def update(self):
        if self.action == 'move':
            Bullet.do_move(self)
        elif self.action == 'hit':
            Bullet.do_hit(self)

    def remove(self):
        gfw.world.remove(self)

    def handle_event(self, e):
        pass

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        image.composite_draw(0, '', *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

class LongBullet(Bullet):
    def __init__(self, pos, damage):
        super().__init__(pos, (1, 0), 1000, 'long')
        self.damage = damage

    @staticmethod
    def load_all_images():
        LongBullet.load_images('long')