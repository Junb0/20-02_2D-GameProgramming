import gfw
import gobj
from pico2d import *
from ext_pico2d import *
from button import Button
import sound

canvas_width = 1280
canvas_height = 720

DIFFICULTY_STR_LIST = ['Easy', 'Normal', 'Hard']

def bgm_volume_down():
    gobj.BGM_VOLUME = clamp(0, gobj.BGM_VOLUME - 1, 10)
    sound.update_volume()

def bgm_volume_up():
    gobj.BGM_VOLUME = clamp(0, gobj.BGM_VOLUME + 1, 10)
    sound.update_volume()

def se_volume_down():
    gobj.SE_VOLUME = clamp(0, gobj.SE_VOLUME - 1, 10)
    sound.update_volume()

def se_volume_up():
    gobj.SE_VOLUME = clamp(0, gobj.SE_VOLUME + 1, 10)
    sound.update_volume()

def difficulty_down():
    gobj.DIFFICULTY = clamp(1, gobj.DIFFICULTY - 1, 3)

def difficulty_up():
    gobj.DIFFICULTY = clamp(1, gobj.DIFFICULTY + 1, 3)

def back_to_title():
    gobj.BACK_TO_TITLE = True
    gfw.pop()

def enter():
    gfw.world.init(['bg', 'ui'])
    center = (canvas_width // 2, canvas_height // 2)
    bg = gobj.ImageObject('option.png', center)
    gfw.world.add(gfw.layer.bg, bg)

    global font
    font = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 40)
    global font2
    font = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 35)
    global l, b, w, h
    l, b, w, h = 500, 350, 80, 80
    btn = Button(l, b, w, h, font, "<", lambda: bgm_volume_down())
    gfw.world.add(gfw.layer.ui, btn)

    l = 700
    btn = Button(l, b, w, h, font, ">", lambda: bgm_volume_up())
    gfw.world.add(gfw.layer.ui, btn)

    b-= 150
    l = 500
    btn = Button(l, b, w, h, font, "<", lambda: se_volume_down())
    gfw.world.add(gfw.layer.ui, btn)

    l = 700
    btn = Button(l, b, w, h, font, ">", lambda: se_volume_up())
    gfw.world.add(gfw.layer.ui, btn)

    b -= 150
    l = 500
    btn = Button(l, b, w, h, font, "<", lambda: difficulty_down())
    gfw.world.add(gfw.layer.ui, btn)

    l = 700
    btn = Button(l, b, w, h, font, ">", lambda: difficulty_up())
    gfw.world.add(gfw.layer.ui, btn)

    l = 950
    w = 300
    btn = Button(l, b, w, h, font, "Back to Title", lambda: back_to_title())
    gfw.world.add(gfw.layer.ui, btn)


def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    draw_centered_text(font, 'BGM Volume', 0, 420, get_canvas_width(), 80)
    draw_centered_text(font, str(gobj.BGM_VOLUME), 0, 350, get_canvas_width(), 80)
    draw_centered_text(font, 'SE Volume', 0, 270, get_canvas_width(), 80)
    draw_centered_text(font, str(gobj.SE_VOLUME), 0, 200, get_canvas_width(), 80)
    draw_centered_text(font, 'Difficulty', 0, 120, get_canvas_width(), 80)
    draw_centered_text(font, str(DIFFICULTY_STR_LIST[gobj.DIFFICULTY - 1]), 0, 50, get_canvas_width(), 80)


def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.pop()

    if handle_mouse(e):
        return

capture = None
def handle_mouse(e):
    global capture
    if capture is not None:
        holding = capture.handle_event(e)
        if not holding:
            capture = None
        return True

    for obj in gfw.world.objects_at(gfw.layer.ui):
        if obj.handle_event(e):
            capture = obj
            return True

def pause():
    pass

def resume():
    pass

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()