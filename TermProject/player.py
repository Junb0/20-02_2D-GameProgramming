import gobj
import gfw
from pico2d import *

class Body:
    ACTIONS = ['die', 'hit', 'idle', 'moveback', 'movefront']
    images = {}
    FPS = 12

    def __init__(self):
        self.pos = (get_canvas_width() // 2, get_canvas_height() // 2)
        self.delta = 0
        self.char = 'hana'
        self.file_fmt = '%s/Sprites/actors/%s/%s/spr_chr_hna_%s%d.png'
        self.images = Body.load_images(self.char, self.file_fmt)
        self.action = 'idle'
        self.speed = 100
        self.fidx = 0
        self.time = 0

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

    def update(self):
        if self.action == 'idle':
            Body.do_idle(self)

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


class Player:
    def __init__(self):
        self.body = Body()
        self.weapon = Weapon()

    def update(self):
        self.body.update()
        self.weapon.update()

    def draw(self):
        self.body.draw()
        self.weapon.draw()

    @staticmethod
    def load_all_images():
        Body.load_all_images()
        Weapon.load_all_images()
