from pico2d import *
from ext_pico2d import *
import gfw
import gobj
import player as P

class UIFrame:
    image = None

    def __init__(self, player):
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/UI/spr_ui_frame.png')
        self.font_ui = gfw.font.load(gobj.res('manaspc.ttf'),35)
        self.font_message = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 20)
        self.player = player

    def draw(self):
        image = self.image
        image.composite_draw(0, '', get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())
        self.font_ui.draw(10, 630, str(self.player.weapon.ammo), (255, 255, 255))
        self.font_ui.draw(100, 630, str(self.player.weapon.max_ammo), (255, 255, 255))
    def update(self):
        pass

    def handle_event(self, e):
        pass