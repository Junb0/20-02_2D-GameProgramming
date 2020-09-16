from pico2d import *

open_canvas()
grass = load_image('../res/grass.png')
character = load_image('../res/run_animation.png')


def handle_events():
    global running, x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, get_canvas_height() - event.y - 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False



running = True
x, y = get_canvas_width() // 2, 80
frame = 0
hide_cursor()

while (x < 800 and running):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, x, y)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    delay(0.02)


close_canvas()
