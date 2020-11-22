import gobj
import gfw
from pico2d import *

class Wall:
    image = None

    def __init__(self, pos):
        self.pos = pos
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/Objects/spr_obj_shop.png')

    def draw(self):
        image = self.image
        image.composite_draw(0, '', *self.pos, image.w * gobj.PIXEL_SCOPE, image.h * gobj.PIXEL_SCOPE)

    def update(self):
        pass

    def get_ground(self):
        x, y = self.pos
        return x - 12 * gobj.PIXEL_SCOPE, y - 8 * gobj.PIXEL_SCOPE, x + 12 * gobj.PIXEL_SCOPE, y - 8 * gobj.PIXEL_SCOPE