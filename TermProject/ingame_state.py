import gfw
from pico2d import *
import gobj

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['bg', 'bullet' , 'character', 'ui'])

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    # gobj.draw_collision_box()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
