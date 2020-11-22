from pico2d import *
import gfw
import gobj
import tower

class UIFrame:
    image = None
    global player

    def __init__(self):
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/UI/spr_ui_frame.png')

    def draw(self):
        image = self.image
        image.composite_draw(0, '', get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())

    def update(self):
        pass

    def handle_event(self, e):
        pass