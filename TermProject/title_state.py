import gfw
import gobj
from pico2d import *
from button import Button
import ingame_state
import option_state

canvas_width = 1280
canvas_height = 720

def start():
    gfw.push(ingame_state)

def option():
    gfw.push(option_state)

def build_world():
    gfw.world.init(['bg', 'ui'])
    center = (canvas_width // 2, canvas_height // 2)
    bg = gobj.ImageObject('title.png', center)
    gfw.world.add(gfw.layer.bg, bg)

    font = gfw.font.load(gobj.res('Sam3KRFont.ttf'), 40)
    l, b, w, h = 500, 250, get_canvas_width() - 1000, 80
    btn = Button(l, b, w, h, font, "Start", lambda: start())
    gfw.world.add(gfw.layer.ui, btn)

    b -= 100
    btn = Button(l, b, w, h, font, "Option", lambda: option())
    gfw.world.add(gfw.layer.ui, btn)

def enter():
    build_world()

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()

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
    build_world()

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()