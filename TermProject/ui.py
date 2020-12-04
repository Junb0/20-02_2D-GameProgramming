from pico2d import *
from ext_pico2d import *
import gfw
import gobj

MESSAGE_TIME = 1

class UIFrame:
    image = None

    def __init__(self, player):
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/UI/spr_ui_frame.png')
        self.font_ui1 = gfw.font.load(gobj.res('manaspc.ttf'),35)
        self.font_ui2 = gfw.font.load(gobj.res('manaspc.ttf'), 30)
        self.font_ui3 = gfw.font.load(gobj.res('manaspc.ttf'), 20)
        self.font_ui4 = gfw.font.load(gobj.res('manaspc.ttf'), 40)
        self.font_message = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 40)
        self.player = player
        self.display_life = player.life
        self.display_gold = player.gold
        self.display_score = gobj.SCORE
        self.message_time1 = MESSAGE_TIME
        self.message_time2 = MESSAGE_TIME
        self.messages1 = []
        self.messages2 = []
        self.ad_ui = ''
        self.magazine_ui = ''
        self.tower_ui = ''
        self.repair_ui = ''
        self.wave_ui = 0

    def draw(self):
        image = self.image
        image.composite_draw(0, '', get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())
        self.font_ui1.draw(10, 630, str(self.player.weapon.ammo), (255, 255, 255))
        self.font_ui1.draw(100, 630, str(self.player.weapon.max_ammo), (255, 255, 255))
        self.font_ui2.draw(210, 680, str(self.display_life), (255, 255, 255))
        self.font_ui2.draw(210, 620, str(self.display_gold), (255, 255, 255))
        self.font_ui4.draw(1120, 670, str(self.wave_ui), (255, 255, 255))
        self.font_ui3.draw(1095, 620, 'score : ' + str(self.display_score).zfill(6), (255, 255, 255))
        draw_centered_text(self.font_ui3, self.ad_ui, 450, 580, 115, 20)
        draw_centered_text(self.font_ui3, self.magazine_ui, 611, 580, 115, 20)
        draw_centered_text(self.font_ui3, self.tower_ui, 777, 580, 115, 20)
        draw_centered_text(self.font_ui3, self.repair_ui, 937, 580, 115, 20)

        if len(self.messages1):
            draw_centered_text(self.font_message, self.messages1[0], 0, 530, 1280, 40)
        if len(self.messages2):
            draw_centered_text(self.font_message, self.messages2[0], 0, 490, 1280, 40, (255, 215, 0))

    def update(self):
        if self.display_life < self.player.life:
            self.display_life += 1
        elif self.display_life > self.player.life:
            self.display_life -= 1

        if self.display_gold < self.player.gold:
            self.display_gold += 1
        elif self.display_gold > self.player.gold:
            self.display_gold -= 1

        if self.display_score < gobj.SCORE:
            self.display_score += 1
        elif self.display_score > gobj.SCORE:
            self.display_score -= 1

        if self.message_time1 > 0 and len(self.messages1):
            self.message_time1 -= gfw.delta_time
            if self.message_time1 <= 0:
                self.messages1.pop(0)
                self.message_time1 = MESSAGE_TIME

        if self.message_time2 > 0 and len(self.messages2):
            self.message_time2 -= gfw.delta_time
            if self.message_time2 <= 0:
                self.messages2.pop(0)
                self.message_time2 = MESSAGE_TIME

    def handle_event(self, e):
        pass