import gfw
import gobj
from pico2d import *
from ext_pico2d import *
from button import Button
import sound

canvas_width = 1280
canvas_height = 720

def back_to_title():
    gfw.pop()
    sound.bgm_title.repeat_play()

def enter():
    gfw.world.init(['bg', 'ui'])
    center = (canvas_width // 2, canvas_height // 2)
    sound.init()
    if gobj.IS_VICTORY:
        bg = gobj.ImageObject('victory.png', center)
        sound.se_victory.play()
    else:
        bg = gobj.ImageObject('defeat.png', center)
        sound.se_defeat.play()
    gfw.world.add(gfw.layer.bg, bg)

    global font
    font = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 40)
    global font2
    font = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 35)
    global l, b, w, h
    l,b,w,h = 50,100,get_canvas_width()-100,80
    btn = Button(l, b, w, h, font, "Back to Title", lambda: back_to_title())
    gfw.world.add(gfw.layer.ui, btn)

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    if gobj.IS_VICTORY:
        draw_centered_text(font, 'score : ' + str(gobj.SCORE), 0, 420, get_canvas_width(), 80)
        draw_centered_text(font, 'kills : ' + str(gobj.KILLED_ENEMY), 0, 360, get_canvas_width(), 80)
        draw_centered_text(font, 'total gold : ' + str(gobj.PICKED_GOLD), 0, 300, get_canvas_width(), 80)
        draw_centered_text(font, 'used gold : ' + str(gobj.CONSUMED_GOLD), 0, 240, get_canvas_width(), 80)

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