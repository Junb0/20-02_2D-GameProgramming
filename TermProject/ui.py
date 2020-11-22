from pico2d import *
from ext_pico2d import *
import gfw
import gobj
import player as P

class UIFrame:
    image = None

    def __init__(self, player):
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/UI/spr_ui_frame.png')
        self.font_ui1 = gfw.font.load(gobj.res('manaspc.ttf'),35)
        self.font_ui2 = gfw.font.load(gobj.res('manaspc.ttf'), 30)
        self.font_message = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 20)
        self.player = player
        self.display_life = player.life
        self.display_gold = player.gold

    def draw(self):
        image = self.image
        image.composite_draw(0, '', get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())
        self.font_ui1.draw(10, 630, str(self.player.weapon.ammo), (255, 255, 255))
        self.font_ui1.draw(100, 630, str(self.player.weapon.max_ammo), (255, 255, 255))
        self.font_ui2.draw(210, 680, str(self.display_life), (255, 255, 255))
        self.font_ui2.draw(210, 620, str(self.display_gold), (255, 255, 255))
    def update(self):
        if self.display_life < self.player.life:
            self.display_life += 1
        elif self.display_life > self.player.life:
            self.display_life -= 1

        if self.display_gold < self.player.gold:
            self.display_gold += 1
        elif self.display_gold > self.player.gold:
            self.display_gold -= 1

    def handle_event(self, e):
        pass