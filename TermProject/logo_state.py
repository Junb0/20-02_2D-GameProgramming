import gfw
import gobj
from pico2d import *
import ingame_state

canvas_width = 1280
canvas_height = 720

def enter():
    global image, elapsed
    image = gfw.image.load(gobj.RES_DIR + '/kpu_credit.png')
    elapsed = 0

def update():
    global elapsed
    elapsed += gfw.delta_time
    if elapsed > 1.0:
        gfw.change(ingame_state)

def draw():
    image.draw(canvas_width // 2, canvas_height // 2)

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
def exit():
    global image
    del image

if __name__ == '__main__':
    gfw.run_main()