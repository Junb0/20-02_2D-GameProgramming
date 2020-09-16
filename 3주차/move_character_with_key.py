from pico2d import *

open_canvas()
grass = load_image('../res/grass.png')
character = load_image('../res/run_animation.png')


def handle_events():
    global running
    global dx
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dx += 1
            elif event.key == SDLK_LEFT:
                dx -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dx -= 1
            elif event.key == SDLK_LEFT:
                dx += 1


running = True
x = get_canvas_width() // 2
frame = 0
dx = 0

while (x < 800 and running):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, x, 90)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x += dx * 5
    delay(0.02)


close_canvas()
